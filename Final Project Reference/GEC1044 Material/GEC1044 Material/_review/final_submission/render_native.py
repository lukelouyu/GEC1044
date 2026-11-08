from pathlib import Path
import pypdfium2 as pdfium, json
root = Path(__file__).parent
doc = pdfium.PdfDocument(str(root / 'revised-native.pdf'))
out = root / 'pages'
out.mkdir(exist_ok=True)
summary = []
for i in range(len(doc)):
    page = doc[i]
    page.render(scale=1.25).to_pil().save(out / f'page-{i+1:02}.png')
    tp = page.get_textpage()
    text = tp.get_text_range()
    (out / f'page-{i+1:02}.txt').write_text(text,encoding='utf8')
    summary.append({'page':i+1,'start':text[:100],'end':text[-140:],'chars':len(text)})
    tp.close()
    page.close()
(root / 'page-summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps(summary,ensure_ascii=True))
