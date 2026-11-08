from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).parent
files = sorted(root.glob('page-*.png'))
thumb_width, thumb_height = 255, 385
sheet = Image.new('RGB', (thumb_width * 4, thumb_height * ((len(files)+3)//4)), '#dddddd')
draw = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert('RGB')
    im.thumbnail((245, 350))
    x, y = (i % 4) * thumb_width, (i // 4) * thumb_height
    sheet.paste(im, (x + 5, y + 25))
    draw.text((x+8, y+5), f.stem, fill='black')
sheet.save(root / 'contact-sheet.png')
print(len(files), 'pages')
