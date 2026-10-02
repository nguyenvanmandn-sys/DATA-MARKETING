#!/usr/bin/env python3
"""
publish_wp.py — Đăng bài SEO lên WordPress qua REST API.

Chỉ dùng thư viện chuẩn của Python (urllib) — không cần cài thêm gói nào.

Cấu hình bằng biến môi trường (xem .env.example):
    WP_SITE          URL gốc của site, vd: https://danangmobile.com
    WP_USER          tên đăng nhập WordPress
    WP_APP_PASSWORD  Application Password (Users -> Profile -> Application Passwords)

Cách dùng:
    # Kiểm tra kết nối + quyền:
    python3 publish_wp.py --check

    # Đọc thử bài viết, in payload mà KHÔNG gọi mạng:
    python3 publish_wp.py articles/bai-mau.md --dry-run

    # Đăng dạng nháp (mặc định) để duyệt trong wp-admin:
    python3 publish_wp.py articles/bai-mau.md

    # Đăng public ngay:
    python3 publish_wp.py articles/bai-mau.md --publish

Định dạng file bài viết: phần front matter (giữa hai dòng ---) + thân bài HTML.
Xem articles/bai-mau.md để biết mẫu.
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


# ----------------------------- Cấu hình ------------------------------------ #

def load_dotenv(path=".env"):
    """Nạp biến từ file .env nếu có (định dạng KEY=VALUE mỗi dòng)."""
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip('"').strip("'")
            os.environ.setdefault(key, val)


def get_config():
    here = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(here, ".env"))
    site = os.environ.get("WP_SITE", "").rstrip("/")
    user = os.environ.get("WP_USER", "")
    pw = os.environ.get("WP_APP_PASSWORD", "")
    missing = [n for n, v in (("WP_SITE", site), ("WP_USER", user),
                              ("WP_APP_PASSWORD", pw)) if not v]
    if missing:
        sys.exit("Thiếu biến môi trường: " + ", ".join(missing) +
                 "\nXem seo-tools/.env.example để biết cách khai báo.")
    return site, user, pw


def auth_header(user, pw):
    # Application Password có thể chứa dấu cách; WordPress chấp nhận cả khi
    # giữ nguyên dấu cách. Dùng Basic Auth.
    token = base64.b64encode(f"{user}:{pw}".encode()).decode()
    return "Basic " + token


# --------------------------- Gọi REST API ---------------------------------- #

def api(site, user, pw, path, method="GET", payload=None, params=None):
    url = f"{site}/wp-json/wp/v2/{path.lstrip('/')}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", auth_header(user, pw))
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "claude-seo-publisher/1.0")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode()
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        raise SystemExit(
            f"Lỗi API {e.code} khi {method} {url}\n{detail[:800]}")
    except urllib.error.URLError as e:
        raise SystemExit(
            f"Không kết nối được tới {url}\nNguyên nhân: {e.reason}\n"
            "Nếu thấy 'Host not in allowlist' nghĩa là môi trường web đang "
            "chặn mạng tới site — cần thêm domain vào Network access.")


def resolve_terms(site, user, pw, taxonomy, names):
    """Đổi danh sách tên category/tag thành ID; tạo mới nếu chưa có."""
    ids = []
    for name in names:
        name = name.strip()
        if not name:
            continue
        found = api(site, user, pw, taxonomy, params={"search": name,
                                                       "per_page": 100})
        match = next((t for t in found
                      if t.get("name", "").lower() == name.lower()), None)
        if match:
            ids.append(match["id"])
        else:
            created = api(site, user, pw, taxonomy, method="POST",
                          payload={"name": name})
            ids.append(created["id"])
            print(f"  + tạo mới {taxonomy}: {name} (id={created['id']})")
    return ids


# ------------------------- Đọc file bài viết ------------------------------- #

def collect_files(paths):
    """Mở rộng danh sách đường dẫn: thư mục -> mọi file .md/.html bên trong."""
    out = []
    for p in paths:
        if os.path.isdir(p):
            for name in sorted(os.listdir(p)):
                if name.endswith((".md", ".html")):
                    out.append(os.path.join(p, name))
        elif os.path.isfile(p):
            out.append(p)
        else:
            sys.exit(f"Không tìm thấy: {p}")
    return out


def parse_article(path):
    """Tách front matter (giữa hai dòng ---) và thân bài HTML."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    meta, body = {}, text
    if text.lstrip().startswith("---"):
        text = text.lstrip()
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                key, _, val = line.partition(":")
                meta[key.strip().lower()] = val.strip()
        body = body.strip()
    if not meta.get("title"):
        sys.exit(f"Bài viết {path} thiếu 'title' trong front matter.")
    return meta, body


def build_payload(site, user, pw, meta, body, force_status=None):
    payload = {
        "title": meta["title"],
        "content": body,
        "status": force_status or meta.get("status", "draft"),
    }
    if meta.get("slug"):
        payload["slug"] = meta["slug"]
    if meta.get("excerpt"):
        # excerpt thường được theme/Yoast dùng làm mô tả meta.
        payload["excerpt"] = meta["excerpt"]
    if meta.get("categories"):
        names = meta["categories"].split(",")
        payload["categories"] = resolve_terms(site, user, pw,
                                               "categories", names)
    if meta.get("tags"):
        names = meta["tags"].split(",")
        payload["tags"] = resolve_terms(site, user, pw, "tags", names)
    return payload


# --------------------------------- CLI ------------------------------------- #

def main():
    ap = argparse.ArgumentParser(description="Đăng bài SEO lên WordPress.")
    ap.add_argument("article", nargs="*",
                    help="một hoặc nhiều file bài viết, hoặc thư mục chứa bài")
    ap.add_argument("--publish", action="store_true",
                    help="đăng public ngay (mặc định đăng nháp)")
    ap.add_argument("--dry-run", action="store_true",
                    help="chỉ in payload, không gọi mạng")
    ap.add_argument("--check", action="store_true",
                    help="kiểm tra kết nối và quyền tài khoản")
    args = ap.parse_args()

    if args.check:
        site, user, pw = get_config()
        me = api(site, user, pw, "users/me", params={"context": "edit"})
        print(f"Kết nối OK tới {site}")
        print(f"Đăng nhập với: {me.get('name')} (id={me.get('id')})")
        print(f"Quyền (capabilities) publish_posts: "
              f"{me.get('capabilities', {}).get('publish_posts', '?')}")
        return

    if not args.article:
        ap.error("cần truyền file/thư mục bài viết (hoặc dùng --check).")

    files = collect_files(args.article)
    if not files:
        sys.exit("Không tìm thấy file bài viết nào (.md/.html).")
    force_status = "publish" if args.publish else None

    if args.dry_run:
        for path in files:
            meta, body = parse_article(path)
            preview = {
                "file": path,
                "title": meta["title"],
                "status": force_status or meta.get("status", "draft"),
                "slug": meta.get("slug", "(tự sinh)"),
                "excerpt": meta.get("excerpt", ""),
                "categories": meta.get("categories", ""),
                "tags": meta.get("tags", ""),
                "content_chars": len(body),
            }
            print(json.dumps(preview, ensure_ascii=False, indent=2))
        return

    site, user, pw = get_config()
    for path in files:
        meta, body = parse_article(path)
        payload = build_payload(site, user, pw, meta, body, force_status)
        result = api(site, user, pw, "posts", method="POST", payload=payload)
        print(f"[{path}] đã tạo bài id={result['id']}, status={result['status']}")
        print(f"  Sửa: {site}/wp-admin/post.php?post={result['id']}&action=edit")
        if result.get("link"):
            print(f"  Link: {result['link']}")


if __name__ == "__main__":
    main()
