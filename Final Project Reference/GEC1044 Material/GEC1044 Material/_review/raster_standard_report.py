from pathlib import Path
import pypdfium2 as pdf

folder=Path(__file__).resolve().parent/'standard_report_verified_render'
doc=pdf.PdfDocument(str(folder/'report.pdf'))
for i,page in enumerate(doc):
    page.render(scale=1.6).to_pil().save(folder/f'page-{i+1:02d}.png')
    content=page.get_textpage().get_text_range()
    (folder/f'page-{i+1:02d}.txt').write_text(content,encoding='utf-8')
    print(i+1,content[:90].replace('\r',' ').replace('\n',' '))
print('Pages:',len(doc))
