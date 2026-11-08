from pathlib import Path
from pypdf import PdfReader
import pypdfium2 as pdfium
from PIL import Image, ImageOps, ImageDraw
R=Path(__file__).parent
u=r'C:\Users\lukel\Downloads\Traditional Chinese Medicine in Singapore Fieldwork Findings (1).pdf'
p=pdfium.PdfDocument(u)
for i in [3,5]:
    p[i].render(scale=1).to_pil().save(R/f'slide-{i+1}.png')
r=PdfReader(u)
print('SLIDE IMAGE COUNTS',[(i+1,len(pg.images)) for i,pg in enumerate(r.pages)])
imgs=[]
for f in (R.parents[1]/'photo').glob('*.jpg'):
    im=Image.open(f); im.thumbnail((500,380))
    tile=Image.new('RGB',(520,420),'white');tile.paste(im,((520-im.width)//2,0));ImageDraw.Draw(tile).text((10,390),f.name,fill='black');imgs.append(tile)
contact=Image.new('RGB',(1040,420*((len(imgs)+1)//2)),'#eeeeee')
for i,im in enumerate(imgs):contact.paste(im,((i%2)*520,(i//2)*420))
contact.save(R/'photos_contact.png')
