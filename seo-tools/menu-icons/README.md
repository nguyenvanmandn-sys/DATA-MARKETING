# Icon menu (Main Menu) — danangmobile.com

8 icon cho 8 mục cấp 1 của Main Menu. Bản gốc dùng `stroke="currentColor"`.

## Cách đã áp dụng
- SVG bị Cloudflare/bảo mật chặn upload → chuyển sang **PNG trắng nền trong suốt**
  (48px) bằng cairosvg, upload lên Media, rồi chèn `<img>` vào **tiêu đề** từng
  menu item cấp 1 (admin có quyền unfiltered_html nên `<img>` được giữ).
- Map: 01→iPhone, 02→MacBook, 03→Apple Watch, 04→iPad, 05→Phụ kiện,
  06→Sửa chữa, 07→Sửa iPhone & MacBook, 08→Tin tức & Sự kiện.

Tạo lại PNG trắng:
```
for f in *.svg; do sed 's/currentColor/#ffffff/g' "$f" > white-$f; done
python3 -c "import cairosvg,glob,os
for f in glob.glob('white-*.svg'):
    cairosvg.svg2png(url=f, write_to='png/'+os.path.basename(f)[6:-4]+'.png',
                     output_width=48, output_height=48)"
```
