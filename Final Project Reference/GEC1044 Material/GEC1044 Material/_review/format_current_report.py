from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile
import hashlib
import json
import shutil

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'GEC1044_Tong_Keow_Final_Polish.docx'
BACKUP = ROOT / '_review' / 'Final_Polish_before_standard_format.bak'

def media_hashes(path):
    with ZipFile(path) as z:
        return {n: hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}

source_hash = hashlib.sha256(TARGET.read_bytes()).hexdigest()
before_media = media_hashes(TARGET)
doc = Document(TARGET)
original = [p.text for p in doc.paragraphs]
original_tables = [[ [c.text for c in r.cells] for r in t.rows] for t in doc.tables]
before_shapes = len(doc.inline_shapes)
changes = []

def replace(p, old, new):
    full = ''.join(r.text for r in p.runs)
    assert p.text == full, 'Paragraph contains an unhandled hyperlink or field.'
    start = full.find(old)
    assert start >= 0, old
    end = start + len(old)
    offset = 0
    inserted = False
    for r in p.runs:
        txt = r.text
        a, b = offset, offset + len(txt)
        offset = b
        if b <= start or a >= end:
            continue
        left = txt[:max(0, start-a)]
        right = txt[max(0, end-a):] if b > end else ''
        r.text = left + (new if not inserted else '') + right
        inserted = True
    changes.append({'before': old, 'after': new})

# Only grammar, a missing abbreviation expansion, and current cross-references.
replace(doc.paragraphs[6], 'work-hours discussion', 'workplace-stress discussion')
replace(doc.paragraphs[37], 'public-relation accounts', 'public-relations accounts')
replace(doc.paragraphs[39], 'daily pressures such as late nights, long work hours, and prolonged phone use—with the demand', 'daily pressures, such as late nights, long work hours and prolonged phone use, with demand')
replace(doc.paragraphs[40], 'Comparative surveys', 'A comparative survey')
replace(doc.paragraphs[40], 'gives 68% of Singapore workers experiencing', 'reports that 68% of Singapore workers experience')
replace(doc.paragraphs[47], 'HSA requires', 'The Health Sciences Authority (HSA) requires')
replace(doc.paragraphs[50], 'From these practice, it will attract younger customer by assuring the quality of the medical product and address their concern on potential side effect.', 'These practices will attract younger customers by reassuring them about product quality and addressing their concerns about potential side effects.')
replace(doc.paragraphs[56], "Lecture’s contrast", "Lecture 5’s contrast")
replace(doc.tables[-1].rows[5].cells[2].paragraphs[0], 'A5; Section 4.3', 'A5; Section 4.4')

# Preserve all latest content; correct the four paragraphs mistakenly marked as headings.
for i in (35, 60, 61, 62):
    doc.paragraphs[i].style = doc.styles['Normal']

def font_run(r, size=None):
    r.font.name = 'Times New Roman'
    if size is not None:
        r.font.size = Pt(size)
    r.font.color.rgb = RGBColor(0, 0, 0)
    rf = r._element.get_or_add_rPr().get_or_add_rFonts()
    rf.set(qn('w:eastAsia'), 'Microsoft YaHei')
    for attr in ('asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme'):
        rf.attrib.pop(qn('w:' + attr), None)

for name, size in [('Normal',12), ('Title',24), ('Subtitle',13), ('Heading 1',15), ('Heading 2',12), ('Caption',10.5)]:
    s = doc.styles[name]
    s.font.name = 'Times New Roman'
    s.font.size = Pt(size)
    s.font.color.rgb = RGBColor(0,0,0)
    rf = s.element.get_or_add_rPr().get_or_add_rFonts()
    rf.set(qn('w:eastAsia'), 'Microsoft YaHei')
    for attr in ('asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme'):
        rf.attrib.pop(qn('w:'+attr),None)
    pf = s.paragraph_format
    pf.widow_control = True
    pf.keep_together = False
    if name == 'Normal':
        pf.line_spacing = 1.15
        pf.space_before = Pt(0)
        pf.space_after = Pt(6)
        pf.keep_with_next = False
    elif name.startswith('Heading'):
        s.font.bold = True
        pf.line_spacing = 1.0
        pf.space_before = Pt(14 if name == 'Heading 1' else 10)
        pf.space_after = Pt(6)
        pf.keep_with_next = True
        pf.keep_together = True
    elif name in ('Title','Subtitle'):
        pf.line_spacing = 1.0
        pf.keep_with_next = True
        pf.space_after = Pt(9)
    else:
        pf.line_spacing = 1.0
        pf.space_before = Pt(6)
        pf.space_after = Pt(6)
        pf.keep_with_next = True

for p in doc.paragraphs:
    pf = p.paragraph_format
    pf.widow_control = True
    if p.style.name in ('Normal','Heading 1','Heading 2','Title','Subtitle','Caption'):
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        # Remove paragraph borders from title and other inherited decorative formatting.
        for border in p._p.xpath('./w:pPr/w:pBdr'):
            border.getparent().remove(border)
    if p.style.name == 'Normal' and p.text:
        pf.keep_with_next = False
        pf.keep_together = False
        pf.line_spacing = 1.15
        pf.space_before = Pt(0)
        pf.space_after = Pt(6)
        pf.left_indent = Inches(0)
        pf.right_indent = Inches(0)
        pf.first_line_indent = Inches(0)
    for r in p.runs:
        font_run(r, 12 if p.style.name == 'Normal' else None)

# Retain the original title block and metadata, rather than add a new cover or contents page.
for p in doc.paragraphs[2:5]:
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    for r in p.runs:
        font_run(r, 11)

# Captions, notes and photographic pages remain attached to their respective objects.
for p in doc.paragraphs:
    if p.text.startswith('Table A'):
        p.style = doc.styles['Caption']
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.keep_together = True
        for r in p.runs:
            font_run(r,10.5)
    elif p.text.startswith('Note.'):
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = False
        for r in p.runs:
            font_run(r,10.5)
    elif p.text.startswith('Figure '):
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.space_after = Pt(4)
        for r in p.runs:
            font_run(r,11)
            r.bold = True
    elif p._p.xpath('.//w:drawing'):
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.keep_together = True

for i in (155,160,165):
    p = doc.paragraphs[i]
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_after = Pt(6)
    for r in p.runs:
        font_run(r,11)

# The newly cited survey must have a matching, consistently formatted bibliography entry.
ref_anchor = next(p for p in doc.paragraphs if p.text.startswith('Lim, M. K.'))
new_ref = OxmlElement('w:p')
ref_anchor._p.addprevious(new_ref)
ref = Paragraph(new_ref, ref_anchor._parent)
ref.style = doc.styles['Normal']
ref.add_run('Kumari, J. (2024, January 24). ')
ref.add_run('68% of Singapore workers experience weekly stress at the workplace: Survey.').italic = True
ref.add_run(' People Matters. https://sea.peoplemattersglobal.com/news/organisational-culture/68-of-singapore-workers-experience-weekly-stress-at-the-workplace-survey-40095')
changes.append({'added_reference': ref.text})

in_refs = False
for p in doc.paragraphs:
    if p.text == 'References':
        in_refs = True
        p.paragraph_format.page_break_before = True
        continue
    if p.text.startswith('Appendix B'):
        in_refs = False
    if in_refs and p.text:
        pf = p.paragraph_format
        pf.line_spacing = 2.0
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.left_indent = Inches(.5)
        pf.first_line_indent = Inches(-.5)
        pf.keep_together = True
        pf.keep_with_next = False
        pf.page_break_before = False
        for r in p.runs:
            font_run(r,12)

# Preserve table columns and all pictures; regularise typography, padding and continuation headers.
for t in doc.tables:
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    pr = t._tbl.tblPr
    borders = pr.find(qn('w:tblBorders'))
    if borders is None:
        borders = OxmlElement('w:tblBorders'); pr.append(borders)
    for name in ('top','left','bottom','right','insideH','insideV'):
        edge = borders.find(qn('w:'+name))
        if edge is None:
            edge = OxmlElement('w:'+name); borders.append(edge)
        for key,val in [('val','single'),('sz','5'),('color','D9D9D9')]:
            edge.set(qn('w:'+key),val)
    for ri,row in enumerate(t.rows):
        row.height = None
        trpr = row._tr.get_or_add_trPr()
        if ri == 0:
            hdr = trpr.find(qn('w:tblHeader'))
            if hdr is None:
                hdr = OxmlElement('w:tblHeader'); trpr.append(hdr)
            hdr.set(qn('w:val'),'true')
        cant = trpr.find(qn('w:cantSplit'))
        if cant is None:
            cant = OxmlElement('w:cantSplit'); trpr.append(cant)
        for ci,cell in enumerate(row.cells):
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            cp = cell._tc.get_or_add_tcPr()
            margin = cp.find(qn('w:tcMar'))
            if margin is None:
                margin = OxmlElement('w:tcMar'); cp.append(margin)
            for side,val in [('top','95'),('bottom','95'),('left','90'),('right','90')]:
                m = margin.find(qn('w:'+side))
                if m is None:
                    m = OxmlElement('w:'+side); margin.append(m)
                m.set(qn('w:w'),val); m.set(qn('w:type'),'dxa')
            if ri == 0:
                shade = cp.find(qn('w:shd'))
                if shade is None:
                    shade = OxmlElement('w:shd'); cp.append(shade)
                shade.set(qn('w:fill'),'EDEDED')
            for p in cell.paragraphs:
                pf = p.paragraph_format
                pf.line_spacing = 1.0
                pf.space_before = Pt(0)
                pf.space_after = Pt(3)
                pf.keep_with_next = False
                pf.keep_together = False
                pf.widow_control = True
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ri == 0 or ci == 0 else WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    font_run(r,10.5)
                    if ri == 0:
                        r.bold = True

for s in doc.sections:
    for part in (s.header,s.footer):
        for p in part.paragraphs:
            p.paragraph_format.line_spacing = 1.0
            for r in p.runs:
                font_run(r,9)

# Drop incidental empty paragraphs; retain explicit page breaks and objects.
for p in list(doc.paragraphs):
    if not p.text.strip() and not p._p.xpath('.//w:br | .//w:drawing | .//w:fldChar'):
        p._element.getparent().remove(p._element)

assert len(doc.inline_shapes) == before_shapes
assert len(doc.tables) == len(original_tables)
for ti,t in enumerate(doc.tables):
    for ri,row in enumerate(t.rows):
        for ci,c in enumerate(row.cells):
            expected = original_tables[ti][ri][ci]
            if (ti,ri,ci) == (6,5,2):
                expected = expected.replace('A5; Section 4.3','A5; Section 4.4')
            assert c.text == expected, (ti,ri,ci)

assert hashlib.sha256(TARGET.read_bytes()).hexdigest() == source_hash, 'Source changed during formatting.'
if not BACKUP.exists():
    shutil.copyfile(TARGET,BACKUP)
doc.save(TARGET)
assert before_media == media_hashes(TARGET), 'Picture binaries changed.'
check = Document(TARGET)
assert all(p.style.name == 'Normal' for p in check.paragraphs if p.text.startswith(('Soup packs make this demand','The themes form a connected','The mixed shop gives','Unschuld\'s (2018) account')))
audit = {'source':str(TARGET),'backup':str(BACKUP),'text_changes':changes,'tables_preserved':len(doc.tables),'inline_pictures_preserved':before_shapes,'media_unchanged':True,'original_paragraph_count':len(original),'final_paragraph_count':len(check.paragraphs)}
(ROOT/'_review'/'standard_report_format_checks.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False,indent=2))
