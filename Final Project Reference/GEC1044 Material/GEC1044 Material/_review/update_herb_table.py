from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import hashlib, json, re, shutil, urllib.request
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(r'C:\Users\lukel\Downloads\GEC1044 Material')
OUT = ROOT / 'GEC1044_Tong_Keow_First_Draft.docx'
ASSETS = ROOT / '_review' / 'herb_table_assets'
ASSETS.mkdir(exist_ok=True)
backup = ROOT / '_review' / 'GEC1044_Tong_Keow_First_Draft_before_herb_format.docx'
if not backup.exists():
    shutil.copy2(OUT, backup)

# The source's alphabetical title order determines the APA n.d. suffixes.
sources = [
 ('american-ginseng','American ginseng','a'),
 ('barbary-wolfberry-fruit','Barbary wolfberry fruit','b'),
 ('chinese-date','Chinese date','c'),
 ('common-yam-rhizome','Common yam rhizome','d'),
 ('fragrant-solomonseal-rhizome','Fragrant solomonseal rhizome','e'),
 ('ginseng','Ginseng','f'),
 ('grosvenor-momordica-fruit','Grosvenor momordica fruit','g'),
 ('milkvetch-root','Milkvetch root','h'),
 ('tangshen','Tangshen','i'),
]
def asset(source):
    slug,title,letter=source
    url='https://herbaltcm.sn.polyu.edu.hk/herbal/'+slug
    html=urllib.request.urlopen(url,timeout=35).read().decode('utf-8')
    (ASSETS/(slug+'.html')).write_text(html,encoding='utf-8')
    images=re.findall(r'<img[^>]+src="([^"]+/417p278/[^"]+)"',html)
    if not images:
        raise RuntimeError('No reference image for '+slug)
    image_url=images[0]
    image_path=ASSETS/(slug+'.jpg')
    image_path.write_bytes(urllib.request.urlopen(image_url,timeout=35).read())
    return slug,{'page':url,'image':image_url,'local':str(image_path),'letter':letter}
with ThreadPoolExecutor(max_workers=5) as pool:
    evidence=dict(pool.map(asset,sources))
(ASSETS/'sources.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')

profiles=[
 ('ginseng','人参','Ren Shen','Ginseng (root)','Sweet, slightly bitter; neutral','Heart, Spleen, Lung','Strongly tonifies original Qi; supports Spleen and Lung; generates fluids; calms the spirit.','Poor appetite, fatigue and breathlessness in Qi-deficiency patterns; thirst from fluid depletion.'),
 ('american-ginseng','西洋参','Xi Yang Shen','American ginseng (root)','Sweet, slightly bitter; cool','Heart, Lung, Kidney','Tonifies Qi and nourishes Yin; clears heat; generates fluids.','Fatigue, dry mouth, thirst and cough in Qi–Yin deficiency with deficiency heat.'),
 ('tangshen','党参','Dang Shen','Codonopsis (root)','Sweet; neutral','Spleen, Lung','Tonifies middle Qi; strengthens Spleen and Lung functions.','Poor appetite, loose stools, fatigue and shortness of breath in Spleen–Lung Qi deficiency.'),
 ('milkvetch-root','黄芪','Huang Qi','Astragalus / milkvetch (root)','Sweet; warm','Spleen, Lung','Tonifies Qi; strengthens exterior defence; promotes fluid discharge and tissue repair.','Fatigue, poor appetite and loose stools in Qi deficiency; spontaneous sweating from weak exterior defence.'),
 ('fragrant-solomonseal-rhizome','玉竹','Yu Zhu','Fragrant Solomon’s seal (rhizome)','Sweet; slightly cold','Lung, Stomach','Nourishes Yin; moistens dryness; generates fluids and relieves thirst.','Dry cough, dry throat and thirst in Lung–Stomach Yin deficiency.'),
 ('common-yam-rhizome','淮山／山药','Huai Shan / Shan Yao','Chinese yam (rhizome)','Sweet; neutral','Spleen, Lung, Kidney','Supports Spleen and Stomach; generates fluids and benefits Lung; strengthens Kidney.','Poor appetite and persistent diarrhoea in Spleen deficiency; chronic cough in Lung deficiency; frequent urination in Kidney deficiency.'),
 ('chinese-date','红枣／大枣','Hong Zao / Da Zao','Red dates / jujube (fruit)','Sweet; warm','Spleen, Stomach','Tonifies middle Qi; nourishes Blood; calms the spirit.','Poor appetite, tiredness and loose stools in Spleen-deficiency patterns.'),
 ('barbary-wolfberry-fruit','枸杞子','Gou Qi Zi','Goji / wolfberry (fruit)','Sweet; neutral','Liver, Kidney','Nourishes Liver and Kidney; replenishes essence; supports vision.','Dizziness, aching lower back and knees, and impaired vision in Liver–Kidney deficiency patterns.'),
 ('grosvenor-momordica-fruit','罗汉果','Luo Han Guo','Monk fruit (fruit)','Sweet; cool','Lung, Large Intestine','Clears heat; moistens Lung; lubricates the intestines.','Dry cough, sore throat and hoarseness in Lung-heat dryness; constipation from intestinal dryness.'),
]

d=Document(OUT)
old=d.tables[0]
assert len(old.columns)==3 and 'Ginseng' in old.cell(1,0).text
other_tables=[t._tbl.xml for t in d.tables[1:]]
replacements={
 'Table 1  Eight herb entries in the fieldwork presentation': 'Table 1  Traditional profiles of herbs in the eight presentation entries',
 'Requirement A asks for eight best-selling herbs by sales volume over the preceding 12 months. Our materials identify eight entries but contain no transaction totals, quantities or reliable comparative order. Table 1 therefore records fieldwork-identified common sellers, without claiming a numerical annual ranking.': 'Requirement A asks for eight best-selling herbs by sales volume over the preceding 12 months. Our materials identify eight entries but contain no transaction totals, quantities or reliable comparative order. Table 1 profiles those fieldwork-identified common sellers. The combined ginseng / American ginseng entry is separated into two profiles to show their distinct properties; the nine rows do not constitute a ninth sales entry or a numerical annual ranking.',
 'The first entry requires care: the presentation combines ginseng and American ginseng, while the cabinet photograph separately labels American ginseng. We preserve the presentation’s eight entries without treating the two materials as one botanical ingredient or inventing a ninth ranking. The overlap between medicinal materials and soup ingredients is analytically significant. Several herbs enter routine cooking rather than appearing only in a clinical prescription.': 'The presentation combines ginseng and American ginseng, while the cabinet photograph separately labels American ginseng. Their separate profiles make a distinction relevant to 辨证论治 visible: an association with fatigue does not make these herbs interchangeable, and accompanying signs such as dryness and deficiency heat can matter to selection. The remaining seven entries retain their original order. The overlap between medicinal materials and soup ingredients is analytically significant. Several herbs enter routine cooking rather than appearing only in a clinical prescription.',
}
for para in d.paragraphs:
    if para.text in replacements:
        para.text=replacements[para.text]

t=d.add_table(rows=1,cols=5)
t.autofit=False
widths=[1.42,.92,.87,1.61,1.98]
for col,width in zip(t.columns,widths): col.width=Inches(width)
for j,head in enumerate(['Herb','Nature & Flavour','Meridian','Function','Application']):
    t.cell(0,j).text=head
for slug,chinese,pinyin,english,nature,meridians,function,application in profiles:
    cells=t.add_row().cells
    p=cells[0].paragraphs[0]
    p.add_run().add_picture(evidence[slug]['local'],width=Inches(1.08))
    p=cells[0].add_paragraph()
    p.add_run(chinese+' ').bold=True
    p.add_run(pinyin).italic=True
    cells[0].add_paragraph(english)
    p=cells[0].add_paragraph('(PolyU, n.d.-'+evidence[slug]['letter']+')')
    for run in p.runs: run.font.size=Pt(8.5)
    for j,txt in enumerate([nature,meridians,function,application],1): cells[j].text=txt
pr=t._tbl.tblPr
borders=OxmlElement('w:tblBorders')
for edge in ['top','left','bottom','right','insideH','insideV']:
    e=OxmlElement('w:'+edge)
    for k,v in [('val','single'),('sz','4'),('color','D9D9D9')]: e.set(qn('w:'+k),v)
    borders.append(e)
pr.append(borders)
for ri,row in enumerate(t.rows):
    trpr=row._tr.get_or_add_trPr()
    trpr.append(OxmlElement('w:cantSplit'))
    if ri==0: trpr.append(OxmlElement('w:tblHeader'))
    for j,cell in enumerate(row.cells):
        cell.width=Inches(widths[j]); cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
        tcpr=cell._tc.get_or_add_tcPr()
        mar=OxmlElement('w:tcMar')
        for edge,value in [('top','100'),('bottom','100'),('left','90'),('right','90')]:
            e=OxmlElement('w:'+edge); e.set(qn('w:w'),value); e.set(qn('w:type'),'dxa'); mar.append(e)
        tcpr.append(mar)
        if ri==0:
            sh=OxmlElement('w:shd'); sh.set(qn('w:fill'),'E8E8E8'); tcpr.append(sh)
        for p in cell.paragraphs:
            p.alignment=WD_ALIGN_PARAGRAPH.CENTER if j<3 or ri==0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after=Pt(0)
            p.paragraph_format.space_before=Pt(0)
            p.paragraph_format.line_spacing=1.05
            for run in p.runs:
                if run.font.size is None: run.font.size=Pt(10.5)
                if ri==0: run.bold=True
                run.font.name='Times New Roman'
                run._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'Microsoft YaHei')
old._tbl.addprevious(t._tbl)
old._tbl.getparent().remove(old._tbl)

# Source and evidence qualifications remain next to the table rather than being
# mistaken for additional findings from the staff interview.
cap=next(p for p in d.paragraphs if p.text==replacements['Table 1  Eight herb entries in the fieldwork presentation'])
note=cap.insert_paragraph_before('Note. Properties, traditional applications and reference photographs are adapted from The Hong Kong Polytechnic University (PolyU, n.d.-a–i), with the corresponding source identified in each herb cell. These photographs illustrate medicinal materials and were not taken at Tong Keow. The expanded profiles are reference information, not additional staff testimony or measured treatment outcomes. Meridian names refer to TCM functional systems. Applications are examples tied to patterns; a symptom alone does not justify herb selection under 辨证论治. The nature classifications follow the cited database.','Caption')
note.paragraph_format.keep_with_next=True
note.paragraph_format.space_after=Pt(7)

anchor=next(p for p in d.paragraphs if p.text.startswith('Lim, M. K.'))
for slug,title,letter in sources:
    p=anchor.insert_paragraph_before()
    p.paragraph_format.left_indent=Inches(.3)
    p.paragraph_format.first_line_indent=Inches(-.3)
    p.paragraph_format.space_after=Pt(9)
    p.add_run('The Hong Kong Polytechnic University. (n.d.-'+letter+'). ')
    p.add_run(title+'.').italic=True
    p.add_run(' Chinese Herbal Medicine Database. https://herbaltcm.sn.polyu.edu.hk/herbal/'+slug)

assert len(d.tables)==6
assert [x._tbl.xml for x in d.tables[1:]]==other_tables, 'An unrelated table changed'
d.save(OUT)
text='\n'.join(p.text for p in d.paragraphs)+'\n'+'\n'.join(c.text for t in d.tables for row in t.rows for c in row.cells)
(ROOT/'_review'/'draft_sources'/'draft_text.txt').write_text(text,encoding='utf-8')
print(json.dumps({'output':str(OUT),'herb_profiles':len(profiles),'columns':5,'reference_photographs':len(profiles),'unrelated_tables_unchanged':True},indent=2))
