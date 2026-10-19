# Cấu hình kết nối Claude ↔ danangmobile.com

Tài liệu này mô tả cách Claude kết nối và làm việc với website
**danangmobile.com**. Lưu lại để các phiên sau kết nối lại nhanh.

> ⚠️ **Bảo mật:** file này KHÔNG chứa mật khẩu thật. Khoá thật nằm trong
> `seo-tools/.env` (đã được `.gitignore` bỏ qua, không commit). Xem mục
> "Khôi phục kết nối" bên dưới.

---

## 1. Website
- **URL:** https://danangmobile.com
- **Nền tảng:** WordPress + WooCommerce
- **Theme:** Flatsome (child: flatsome-child)
- **Plugin chính:** Rank Math SEO (PRO), Solid Security Pro, LiteSpeed Cache, ACF, WPClever
- **CDN/Proxy:** Cloudflare (nhớ Purge cache sau khi đổi nội dung)

## 2. Cách kết nối (cơ chế)
Claude làm việc với site qua **REST API + Basic Auth bằng Application Password**
(không dùng mật khẩu đăng nhập thường).

| Thành phần | Giá trị |
|---|---|
| Tài khoản | `aiquantri` (Nguyễn Văn Mẫn, user id = 8, vai trò Administrator) |
| Loại xác thực | WordPress **Application Password** (Basic Auth qua HTTPS) |
| Tạo App Password | wp-admin → Users → Profile → Application Passwords |
| Yêu cầu | Solid Security: bật **Application Passwords** cho nhóm Administrators; REST API để **Default Access** |

### Biến môi trường cần có
```
WP_SITE=https://danangmobile.com
WP_USER=aiquantri
WP_APP_PASSWORD=<application password, dạng "xxxx xxxx xxxx xxxx xxxx xxxx">
```

## 3. API đang dùng
- **WordPress core:** `/wp-json/wp/v2/` → posts, pages, categories, tags, media,
  menus, menu-items, menu-locations, users, product_cat, search, plugins.
- **WooCommerce:** `/wp-json/wc/v3/` → products, products/{id}/variations
  (Application Password của admin dùng được cho cả wc/v3).

## 4. Công cụ trong repo (`seo-tools/`)
| File | Chức năng |
|---|---|
| `publish_wp.py` | Đăng/sửa bài từ file Markdown (front matter + HTML) lên WP. |
| `add_images.py` | Upload ảnh lên Media, gán featured + chèn `<figure>` vào bài. |
| `rebuild_menu.py` | Dựng lại Main Menu (67 mục) từ snapshot. |
| `menu-backup-29.md` | Snapshot cấu trúc Main Menu (phòng khi mất menu). |
| `menu-icons/` | 8 icon menu (SVG + PNG trắng) cho 8 mục cấp 1. |
| `landing/` | Bản lưu HTML các trang landing (pillar). |
| `articles/` | Các bài viết Markdown đã/đang đăng. |
| `ke-hoach-seo-thay-pin.md` | Lộ trình cụm 15 bài SEO "thay pin iPhone Đà Nẵng". |
| `.env` | Khoá thật (KHÔNG commit). Mẫu: `.env.example`. |

### Lệnh thường dùng
```bash
cd seo-tools
python3 publish_wp.py --check                         # kiểm tra kết nối
python3 publish_wp.py articles/bai.md --publish        # đăng public
python3 publish_wp.py articles/ --dry-run              # xem trước, không gọi mạng
```

## 5. Khôi phục kết nối ở phiên sau
Môi trường cloud là **ephemeral** (container bị xoá khi hết phiên) nên `.env`
sẽ mất. Để Claude tự kết nối lại, đặt 3 biến môi trường ở **cấu hình môi
trường của Claude Code on the web** (Environment variables / Secrets):
`WP_SITE`, `WP_USER`, `WP_APP_PASSWORD`.
Tham khảo: https://code.claude.com/docs/en/claude-code-on-the-web

Khi đã có biến môi trường, mỗi phiên chỉ cần chạy `python3 publish_wp.py --check`
là kết nối ngay, không cần nhập lại.

## 6. Hiện trạng đã cấu hình trên site (tham chiếu nhanh)
- **Chuyên mục:** `Cowork` (id 728) – gom nội dung do aiquantri đăng; `Mẹo vặt` (543).
- **Menu chính:** "Main Menu" (id 701) gán location `primary`, 8 mục cấp 1 có icon.
  Top bar: menu id 30 gán `top_bar_nav`.
- **Trang landing (Page):**
  - `/dich-vu-thay-pin-iphone-da-nang/` (id 10492) – pillar thay pin (bảng giá + FAQ + schema).
  - `/tat-ca-iphone/` (id 10489) – liệt kê sản phẩm iPhone (mục menu iPhone trỏ vào).
- **Sản phẩm đã chỉnh giá (WooCommerce):**
  - iPhone 17 Pro Max 256GB: id 9685, 8873 → 34.499.000đ
  - iPhone 17 Pro Max 512GB: id 9129, 8987 → 40.299.000đ
- **Lưu ý kỹ thuật:** một số URL danh mục (`/iphone/`, `/thay-pin-iphone/`,
  `/macbook/`…) đang bị **redirect 301 trong Rank Math** → cần xoá thủ công
  trong Rank Math → Redirections (API không xoá được).
