#!/usr/bin/env python3
"""rebuild_menu.py — Dựng lại Main Menu danangmobile.com từ snapshot.

Tạo menu 'Main Menu', gán vào location 'primary', rồi tạo lại toàn bộ
67 mục đúng thứ tự + phân cấp. Mỗi mục trỏ tới product_cat/category bằng
object_id để WordPress tự sinh URL chuẩn (không dùng URL cache cũ).
"""
from publish_wp import get_config, api

# (old_id, parent_old_id, title, kind, ref)
#   kind: 'pc'=product_cat object_id, 'cat'=category object_id, 'auto'=resolve theo slug rồi custom
ITEMS = [
 (396,0,"iPhone","pc",16),
 (8872,396,"iPhone 17 Series","pc",675),
 (5906,396,"iPhone 16 Series","pc",404),
 (5440,396,"iPhone 15 Series","pc",368),
 (8725,5440,"iPhone 15","pc",669),
 (8726,5440,"iPhone 15 Plus","pc",670),
 (8727,5440,"iPhone 15 Pro","pc",671),
 (8728,5440,"iPhone 15 Pro Max","pc",672),
 (4439,396,"iPhone 14 Series","pc",299),
 (8723,4439,"iPhone 14","pc",667),
 (8724,4439,"iPhone 14 Plus","pc",668),
 (8721,4439,"iPhone 14 Pro","pc",665),
 (8722,4439,"iPhone 14 Pro Max","pc",666),
 (3687,396,"iPhone 13 Series","pc",242),
 (9145,396,"iPhone 12 Series","pc",678),
 (2981,9145,"iPhone 12 Pro | Pro Max","pc",79),
 (3035,9145,"iPhone 12 | 12 mini","pc",89),
 (3034,396,"iPhone 11 Series","pc",90),
 (8729,3034,"iPhone 11","pc",673),
 (8730,3034,"iPhone 11 Pro","pc",674),
 (397,3034,"iPhone 11 Pro Max","pc",22),
 (3008,396,"iPhone X | Xs | Xs Max","pc",19),
 (404,0,"MacBook","pc",28),
 (3014,404,"MacBook Air","pc",85),
 (3015,404,"MacBook Pro","pc",84),
 (3013,404,"MacBook 12","pc",86),
 (3011,404,"iMac | Mac Mini","pc",87),
 (394,0,"Apple Watch","pc",23),
 (395,0,"iPad","pc",21),
 (6278,395,"iPad Air","pc",433),
 (6279,395,"iPad Pro","pc",434),
 (6280,395,"iPad Gen","pc",435),
 (6281,395,"iPad Mini","pc",436),
 (405,0,"Phụ kiện","pc",20),
 (6846,0,"Sửa chữa","pc",614),
 (6817,6846,"Sửa iPhone","pc",545),
 (6827,6817,"Thay pin","pc",603),
 (6822,6817,"Thay ép kính","pc",605),
 (6828,6817,"Thay màn hình","pc",604),
 (6823,6817,"Thay kính cảm ứng","pc",606),
 (6820,6817,"Thay camera sau","pc",607),
 (6821,6817,"Thay camera trước","pc",608),
 (6825,6817,"Thay loa ngoài","pc",609),
 (6826,6817,"Thay loa trong","pc",610),
 (6824,6817,"Thay kính lưng","pc",611),
 (6829,6817,"Thay vỏ","pc",612),
 (6819,6817,"Ép cổ cáp màn hình","pc",613),
 (6716,6846,"Sửa chữa Macbook","pc",466),
 (6730,6716,"Màn hình MacBook","pc",482),
 (6741,6716,"Pin MacBook","pc",483),
 (6717,6716,"Bàn phím MacBook","pc",484),
 (6727,6716,"Loa MacBook","pc",486),
 (6754,6716,"Thay quạt tản nhiệt","pc",487),
 (6763,6716,"Sửa Main MacBook","pc",488),
 (6764,6716,"Thay Ổ Cứng MacBook","pc",489),
 (6770,6846,"Sửa iPad","pc",557),
 (6771,6770,"Thay pin iPad","pc",558),
 (6776,6770,"Ép kính iPad","pc",559),
 (6780,6770,"Thay màn hình iPad","pc",560),
 (6847,6770,"Thay kính cảm ứng iPad","pc",581),
 (6790,6770,"Thay main iPad","pc",562),
 (6797,6770,"Thay cáp sạc iPad","pc",563),
 (6802,6770,"Thay cáp home iPad","pc",564),
 (6810,6770,"Thay vỏ iPad","pc",566),
 (6815,6770,"Thay loa ngoài iPad","pc",567),
 (6767,0,"Sửa iPhone, Sửa MacBook","cat",543),
 (2313,0,"Tin tức & Sự kiện","auto","tin-tuc-su-kien"),
]

def main():
    site,user,pw=get_config()
    # 1) tao menu + gan location primary
    menu=api(site,user,pw,"menus",method="POST",
             payload={"name":"Main Menu","locations":["primary"]})
    mid=menu["id"]
    print(f"Tao menu 'Main Menu' id={mid}, locations={menu.get('locations')}")
    idmap={0:0}
    for order,(oid,pold,title,kind,ref) in enumerate(ITEMS, start=1):
        payload={"title":title,"menus":mid,"menu_order":order,
                 "parent":idmap.get(pold,0),"status":"publish"}
        if kind=="pc":
            payload.update(type="taxonomy",object="product_cat",object_id=ref)
        elif kind=="cat":
            payload.update(type="taxonomy",object="category",object_id=ref)
        else:  # auto: thu category -> product_cat -> custom url
            tid=None;obj=None
            for tax in ("categories","product_cat"):
                f=api(site,user,pw,tax,params={"slug":ref})
                if f: tid=f[0]["id"];obj="category" if tax=="categories" else "product_cat";break
            if tid:
                payload.update(type="taxonomy",object=obj,object_id=tid)
            else:
                payload.update(type="custom",url=f"https://danangmobile.com/{ref}/")
        r=api(site,user,pw,"menu-items",method="POST",payload=payload)
        idmap[oid]=r["id"]
        print(f"  [{order:2}] {title[:34]:<34} -> id={r['id']} parent={payload['parent']}")
    print(f"\nXONG: tao {len(ITEMS)} muc trong menu id={mid}")

if __name__=="__main__":
    main()
