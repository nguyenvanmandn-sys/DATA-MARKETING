#!/usr/bin/env python3
"""add_images.py — Upload ảnh lên WordPress Media rồi chèn vào bài đã đăng.

Dùng chung cấu hình WP_SITE / WP_USER / WP_APP_PASSWORD với publish_wp.py.
Chỉ dùng thư viện chuẩn (urllib).

Mỗi mục trong PLAN: post_id -> {alt, images:[đường dẫn file ảnh local]}.
- Ảnh đầu tiên được đặt làm featured image (ảnh đại diện).
- Tất cả ảnh được chèn dạng <figure> rải đều trong thân bài (trước mỗi <h2>),
  ảnh dư thì nối vào cuối.
"""

import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request

from publish_wp import get_config, auth_header, api

# post_id -> cấu hình ảnh
PLAN = {
    10369: {"alt": "Mua iPhone cũ tại Đà Nẵng",
            "images": ["/tmp/imgs/iphone-1011.jpg",
                       "/tmp/imgs/iphone-1012.jpg",
                       "/tmp/imgs/iphone-1013.jpg"]},
    10370: {"alt": "Mua iPhone trả góp tại Đà Nẵng",
            "images": ["/tmp/imgs/iphone-0220.jpg"]},
    10371: {"alt": "Phân biệt iPhone chính hãng và hàng dựng",
            "images": ["/tmp/imgs/iphone-0252.jpg"]},
    10372: {"alt": "Sửa MacBook tại Đà Nẵng",
            "images": ["/tmp/imgs/macbook-1033.jpg",
                       "/tmp/imgs/macbook-1038.jpg"]},
    10373: {"alt": "Thay màn hình iPhone tại Đà Nẵng",
            "images": ["/tmp/imgs/iphone-0278.jpg"]},
    10374: {"alt": "Thay pin iPhone tại Đà Nẵng",
            "images": ["/tmp/imgs/iphone-0125.jpg"]},
}


def upload_media(site, user, pw, path, alt):
    """Upload 1 file ảnh, trả về (id, source_url)."""
    fname = os.path.basename(path)
    ctype = mimetypes.guess_type(fname)[0] or "image/jpeg"
    with open(path, "rb") as fh:
        body = fh.read()
    url = f"{site}/wp-json/wp/v2/media"
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", auth_header(user, pw))
    req.add_header("Content-Type", ctype)
    req.add_header("Content-Disposition", f'attachment; filename="{fname}"')
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "claude-seo-publisher/1.0")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            media = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Lỗi upload {fname}: {e.code}\n{e.read().decode()[:600]}")
    mid = media["id"]
    # đặt alt text + title + caption cho SEO
    api(site, user, pw, f"media/{mid}", method="POST",
        payload={"alt_text": alt, "title": alt, "caption": alt})
    print(f"  upload {fname} -> media id={mid}")
    return mid, media["source_url"]


def figure_html(src, alt, mid):
    return (f'\n<figure class="wp-block-image size-large">'
            f'<img src="{src}" alt="{alt}" class="wp-image-{mid}"/>'
            f'<figcaption>{alt}</figcaption></figure>\n')


def insert_figures(content, figures):
    """Chèn các figure trước mỗi <h2>; figure dư nối vào cuối."""
    if not figures:
        return content
    marker = "<h2"
    idx = content.find(marker)
    if idx == -1:
        return content + "".join(figures)
    out = content[:idx]
    rest = content[idx:]
    fi = 0
    # tách theo từng <h2> và chèn 1 figure trước mỗi heading
    while True:
        nxt = rest.find(marker, len(marker))
        block = rest if nxt == -1 else rest[:nxt]
        if fi < len(figures):
            out += figures[fi]
            fi += 1
        out += block
        if nxt == -1:
            break
        rest = rest[nxt:]
    # còn dư -> nối cuối
    if fi < len(figures):
        out += "".join(figures[fi:])
    return out


def main():
    site, user, pw = get_config()
    for post_id, cfg in PLAN.items():
        alt = cfg["alt"]
        figs, featured = [], None
        for p in cfg["images"]:
            mid, src = upload_media(site, user, pw, p, alt)
            if featured is None:
                featured = mid
            figs.append(figure_html(src, alt, mid))
        # lấy nội dung hiện tại (raw)
        post = api(site, user, pw, f"posts/{post_id}",
                   params={"context": "edit"})
        raw = post["content"]["raw"]
        new_content = insert_figures(raw, figs)
        api(site, user, pw, f"posts/{post_id}", method="POST",
            payload={"content": new_content, "featured_media": featured})
        print(f"[post {post_id}] +{len(figs)} ảnh, featured={featured} ✓")


if __name__ == "__main__":
    main()
