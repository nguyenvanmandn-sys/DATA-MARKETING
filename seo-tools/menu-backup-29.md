# Snapshot Main Menu (menu term id=29) — danangmobile.com

Bản chụp cấu trúc Main Menu, lấy từ lần audit trước khi menu bị xoá nhầm
(2026-05-29). Dùng để khôi phục nếu backup hosting không khả dụng.

Cột: `id` (menu item cũ) · `type/object#object_id` (nếu biết) · `url`.
Thụt lề thể hiện phân cấp cha–con. Thứ tự giữ nguyên như hiển thị.

```
iPhone                         id=396   taxonomy/product_cat#16   /iphone/
  iPhone 17 Series             id=8872  taxonomy/product_cat#675  /iphone/iphone-17-series/
  iPhone 16 Series             id=5906  taxonomy/product_cat#404  /iphone/iphone-16-series-chinh-hang-gia-re-nhat/
  iPhone 15 Series             id=5440  taxonomy/product_cat#368  /iphone/iphone-15-series/
    iPhone 15                  id=8725  taxonomy/product_cat#669  /iphone-15/
    iPhone 15 Plus             id=8726  taxonomy/product_cat#670  /iphone-15-plus/
    iPhone 15 Pro              id=8727  taxonomy/product_cat#671  /iphone-15-pro/
    iPhone 15 Pro Max          id=8728  taxonomy/product_cat#672  /iphone-15-pro-max/
  iPhone 14 Series             id=4439  taxonomy/product_cat#299  /iphone/iphone-14-series/
    iPhone 14                  id=8723  taxonomy/product_cat#667  /iphone-14/
    iPhone 14 Plus             id=8724  taxonomy/product_cat#668  /iphone-14-plus/
    iPhone 14 Pro              id=8721  taxonomy/product_cat#665  /iphone-14-pro/
    iPhone 14 Pro Max          id=8722  taxonomy/product_cat#666  /iphone-14-pro-max/
  iPhone 13 Series             id=3687  taxonomy/product_cat#242  /iphone/iphone-13/
  iPhone 12 Series             id=9145  taxonomy/product_cat#678  /iphone-12-series/
    iPhone 12 Pro | Pro Max    id=2981  taxonomy/product_cat#79   /iphone-12-series/iphone-12-pro-max/
    iPhone 12 | 12 mini        id=3035  taxonomy/product_cat#89   /iphone/iphone-12-iphone-12-mini/
  iPhone 11 Series             id=3034  taxonomy/product_cat#90   /iphone/iphone-11-series/
    iPhone 11                  id=8729  taxonomy/product_cat#673  /iphone-11/
    iPhone 11 Pro              id=8730  taxonomy/product_cat#674  /iphone-11-pro/
    iPhone 11 Pro Max          id=397   taxonomy/product_cat#22   /iphone/iphone-11-pro-max/
  iPhone X | Xs | Xs Max       id=3008  taxonomy/product_cat#19   /iphone/iphone-x-xs-xs-max/
MacBook                        id=404   (product_cat)             /macbook/
  MacBook Air                  id=3014                            /macbook/macbook-air-moi-nguyen-seal/
  MacBook Pro                  id=3015                            /macbook/macbook-pro/
  MacBook 12                   id=3013                            /macbook/macbook-12/
  iMac | Mac Mini              id=3011                            /macbook/imac-mac-mini/
Apple Watch                    id=394   (product_cat)             /apple-watch/
iPad                           id=395   (product_cat)             /ipad/
  iPad Air                     id=6278                            /ipad-air/
  iPad Pro                     id=6279                            /ipad/ipad-pro/
  iPad Gen                     id=6280                            /ipad/ipad-gen/
  iPad Mini                    id=6281                            /ipad/ipad-mini/
Phụ kiện                       id=405                             /phu-kien/   (cache cu: /phu-kien-iphone-ipad-macbook/)
Sửa chữa                       id=6846                            /sua-chua/
  Sửa iPhone                   id=6817  taxonomy/product_cat#545  /sua-chua-iphone/
    Thay pin                   id=6827                            /thay-pin-iphone/
    Thay ép kính               id=6822                            /ep-kinh-thay-mat-kinh-iphone/
    Thay màn hình              id=6828                            /thay-man-hinh-iphone/
    Thay kính cảm ứng          id=6823                            /sua-chua-iphone/thay-kinh-cam-ung-iphone/
    Thay camera sau            id=6820                            /sua-chua-iphone/thay-camera-sau-iphone/
    Thay camera trước          id=6821                            /sua-chua-iphone/thay-camera-truoc-iphone/
    Thay loa ngoài             id=6825                            /sua-chua-iphone/thay-loa-ngoai-iphone/
    Thay loa trong             id=6826                            /sua-chua-iphone/thay-loa-trong-iphone/
    Thay kính lưng             id=6824                            /sua-chua-iphone/thay-kinh-lung-iphone/
    Thay vỏ                    id=6829                            /sua-chua-iphone/thay-vo-iphone/
    Ép cổ cáp màn hình         id=6819                            /sua-chua-iphone/ep-co-cap-man-hinh-iphone/
  Sửa chữa Macbook             id=6716                            /sua-chua-macbook-da-nang/
    Màn hình MacBook           id=6730                            /sua-chua-macbook-da-nang/man-hinh-macbook/
    Pin MacBook                id=6741                            /thay-pin-macbook-chinh-hang/
    Bàn phím MacBook           id=6717                            /sua-chua-macbook-da-nang/ban-phim-macbook/
    Loa MacBook                id=6727                            /sua-chua-macbook-da-nang/loa-macbook/
    Loa MacBook                id=6751                            /sua-chua-macbook-da-nang/loa-macbook/
    Thay quạt tản nhiệt        id=6754                            /sua-chua-macbook-da-nang/thay-quat-tan-nhiet/
    Sửa Main MacBook           id=6763                            /sua-chua-macbook-da-nang/sua-main-macbook/
    Thay Ổ Cứng MacBook        id=6764                            /sua-chua-macbook-da-nang/thay-o-cung-macbook/
  Sửa iPad                     id=6770                            /sua-chua/sua-ipad/
    Thay pin iPad              id=6771                            /sua-chua/sua-ipad/thay-pin-ipad/
    Ép kính iPad               id=6776                            /sua-chua/sua-ipad/ep-kinh-ipad/
    Thay màn hình iPad         id=6780                            /sua-chua/sua-ipad/thay-man-hinh-ipad/
    Thay kính cảm ứng iPad     id=6847                            /sua-chua/sua-ipad/thay-kinh-cam-ung-ipad/
    Thay main iPad             id=6790                            /sua-chua/sua-ipad/thay-main-ipad/
    Thay cáp sạc iPad          id=6797                            /sua-chua/sua-ipad/thay-cap-sac-ipad/
    Thay cáp home iPad         id=6802                            /sua-chua/sua-ipad/thay-cap-home-ipad/
    Thay vỏ iPad               id=6810                            /sua-chua/sua-ipad/thay-vo-ipad/
    Thay loa ngoài iPad        id=6815                            /sua-chua/sua-ipad/thay-loa-ngoai-ipad/
Sửa iPhone, Sửa MacBook        id=6767  taxonomy/category#543     /meo-vat/
Tin tức & Sự kiện              id=2313                            /tin-tuc-su-kien/
```

Ghi chú:
- Icon và thiết lập mega-menu của theme Flatsome lưu trong post meta của
  từng nav_menu_item, KHÔNG có trong snapshot này — chỉ backup hosting mới
  khôi phục được phần đó.
- Các URL "cache cũ" có thể 404; khi dựng lại nên ưu tiên dùng object_id
  (taxonomy) để WordPress tự sinh link danh mục đúng.
