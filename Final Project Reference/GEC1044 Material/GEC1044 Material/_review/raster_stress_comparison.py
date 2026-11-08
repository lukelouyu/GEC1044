from pathlib import Path
import pypdfium2 as pdf

folder = Path(__file__).resolve().parent / 'stress_comparison_render'
doc = pdf.PdfDocument(str(folder / 'report.pdf'))
for i, page in enumerate(doc):
    page.render(scale=1.6).to_pil().save(folder / f'page-{i+1:02d}.png')
    text = page.get_textpage().get_text_range()
    print(i+1, text[:75].replace('\r',' ').replace('\n',' '))
print('Pages:', len(doc))

