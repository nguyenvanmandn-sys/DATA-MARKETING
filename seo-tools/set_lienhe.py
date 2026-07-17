#!/usr/bin/env python3
"""set_lienhe.py — Đưa toàn bộ sản phẩm iPhone/iPad/MacBook/Apple Watch về "Liên hệ".
Sao lưu giá cũ vào price-backup-lienhe.json trước khi xoá (để khôi phục được).
KHÔNG đụng sản phẩm dịch vụ sửa chữa (lọc theo từ khoá).
"""
import publish_wp as p, json, urllib.request, urllib.parse, sys, time
site,user,pw=p.get_config()

def wc(path,method="GET",payload=None,params=None,tries=3):
    url=f"{site}/wp-json/wc/v3/{path}"
    if params: url+="?"+urllib.parse.urlencode(params)
    data=json.dumps(payload).encode() if payload is not None else None
    for t in range(tries):
        try:
            req=urllib.request.Request(url,data=data,method=method)
            req.add_header("Authorization",p.auth_header(user,pw))
            req.add_header("Content-Type","application/json"); req.add_header("User-Agent","Mozilla/5.0")
            with urllib.request.urlopen(req,timeout=60) as r: return json.loads(r.read().decode())
        except Exception as e:
            if t==tries-1: raise
            time.sleep(2)

def log(m):
    print(m, flush=True)

# 1) danh muc thiet bi + con
cats=[]
for pg in range(1,6):
    b=wc("products/categories",params={"per_page":100,"page":pg})
    cats+=b
    if len(b)<100: break
parent={c["id"]:c["parent"] for c in cats}
device={16,21,28,23}
ch=True
while ch:
    ch=False
    for cid,par in parent.items():
        if par in device and cid not in device:
            device.add(cid); ch=True
log(f"[scope] {len(device)} danh muc thiet bi")

# 2) san pham thiet bi (bo dich vu sua)
repair=("thay ","sửa","ép ","màn hình","kính","pin ","camera","loa ","vỏ ","cáp","main","dán","adapter","củ sạc","tai nghe","airpod")
targets=[]
for pg in range(1,15):
    b=wc("products",params={"per_page":100,"page":pg,"status":"publish"})
    if not b: break
    for x in b:
        cids={c["id"] for c in x.get("categories",[])}
        if cids & device and not any(k in x["name"].lower() for k in repair):
            targets.append({"id":x["id"],"name":x["name"],"type":x["type"],
                            "regular_price":x.get("regular_price"),"sale_price":x.get("sale_price")})
    if len(b)<100: break
log(f"[scope] {len(targets)} san pham se ve Lien he")

# 3) xu ly tung san pham: backup + xoa gia
backup=[]
done=0; err=0
for rec in targets:
    try:
        if rec["type"]=="variable":
            vs=wc(f"products/{rec['id']}/variations",params={"per_page":100})
            rec["variations"]=[{"id":v["id"],"regular_price":v.get("regular_price"),"sale_price":v.get("sale_price")} for v in vs]
            if rec["variations"]:
                wc(f"products/{rec['id']}/variations/batch",method="POST",
                   payload={"update":[{"id":v["id"],"regular_price":"","sale_price":""} for v in rec["variations"]]})
        wc(f"products/{rec['id']}",method="PUT",payload={"regular_price":"","sale_price":""})
        backup.append(rec); done+=1
    except Exception as e:
        err+=1; log(f"  ! loi id={rec['id']}: {str(e)[:80]}")
    if done % 20 == 0:
        open("price-backup-lienhe.json","w",encoding="utf-8").write(json.dumps(backup,ensure_ascii=False,indent=1))
        log(f"  ...da xu ly {done}/{len(targets)}")

open("price-backup-lienhe.json","w",encoding="utf-8").write(json.dumps(backup,ensure_ascii=False,indent=1))
log(f"[DONE] Da set ve Lien he: {done} san pham. Loi: {err}. Backup: price-backup-lienhe.json")
