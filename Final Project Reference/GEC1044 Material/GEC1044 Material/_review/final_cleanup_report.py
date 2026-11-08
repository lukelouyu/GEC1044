from pathlib import Path
from copy import deepcopy
import re, json, shutil, hashlib
from zipfile import ZipFile
from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

R=Path(__file__).resolve().parents[1]
F=R/'GEC1044_Tong_Keow_First_Draft.docx'
B=R/'_review/GEC1044_Tong_Keow_before_submission_cleanup.docx'
if not B.exists():shutil.copy2(F,B)
d=Document(B)
def paragraph(prefix):
    matches=[p for p in d.paragraphs if p.text.startswith(prefix)]
    assert len(matches)==1,(prefix,len(matches))
    return matches[0]
def replace(prefix,text):
    p=paragraph(prefix);p.clear();p.add_run(text);return p

replace('In the official June 2025 table,','In the official June 2025 table, Hougang Central subzone has 4,620 residents. Using official rounded age-band totals, approximately 1,070 residents are aged 65 or above, or about 23% of the population. The figures are rounded to the nearest ten; the subzone provides neighbourhood context rather than a measured catchment for the shop (DOS, 2025).')
replace('Comparative industry examples illustrate','These comparative industry examples are promotional or journalistic accounts, not peer-reviewed studies. NYP describes Heng Foh Tong’s redesign of herbal drinks for millennials (Nanyang Polytechnic [NYP], n.d.). Amacha markets TCM-inspired milk teas; a founder interview claims over 150,000 cups sold in eight months, without audited or age-disaggregated data (Amacha, n.d.; Angelynn T., 2026). Teck Soon’s owner reported a 30% sales increase after replacing drawer storage with storefront herb displays in 1982 (Chin, 2024). Eu Yan Sang’s halal category illustrates dietary accessibility, not Tong Keow certification (Eu Yan Sang, n.d.). This is our interpretation: these strategies show deliberate adaptation of access, but do not establish national youth preferences, causes of purchases at our outlet or acceptance of TCM theory.')
replace('WHO defines the four examinations','WHO defines the four examinations 望闻问切 as inspection, listening and smelling, inquiry and palpation; the findings inform pattern differentiation and treatment selection (WHO, 2022). This is our interpretation: the essential distinction is between recognising a complaint and assessing its configuration within an individual. Table A6 records retail associations, without an observed examination, justified pattern, dose or treatment duration. Those associations cannot substitute for clinical assessment or establish that 辨证论治 occurred.')
replace('This is our interpretation: consumption format','This is our interpretation: format does not determine individualisation. A prepared product can follow clinical assessment, and raw herbs can be bought without one; climate supplies context rather than an individual diagnosis. The decisive evidence is a documented connection between assessed signs and treatment selection, which this visit did not provide.')
replace('A7 Survey coverage and evidential status','Appendix A7 Survey coverage and evidential status')
replace('Table A7 Coverage of the seven survey requirements','Table A7 Appendix survey coverage and evidence limits')

# Preserve each picture, reduce the first-column labels, and keep their provenance in the note.
def first_cell(ti,ri,labels):
    c=d.tables[ti].rows[ri].cells[0]
    assert c._tc.xpath('.//a:blip')
    pp=c.paragraphs
    for p in pp[1:]:p._p.getparent().remove(p._p)
    for k,tx in enumerate(labels):
        p=c.add_paragraph(tx);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing=1.05;p.paragraph_format.space_after=Pt(3)
        run=p.add_run() if not p.runs else p.runs[0]
        run.font.size=Pt(10.5 if k==0 else 8.5);run.bold=k==0
def cell(ti,ri,ci,tx):
    c=d.tables[ti].rows[ri].cells[ci];c.text=tx
    p=c.paragraphs[0];p.paragraph_format.line_spacing=1.05;p.paragraph_format.space_after=Pt(2)
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER if ci<3 else WD_ALIGN_PARAGRAPH.LEFT
    p.runs[0].font.size=Pt(10.5)

first_cell(1,1,['Ginseng tonics','人参／西洋参'])
for ci,tx in enumerate(['Varies by formula.','Not recorded.','Staff linked use to fatigue, Qi support and immunity.','Age-specific purchases were not measured.'],1):cell(1,1,ci,tx)
first_cell(4,2,['Specialist herbs','Requiring combinations'])
for ci,tx in enumerate(['Varies by formula.','Varies by formula.','No combination was identified.','Staff described a need for preparation and guidance.'],1):cell(4,2,ci,tx)
for ri,tx in [(5,'Reference: Lingzhi\n(PolyU, n.d.-i)'),(6,'Field display only\nPreparation unidentified'),(7,'Reference: honeysuckle\n(PolyU, n.d.-k)'),(8,'External example\n(Fei Fah, n.d.)')]:
    p=d.tables[1].rows[ri].cells[0].paragraphs[-1]
    p.clear();run=p.add_run(tx);run.font.size=Pt(8.5)
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
for c in d.tables[1].rows[-1].cells:
    for p in c.paragraphs:p.paragraph_format.keep_with_next=True

# Put the removed image attribution directly beneath the relevant table.
replace('Note. Functions and uses are staff reports','Note. Uses follow the interview or presentation. Reference illustrations, including ginseng (PolyU, n.d.-h), do not verify stock; field images show context. Unidentified formulas have no assigned profile.')
replace('Note. Ban Zhi Lian properties are PolyU','Note. Ban Zhi Lian properties are PolyU reference information. The specialist-herb photograph shows the field cabinet only; no second low-demand herb or combination was identified. The ginseng illustration does not identify a strong-tonic formula. Lower demand is staff-reported, not a verified ranking.')
replace('This revision retains the presentation’s fieldwork','This revision retains the presentation’s fieldwork findings within the thematic analysis of everyday care, convenience and localisation. It separates evidence from interpretation, labels industry examples as promotional or journalistic rather than peer-reviewed, and centres Section 6 on 辨证论治. The final cleanup simplifies neighbourhood calculations, shortens crowded table entries, distinguishes Appendix A7 from main Section 7, and standardises Chinese typography. The illustrated five-column tables and APA 7 references remain. The group presentation and Google Doc template are unchanged.')

# Keep the brief comparison and table notes intact across pages.
paragraph('These comparative industry examples').paragraph_format.keep_together=True
paragraph('7 Limitations and remaining evidence gaps').paragraph_format.page_break_before=True
for p in d.paragraphs:
    if p.text.startswith('Note.'):p.paragraph_format.keep_together=True

# Start the key diagnostic term on its own paragraph instead of splitting it at the margin.
p=paragraph('The course reading of the Suwen')
tx=p.text
tail='辨证论治 requires the person’s signs and circumstances to justify selection, so climatic context cannot substitute for individual assessment.'
assert tx.endswith(tail)
p.clear();p.add_run(tx[:-len(tail)].rstrip())
np=p.insert_paragraph_before(tail)
p._p.addnext(np._p)

# The Chinese label is already complete in the first cell; use its translation in this narrow cell.
cell(1,6,3,'Staff described Liver nourishment and soothing constraint.')

# Set an explicit, installed Chinese font and language on every Chinese text run.
# Split mixed-language runs so converters need not infer the script or font.
def clean_chinese_runs(p):
    for run in list(p.runs):
        tx=run.text
        if not re.search(r'[\u3400-\u9fff]',tx):continue
        if run._r.xpath('.//w:drawing'):continue
        props=deepcopy(run._r.rPr) if run._r.rPr is not None else None
        parent=run._r.getparent();idx=parent.index(run._r)
        parts=re.findall(r'[\u3400-\u9fff]+|[^\u3400-\u9fff]+',tx)
        for part in parts:
            nr=OxmlElement('w:r')
            if props is not None:nr.append(deepcopy(props))
            # Preserve real Word line breaks and tabs rather than placing them inside w:t.
            for token in re.findall(r'[^\n\t]+|\n|\t',part):
                if token=='\n':nr.append(OxmlElement('w:br'))
                elif token=='\t':nr.append(OxmlElement('w:tab'))
                else:
                    nt=OxmlElement('w:t');nt.text=token
                    if token[0].isspace() or token[-1].isspace():nt.set(qn('xml:space'),'preserve')
                    nr.append(nt)
            if re.search(r'[\u3400-\u9fff]',part):
                rp=nr.get_or_add_rPr();fonts=rp.get_or_add_rFonts()
                for key in ['ascii','hAnsi','eastAsia','cs']:fonts.set(qn('w:'+key),'SimSun')
                for key in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:
                    fonts.attrib.pop(qn('w:'+key),None)
                lang=rp.find(qn('w:lang'))
                if lang is None:lang=OxmlElement('w:lang');rp.append(lang)
                lang.set(qn('w:val'),'zh-CN');lang.set(qn('w:eastAsia'),'zh-CN')
            parent.insert(idx,nr);idx+=1
        parent.remove(run._r)

allpars=list(d.paragraphs)
for t in d.tables:
    for row in t.rows:
        for c in row.cells:allpars.extend(c.paragraphs)
for p in allpars:
    for run in p.runs:
        for old,new in [('mood-related proprietary preparation','proprietary preparation for mood support'),('mood-related preparation','preparation for mood support'),('mood-related product','product for mood support')]:
            if old in run.text:run.text=run.text.replace(old,new)
    clean_chinese_runs(p)
d.save(F)

txt='\n'.join(p.text for p in allpars)
def media(path):
    with ZipFile(path) as z:return {n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
checks={
    'no_repeated_ones':not re.search(r'(?:1[. ]+){4,}',txt),
    'no_reported_typos':all(s not in txt for s in ['辩论论治','研解都','mod- . related','辨 证论治']),
    'three_core_terms_present':all(s in txt for s in ['辨证论治','疏肝解郁','望闻问切']),
    'images_unchanged':media(B)==media(F),
    'all_23_pictures':len(d.inline_shapes)==23,
    'appendix_explicit':paragraph('Appendix A7').text.startswith('Appendix A7'),
    'main_headings_preserved':all(sum(p.text==s for p in d.paragraphs)==1 for s in ['7 Limitations and remaining evidence gaps','8 Conclusion']),
    'no_automatic_numbering':len(d.element.xpath('.//w:numPr'))==0,
}
assert all(checks.values()),checks
(R/'_review/final_cleanup_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
