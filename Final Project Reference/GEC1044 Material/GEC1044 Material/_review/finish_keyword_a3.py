from docx import Document
from pathlib import Path

f = Path(__file__).resolve().parents[1] / 'GEC1044_Tong_Keow_First_Draft.docx'
d = Document(f)
for p in d.paragraphs:
    for r in p.runs:
        old = r.text
        new = old.replace('HSA, 2025, section 5', 'HSA, 2025a, section 5')
        new = new.replace('Secondary evidence from HSA lists', 'Secondary evidence from the Health Sciences Authority (HSA) lists')
        new = new.replace('while product-level local processing remains unverified.', 'while the soup packs’ local processing remains unverified.')
        new = new.replace('The supplementary photograph identifies a Nature’s Green product labelled “Made in Singapore”, but does not establish its factory, complete formula or whether it was the exact preparation intended in the interview.', 'HSA corroborates Singapore manufacture of the pictured Nature’s Green capsules; the ingredient origins and whether this was the preparation intended in the interview remain unverified.')
        if new != old:
            r.text = new
    if p.text.startswith('A4 Five soup therapies'):
        previous = p._p.getprevious()
        # Remove the empty manual page-break paragraph between A3 and A4.
        if previous.tag.endswith('}p') and not ''.join(previous.itertext()).strip():
            previous.getparent().remove(previous)
        elif previous.tag.endswith('}p') and not previous.xpath('.//w:t') and not previous.xpath('.//w:drawing'):
            previous.getparent().remove(previous)
d.save(f)
assert len(Document(f).inline_shapes) == 36
print('Updated dependent wording and removed empty paragraph before A4.')
