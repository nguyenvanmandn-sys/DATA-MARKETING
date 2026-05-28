# nguyenvanman.com — source code 3 trang

Repo này tách biệt rõ ràng 3 trang web độc lập. **Khi sửa trang nào chỉ chạm vào thư mục/file của trang đó. Tuyệt đối không sửa chéo.**

## Cấu trúc thư mục

```
/
├── index.html              ← Trang chủ:        nguyenvanman.com
├── cafe/
│   └── index.html          ← Trang cà phê:     nguyenvanman.com/cafe
└── shipper/
    └── index.html          ← Trang shipper:    nguyenvanman.com/shipper
```

## Quy tắc khi sửa

| Yêu cầu sửa             | Chỉ được sửa file        |
| ----------------------- | ------------------------ |
| Trang chủ               | `index.html`             |
| Trang `/cafe`           | `cafe/index.html`        |
| Trang `/shipper`        | `shipper/index.html`     |

## Tài nguyên đi kèm (KHÔNG có trong repo này, nằm ở máy local của owner)

Các file sau là một phần của deployment thật trên Vercel nhưng chưa được commit vào repo (giữ ở máy gốc, sẽ kèm khi `vercel --prod`):

- `logo-man.png` (favicon dùng chung — cả 3 trang reference qua `../logo-man.png` hoặc `/logo-man.png`)
- `hero-man.png`, `shoptao-team.jpg`, `story-man.jpg` (trang chủ)
- `cafe/logo.jpg` (avatar trang /cafe)
- `shipper/shipper-hero.png`, `shipper-og.png` (trang /shipper)
- `/api/submit` (serverless function xử lý form shipper)

## Quy trình deploy an toàn

1. Claude sửa file trong repo theo yêu cầu.
2. Owner pull/copy file đã sửa về máy local (nơi có đầy đủ assets + `/api`).
3. Owner chạy `vercel --prod` từ máy local để deploy toàn bộ site.

Cách này đảm bảo:
- Đúng 1 trang bị thay đổi, 2 trang còn lại giữ nguyên bit-for-bit.
- API và mọi asset gốc không bị mất.
