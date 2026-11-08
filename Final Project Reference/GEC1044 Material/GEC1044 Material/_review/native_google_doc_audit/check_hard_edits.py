from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import json
import pypdfium2 as pdfium

folder = Path(__file__).parent / 'hard_edits'
folder.mkdir(exist_ok=True)
source_pdf = Path(r'C:\Users\lukel\AppData\Local\Temp\browser-use\exports\GEC1044 Field Trip Report-d820f2a1-8114-4ea7-be86-0a33c5f4b371.pdf')
source_docx = Path(r'C:\Users\lukel\AppData\Local\Temp\browser-use\exports\GEC1044 Field Trip Report-e5ec2b89-29f8-48f2-afe4-42460334f514.docx')
pdf = pdfium.PdfDocument(str(source_pdf))
pages=[]
for i in range(len(pdf)):
    page=pdf[i]
    tp=page.get_textpage()
    text=tp.get_text_range()
    (folder/f'page-{i+1:02d}.txt').write_text(text,encoding='utf-8')
    page.render(scale=1.6).to_pil().save(folder/f'page-{i+1:02d}.png')
    pages.append({'page':i+1,'characters':len(text.strip())})
    tp.close()
    page.close()
pdf.close()
with ZipFile(source_docx) as z:
    root=ET.fromstring(z.read('word/document.xml'))
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
paras=[''.join(p.itertext()) for p in []]
paras=[''.join(t.text or '' for t in p.findall('.//w:t',ns)) for p in root.findall('.//w:p',ns)]
content='\n'.join(paras)
tables=[]
for table in root.findall('.//w:body/w:tbl',ns):
    rows=table.findall('w:tr',ns)
    tables.append({'rows':len(rows),'first_column':[''.join(t.text or '' for t in r.find('w:tc',ns).findall('.//w:t',ns)) for r in rows]})
report={'pdf_pages':pages,'docx_headings':{s:sum(p==s for p in paras) for s in ['4.2 Comparative industry examples','4.3 Products for daily pressures','8 Limitations']},'colds_sentence_count':content.count('These are reference descriptors for comparison with the broad complaint “colds”.'),'garbled_product_name':content.count('产品名称'),'bpleurum':content.count('bpleurum'),'liquorice':content.count('liquorice'),'tables':tables}
(folder/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
