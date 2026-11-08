from pathlib import Path
import json
from zipfile import ZipFile
import hashlib
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt

root=Path(__file__).resolve().parent.parent
path=root/'GEC1044_Tong_Keow_Final_Polish.docx'
d=Document(path)
def media(path):
    with ZipFile(path) as z:
        return {n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
original_media=media(path)
before=[p.text for p in d.paragraphs]
for p in d.paragraphs:
    for r in p.runs:
        if 'A comparative survey place this' in r.text:
            r.text=r.text.replace('A comparative survey place this','A comparative survey places this')
    if p.style.name=='Normal' and p.text:
        content=[r for r in p.runs if r.text.strip()]
        if content and all(r.bold is True for r in content):
            for r in content:
                r.bold=False
    if p.text.startswith('Table A'):
        for r in p.runs:
            r.bold=False
    if p.text.startswith(('A2 Eight reported','A5 Three comparatively','A6 Staff-described','A7 Survey coverage')):
        p.paragraph_format.page_break_before=True
    if p.text.startswith('Staff described the six product associations'):
        p.paragraph_format.keep_with_next=True
    # Narrative passages referring to tables remain normal prose, not captions.
    if p.text.startswith(('Table A1 describes ginseng', 'Table A3 separates local cultivation')):
        p.style=d.styles['Normal']
        pf=p.paragraph_format
        pf.line_spacing=1.15
        pf.space_before=Pt(0)
        pf.space_after=Pt(6)
        pf.keep_with_next=False
        pf.keep_together=False
        for r in p.runs:
            r.font.size=Pt(12)
            r.bold=False

# Fit the A3 table and its explanatory note on one page without reducing type size.
for row in d.tables[2].rows:
    for cell in row.cells:
        margin=cell._tc.get_or_add_tcPr().find(qn('w:tcMar'))
        for side in ('top','bottom'):
            margin.find(qn('w:'+side)).set(qn('w:w'),'60')
        for p in cell.paragraphs:
            p.paragraph_format.space_after=Pt(1)

expected=[s.replace('A comparative survey place this','A comparative survey places this') for s in before]
assert [p.text for p in d.paragraphs]==expected
d.save(path)
assert media(path)==original_media
auditpath=root/'_review'/'standard_report_format_checks.json'
audit=json.loads(auditpath.read_text(encoding='utf-8'))
audit['text_changes'].append({'before':'A comparative survey place this','after':'A comparative survey places this'})
audit['final_layout_repairs']=['A3 table-note pairing','A2 and A5–A7 begin on new pages','A6 introduction kept with table','Normal prose and table captions regular weight','Narrative references to tables kept in normal body type']
auditpath.write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print('Final layout repairs saved in the same file; all text and pictures preserved.')
