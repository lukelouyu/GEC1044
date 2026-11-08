from pathlib import Path
import pypdfium2 as pdfium
src = Path('C:/Users/lukel/Downloads/GEC1044 Field Trip Report – backup before word-limit edit.pdf')
out = Path(__file__).parent / 'backup_comparison'
out.mkdir(exist_ok=True)
doc = pdfium.PdfDocument(str(src))
texts=[]
for i in range(len(doc)):
    page=doc[i]
    tp=page.get_textpage()
    text=tp.get_text_range()
    texts.append(f'\n--- PAGE {i+1} ---\n{text}')
    (out/f'page-{i+1:02}.txt').write_text(text,encoding='utf-8')
    if i < 12:
        page.render(scale=1.2).to_pil().save(out/f'page-{i+1:02}.png')
    tp.close()
    page.close()
(out/'backup-text.txt').write_text(''.join(texts),encoding='utf-8')
print(f'Extracted {len(doc)} pages')
