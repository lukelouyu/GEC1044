from pathlib import Path
import json
import pypdfium2 as pdfium

source = Path(r'C:\Users\lukel\AppData\Local\Temp\browser-use\exports\GEC1044 Field Trip Report-1eda56bf-513e-44e9-9b60-f7824b309095.pdf')
out = Path(__file__).parent / 'final_concise'
out.mkdir(exist_ok=True)
pdf = pdfium.PdfDocument(str(source))
summary = []
for i in range(len(pdf)):
    page = pdf[i]
    tp = page.get_textpage()
    text = tp.get_text_range()
    (out / f'page-{i+1:02d}.txt').write_text(text, encoding='utf-8')
    page.render(scale=1.6).to_pil().save(out / f'page-{i+1:02d}.png')
    summary.append({'page': i+1, 'characters': len(text.strip()), 'start': text[:130], 'end': text[-100:]})
    tp.close()
    page.close()
print(json.dumps(summary, ensure_ascii=True))
pdf.close()
