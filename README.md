# nguyenvanman.com — source code

Repo này tách biệt rõ ràng từng trang. **Khi sửa trang nào chỉ chạm vào đúng file của trang đó. Tuyệt đối không sửa chéo.**

## Cấu trúc trang

| URL | File trong repo | Trạng thái |
| --- | --- | --- |
| `nguyenvanman.com/` | `index.html` | ✅ có |
| `nguyenvanman.com/dich-vu.html` | `dich-vu.html` | ✅ có |
| `nguyenvanman.com/san-pham.html` | `san-pham.html` | ❌ **THIẾU** |
| `nguyenvanman.com/cafe` | `cafe/index.html` | ✅ có |
| `nguyenvanman.com/shipper` | `shipper/index.html` | ✅ có |

## Tài nguyên dùng chung (THIẾU trong repo, chỉ có ở máy local)

Các file sau là một phần của deployment thật trên Vercel, chưa được commit vào repo. Cần owner upload từ máy gốc trước khi deploy:

### Ảnh dùng chung (root)
- `logo-man.png` — favicon + logo header/footer của index, dich-vu, san-pham
- `logo-man.svg` — fallback nếu PNG lỗi
- `hero-man.png` + `hero-man.svg` — ảnh chân dung trang chủ
- `shoptao-team.jpg` — ảnh team trang chủ
- `story-man.jpg` — ảnh câu chuyện trang chủ
- `og-image.png` — Open Graph share image trang chủ
- `shipper-og.png` — Open Graph share image trang shipper

### CSS/JS dùng chung
- `styles.css` — stylesheet chính của index, dich-vu, san-pham
- `script.js` — JS chính của các trang trên

### Ảnh riêng của từng trang
- `cafe/logo.jpg` — avatar trang /cafe
- `shipper/shipper-hero.png` — ảnh hero trang /shipper

### Serverless function
- `api/submit.js` (hoặc tương đương) — endpoint xử lý form upload ảnh shipper

## Quy tắc khi sửa

| Yêu cầu sửa             | Chỉ được sửa file              |
| ----------------------- | ------------------------------ |
| Trang chủ               | `index.html`                   |
| Trang dịch vụ           | `dich-vu.html`                 |
| Trang sản phẩm          | `san-pham.html`                |
| Trang `/cafe`           | `cafe/index.html`              |
| Trang `/shipper`        | `shipper/index.html`           |

CSS/JS dùng chung (`styles.css`, `script.js`) ảnh hưởng tới **index + dich-vu + san-pham**, sửa cẩn thận.

## Quy trình deploy an toàn

1. Owner push **toàn bộ source gốc** từ máy (gồm các file ✅ và ❌ ở trên) lên branch `main` của repo này.
2. Vercel project được kết nối Git với repo → mọi push lên `main` tự deploy.
3. Khi cần sửa: Claude edit file trên branch riêng, mở PR, preview, merge vào `main` → auto-deploy.
