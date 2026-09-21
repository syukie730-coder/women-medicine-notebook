"""画像なしなら仮アイコンを作成。画像を渡すと縮小して差し替える。"""
from pathlib import Path
import sys, re
from PIL import Image, ImageOps, ImageDraw
root = Path(__file__).resolve().parents[1]
dist = root / 'dist'
if len(sys.argv) > 1:
    with Image.open(sys.argv[1]) as original:
        source = ImageOps.exif_transpose(original).convert('RGBA')
        source.thumbnail((512, 512), Image.Resampling.LANCZOS)
        icon = Image.new('RGBA', (512, 512), '#fff0f6')
        icon.alpha_composite(source, ((512-source.width)//2, (512-source.height)//2))
        icon = icon.convert('RGB')
else:
    icon = Image.new('RGB', (512, 512), '#fff0f6')
    d = ImageDraw.Draw(icon)
    d.rounded_rectangle((105, 66, 407, 446), radius=38, fill='#a83f68')
    d.rounded_rectangle((137, 86, 387, 426), radius=24, fill='#fffafb')
    d.line((162, 95, 162, 418), fill='#eac1d2', width=8)
    d.rounded_rectangle((197, 151, 341, 239), radius=44, fill='#eeb5cd', outline='#a83f68', width=7)
    d.line((269, 155, 269, 236), fill='#a83f68', width=6)
    for y in (292, 332, 372):
        d.rounded_rectangle((200, y, 337, y+9), radius=4, fill='#d9a0b7')
# 画面用は144px、ホーム画面用は各端末に必要なサイズ。
icon.resize((144,144),Image.Resampling.LANCZOS).save(dist/'assets/app-icon.webp','WEBP',quality=84,method=6)
for size, target in [(180,'apple-touch-icon.png'),(192,'assets/icon-192.png'),(512,'assets/icon-512.png')]:
    icon.resize((size,size),Image.Resampling.LANCZOS).quantize(colors=128).save(dist/target,'PNG',optimize=True)
# 画像差し替え時に古い画像が残らないようキャッシュ番号も更新。
if len(sys.argv) > 1:
    sw=dist/'sw.js'; text=sw.read_text()
    current=int(re.search(r'women-medicine-notebook-v(\d+)', text).group(1))
    new=current+1
    sw.write_text(text.replace(f'women-medicine-notebook-v{current}',f'women-medicine-notebook-v{new}').replace(f'png?v={current}',f'png?v={new}'))
    html=dist/'index.html';html.write_text(html.read_text().replace(f'png?v={current}',f'png?v={new}'))
for p in [dist/'assets/app-icon.webp',dist/'apple-touch-icon.png',dist/'assets/icon-192.png',dist/'assets/icon-512.png']:
    print(p.name, p.stat().st_size, 'bytes')
