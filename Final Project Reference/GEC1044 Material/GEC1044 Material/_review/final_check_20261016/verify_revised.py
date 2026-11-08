from pathlib import Path
import json
import sys
import pypdfium2 as pdfium
from pypdf import PdfReader
from PIL import Image, ImageOps, ImageDraw

sys.stdout.reconfigure(encoding='utf-8')

root = Path(__file__).parent
source = root / 'revised-report.pdf'
reader = PdfReader(source)
texts = [p.extract_text() or '' for p in reader.pages]
(root / 'revised-pages.json').write_text(json.dumps(texts, ensure_ascii=False, indent=2), encoding='utf-8')
pdf = pdfium.PdfDocument(source)
thumbs = []
for i, text in enumerate(texts):
    page = pdf[i]
    im = page.render(scale=1400/page.get_width()).to_pil().convert('RGB')
    im.save(root / f'revised-page-{i+1:02}.png')
    thumb = ImageOps.contain(im, (260, 370))
    tile = Image.new('RGB', (280, 402), 'white')
    tile.paste(thumb, ((280-thumb.width)//2, 25))
    ImageDraw.Draw(tile).text((10, 6), f'Page {i+1}', fill='black')
    thumbs.append(tile)
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    print(json.dumps({'page':i+1, 'characters':len(text), 'start':lines[:3], 'end':lines[-2:]}, ensure_ascii=False))
sheet = Image.new('RGB', (280*5, 402*((len(thumbs)+4)//5)), '#dddddd')
for i, thumb in enumerate(thumbs):
    sheet.paste(thumb, ((i%5)*280, (i//5)*402))
sheet.save(root / 'revised-contact-sheet.png')
print(f'Pages: {len(texts)}')
