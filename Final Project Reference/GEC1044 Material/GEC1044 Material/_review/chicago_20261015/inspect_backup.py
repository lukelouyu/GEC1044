from pathlib import Path
from docx import Document

root = Path(__file__).parent
doc = Document(root / 'before-chicago-review.docx')
for i, p in enumerate(doc.paragraphs):
    if p.text.startswith('Figure 4'):
        for j in range(max(0, i-2), i):
            for k, blip in enumerate(doc.paragraphs[j]._p.xpath('.//a:blip')):
                rel = doc.part.rels[blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')]
                target = root / f'figure4-{j}-{k}{Path(str(rel.target_part.partname)).suffix}'
                target.write_bytes(rel.target_part.blob)
                print(target)
