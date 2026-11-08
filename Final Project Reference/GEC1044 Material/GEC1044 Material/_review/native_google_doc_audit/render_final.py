from pathlib import Path
import json
import pypdfium2 as pdfium

source = Path(r'C:\Users\lukel\AppData\Local\Temp\browser-use\exports\GEC1044 Field Trip Report-bb02c26e-077a-44e6-a40a-8d17116ca8ab.pdf')
output = Path(__file__).parent
pdf = pdfium.PdfDocument(str(source))
pages = []
for i in range(len(pdf)):
    page = pdf[i]
    textpage = page.get_textpage()
    text = textpage.get_text_range()
    (output / f'final-page-{i+1:02d}.txt').write_text(text, encoding='utf-8')
    page.render(scale=1.6).to_pil().save(output / f'final-page-{i+1:02d}.png')
    pages.append({'page':i+1, 'characters':len(text.strip()), 'start':text[:110].replace('\r\n',' '), 'end':text[-90:].replace('\r\n',' ')})
    textpage.close()
    page.close()
print(json.dumps({'count':len(pdf), 'pages':pages}, ensure_ascii=False))
pdf.close()
