from pathlib import Path
import pypdfium2 as pdf
root=Path(__file__).resolve().parent/'company_background_render'
d=pdf.PdfDocument(str(root/'report.pdf'))
for i,page in enumerate(d):
    page.render(scale=1.6).to_pil().save(root/f'page-{i+1:02d}.png')
    text=page.get_textpage().get_text_range()
    (root/f'page-{i+1:02d}.txt').write_text(text,encoding='utf-8')
    print(i+1,text[:80].replace('\r',' ').replace('\n',' '))
print('Pages:',len(d))
