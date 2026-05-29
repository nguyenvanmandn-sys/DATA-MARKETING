# Bộ công cụ đăng bài SEO lên WordPress (danangmobile.com)

Cho phép Claude (và bạn) viết bài SEO rồi đăng thẳng lên WordPress qua REST API.
Script chỉ dùng thư viện chuẩn của Python — **không cần `pip install`**.

## Cần làm 1 lần để kết nối

### 1. Mở mạng tới website
Môi trường Claude Code trên web chặn mạng theo allowlist. Nếu gặp lỗi
`Host not in allowlist`, cần thêm `danangmobile.com` vào **Network access** của
môi trường. Xem: https://code.claude.com/docs/en/claude-code-on-the-web

### 2. Tạo Application Password trong WordPress
1. Đăng nhập `https://danangmobile.com/wp-admin/`
2. Vào **Users → Profile** (Thành viên → Hồ sơ cá nhân)
3. Kéo xuống mục **Application Passwords**
4. Nhập tên ứng dụng, ví dụ `claude-seo`, bấm **Add New Application Password**
5. Copy chuỗi mật khẩu hiện ra (dạng `xxxx xxxx xxxx xxxx xxxx xxxx`)

> Đây là khóa riêng, không phải mật khẩu đăng nhập chính. Có thể thu hồi bất cứ
> lúc nào trong cùng trang đó.

### 3. Khai báo biến môi trường
Sao chép `.env.example` thành `.env` rồi điền `WP_SITE`, `WP_USER`,
`WP_APP_PASSWORD`. File `.env` đã được `.gitignore` bỏ qua nên không bị commit.

## Cách dùng

```bash
cd seo-tools

# Kiểm tra kết nối + quyền tài khoản
python3 publish_wp.py --check

# Xem trước nội dung mà KHÔNG gọi mạng
python3 publish_wp.py articles/cach-chon-mua-iphone-cu-da-nang.md --dry-run

# Đăng dạng NHÁP (mặc định) để duyệt trong wp-admin
python3 publish_wp.py articles/cach-chon-mua-iphone-cu-da-nang.md

# Đăng PUBLIC ngay
python3 publish_wp.py articles/cach-chon-mua-iphone-cu-da-nang.md --publish

# Đăng HÀNG LOẠT: truyền nhiều file, hoặc cả thư mục
python3 publish_wp.py articles/                      # tất cả bài trong thư mục (nháp)
python3 publish_wp.py articles/a.md articles/b.md    # vài bài cụ thể
```

## Các bài SEO đã viết sẵn (đăng dạng nháp)

| File | Chủ đề |
|---|---|
| `cach-chon-mua-iphone-cu-da-nang.md` | Kinh nghiệm mua iPhone cũ |
| `thay-pin-iphone-da-nang.md` | Dịch vụ thay pin iPhone |
| `thay-man-hinh-iphone-da-nang.md` | Dịch vụ thay màn hình iPhone |
| `phan-biet-iphone-chinh-hang-va-hang-dung.md` | Phân biệt máy thật / máy dựng |
| `mua-iphone-tra-gop-da-nang.md` | Mua iPhone trả góp |
| `sua-macbook-da-nang.md` | Dịch vụ sửa MacBook |

## Viết bài mới

Tạo file `articles/ten-bai.md` theo mẫu: phần **front matter** giữa hai dòng
`---`, sau đó là **thân bài HTML**.

```
---
title: Tiêu đề bài viết (chứa từ khóa chính)
slug: duong-dan-than-thien-seo
status: draft
excerpt: Mô tả meta 150-160 ký tự, chứa từ khóa, hấp dẫn người đọc.
categories: Tên chuyên mục
tags: từ khóa 1, từ khóa 2
---
<p>Mở bài...</p>
<h2>Tiêu đề phụ H2 chứa từ khóa</h2>
<p>Nội dung...</p>
```

Quy ước SEO khi viết:
- 1 từ khóa chính, xuất hiện ở title, đoạn mở đầu, ít nhất 1 thẻ H2.
- Mô tả meta (`excerpt`) 150–160 ký tự.
- Dùng H2/H3 phân tầng rõ ràng, đoạn ngắn, có danh sách (ul/ol).
- Đăng `draft` để duyệt trước khi public.
