from pathlib import Path
import re
import json
import zipfile
from lxml import etree
from PIL import Image
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
OUT = ROOT / 'Final_Report_V1.docx'
SOURCE = WORK / 'report_v1.md'
PHOTO = ROOT / 'gec1044 hospital visit (3)' / 'gec1044 hospital visit'

SOURCES = {
    'pulse': ('photo_2026-10-15_23-47-39.jpg', (0, 150, 1220, 920)),
    'properties': ('photo_2026-10-15_23-47-48.jpg', (0, 210, 960, 805)),
    'acupuncture': ('photo_2026-10-15_23-47-53.jpg', (0, 180, 960, 790)),
}

RECIPE = [
    ['Ingredient', 'Planned weight', 'Specification'],
    ['Chinese yam', '200 g', 'Fresh peeled edible portion'],
    ['Lotus seeds', '20 g', 'Dried shelled seeds with green embryos removed'],
    ['Red dates', '15 g', 'Dried pitted edible portion'],
    ['Rice', '80 g', 'Dry uncooked white rice'],
    ['Water', '1,000 ml', 'Starting amount; add if needed during cooking'],
]

PROPERTIES = [
    ['Ingredient', 'Nature and flavour', 'Traditional affinity', 'Role in this congee'],
    ['Chinese yam', 'Neutral and sweet', 'Spleen Lung Kidney', 'Main digestive and nourishing focus'],
    ['Lotus seed', 'Neutral sweet and astringent', 'Spleen Kidney Heart', 'Links digestive support with calming shen'],
    ['Red date', 'Warm and sweet', 'Spleen Stomach', 'Supporting nourishment and natural sweetness'],
    ['Rice', 'Sweet in the lecture classification', 'Food base', 'Provides a familiar meal and soft texture'],
]

BIBLIOGRAPHY = [
    'Cacioppo, John T., Laura A. Freberg, and Stephanie J. Cacioppo. Discovering Psychology: The Science of Mind. 4th ed. Cengage Learning, 2022.',
    'Centers for Disease Control and Prevention. “How to Measure Physical Activity Intensity.” December 4, 2025. https://www.cdc.gov/physical-activity-basics/measuring/.',
    'Chinese University of Hong Kong, School of Chinese Medicine. “傷寒論註.” Attributed to Zhang Ji, with commentary by Ke Qin. Accessed November 6, 2026. https://www.scm.cuhk.edu.hk/en-gb/elearning-platform/chinese-medicine-texts-collection-2/chinese-medicine-texts-collection-5/chinese-medicine-texts-collection-5/.',
    'Hong Kong Department of Health, Chinese Medicine Regulatory Office. “药补或食补?” Accessed November 6, 2026. https://www.cmro.gov.hk/html/gb/useful_information/public_health/exhibit_boards/Herbal_Tonics_or_Food_Tonics.html.',
    'Hong Kong Polytechnic University. “大枣.” Accessed November 6, 2026. https://herbaltcm.sn.polyu.edu.hk/sc/herbal/chinese-date.',
    'Hong Kong Polytechnic University. “山药.” Accessed November 6, 2026. https://herbaltcm.sn.polyu.edu.hk/sc/herbal/common-yam-rhizome.',
    'Hong Kong Polytechnic University. “莲子.” Accessed November 6, 2026. https://herbaltcm.sn.polyu.edu.hk/sc/herbal/lotus-seed.',
    'Hooley, Jill M., Matthew K. Nock, and James N. Butcher. Abnormal Psychology. 18th global ed. Harlow, England: Pearson, 2021.',
    'Lou Yu. Photographs of teaching slides in the Thong Chai visit collection. October 15, 2026. Personal photographs.',
    'MacPherson, Hugh, Stewart Richmond, Martin Bland, Stephen Brealey, Rhian Gabe, Ann Hopton, Ada Keding, et al. “Acupuncture and Counselling for Depression in Primary Care: A Randomised Controlled Trial.” PLoS Medicine 10, no. 9 (2013): e1001518. https://doi.org/10.1371/journal.pmed.1001518.',
    'National University of Singapore. GEC1044 Chinese Medicine: Theory and Practice. Lectures 2, 3, 7, 8, 9, and 10. Course teaching materials, AY2026/27 Semester 1.',
    'National University of Singapore. GEC1044. “Assessment.” Course page text saved November 5, 2026.',
    'NHS. “Water, Drinks and Hydration.” Accessed November 6, 2026. https://www.nhs.uk/Live-well/eat-well/food-guidelines-and-food-labels/water-drinks-nutrition/.',
    'Pearson. “Abnormal Psychology, Global Edition.” Title overview. Accessed November 6, 2026. https://www.pearson.com/en-nz/subject-catalog/p/abnormal-psychology-global-edition/P200000003860?view=educator.',
    '梁頌然. “中醫藥如何治療失眠.” University of Hong Kong Faculty of Medicine. February 5, 2022. https://www.med.hku.hk/zh-hk/media/knowledge-exchange/newspaper-columns/2022/feb/chinese-medicine-treatment-for-insomnia.',
]

ITALICS = [
    'Discovering Psychology: The Science of Mind', 'Abnormal Psychology',
    'Discovering Psychology', 'PLoS Medicine', 'Shanghan lun', 'yangsheng',
]

def font_style(style, size, bold=False):
    style.font.name = 'Arial'
    style.font.size = Pt(size)
    style.font.bold = bold
    style.font.color.rgb = RGBColor(0, 0, 0)
    rf = style.element.get_or_add_rPr().get_or_add_rFonts()
    rf.set(qn('w:ascii'), 'Arial')
    rf.set(qn('w:hAnsi'), 'Arial')
    rf.set(qn('w:eastAsia'), 'Microsoft YaHei')

def write_text(p, text):
    for part in re.split(r'(\[\^\d+\])', text):
        m = re.fullmatch(r'\[\^(\d+)\]', part)
        if m:
            r = p.add_run()
            r.style = 'Footnote Reference'
            ref = OxmlElement('w:footnoteReference')
            ref.set(qn('w:id'), m.group(1))
            r._r.append(ref)
        elif part:
            p.add_run(part)

def decorate_paragraph(p):
    # Italicise book and journal titles while preserving separate footnote runs.
    for run in list(p.runs):
        if not run.text:
            continue
        text = run.text
        pats = '(' + '|'.join(re.escape(x) for x in sorted(ITALICS, key=len, reverse=True)) + ')'
        parts = re.split(pats, text)
        if len(parts) > 1:
            run.text = ''
            cursor = run._r
            for part in parts:
                if not part:
                    continue
                r = OxmlElement('w:r')
                if part in ITALICS:
                    pr = OxmlElement('w:rPr')
                    pr.append(OxmlElement('w:i'))
                    r.append(pr)
                t = OxmlElement('w:t')
                t.set(qn('xml:space'), 'preserve')
                t.text = part
                r.append(t)
                cursor.addnext(r)
                cursor = r

def add_table(doc, rows, widths):
    table = doc.add_table(rows=1, cols=len(rows[0]))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for cell, width in zip(table.rows[0].cells, widths):
        cell.width = Inches(width)
    for i, row in enumerate(rows):
        cells = table.rows[0].cells if i == 0 else table.add_row().cells
        for j, text in enumerate(row):
            cell = cells[j]
            cell.width = Inches(widths[j])
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tcPr = cell._tc.get_or_add_tcPr()
            margins = OxmlElement('w:tcMar')
            for key in ['top','left','bottom','right']:
                el = OxmlElement('w:'+key)
                el.set(qn('w:w'), '90')
                el.set(qn('w:type'), 'dxa')
                margins.append(el)
            tcPr.append(margins)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.keep_with_next = i < len(rows) - 1
            r = p.add_run(text)
            r.font.size = Pt(9.5)
            if i == 0:
                r.bold = True
                shade = OxmlElement('w:shd')
                shade.set(qn('w:fill'), 'F2F2F2')
                tcPr.append(shade)
        trpr = table.rows[i]._tr.get_or_add_trPr()
        trpr.append(OxmlElement('w:cantSplit'))
        if i == 0:
            trpr.append(OxmlElement('w:tblHeader'))
    borders = OxmlElement('w:tblBorders')
    for key in ['top','left','bottom','right','insideH','insideV']:
        el = OxmlElement('w:'+key)
        el.set(qn('w:val'),'single')
        el.set(qn('w:sz'),'4')
        el.set(qn('w:color'),'D9D9D9')
        borders.append(el)
    table._tbl.tblPr.append(borders)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return table

def add_placeholder(doc, kind):
    if kind == 'cooking':
        text = 'Add four original cooking photographs here\nWeighing  |  Preparing  |  Simmering  |  Finished portion'
    else:
        text = 'Add the cooking and tasting record here, including the actual time, cost, texture, taste, portion size and personal response.'
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(9)
    r=p.add_run(text)
    r.italic=True
    r.font.size=Pt(10)
    r.font.color.rgb=RGBColor.from_string('666666')
    shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'F5F5F5')
    p._p.get_or_add_pPr().append(shade)

def xmlbytes(root):
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)

def add_notes(path, notes):
    W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    REL='http://schemas.openxmlformats.org/package/2006/relationships'
    CT='http://schemas.openxmlformats.org/package/2006/content-types'
    def w(name): return '{'+W+'}'+name
    root=etree.Element(w('footnotes'),nsmap={'w':W,'r':R})
    for id_,kind in [('-1','separator'),('0','continuationSeparator')]:
        n=etree.SubElement(root,w('footnote'));n.set(w('id'),id_);n.set(w('type'),kind)
        etree.SubElement(etree.SubElement(etree.SubElement(n,w('p')),w('r')),w(kind))
    for id_, text in notes.items():
        n=etree.SubElement(root,w('footnote'));n.set(w('id'),id_)
        p=etree.SubElement(n,w('p'));pr=etree.SubElement(p,w('pPr'))
        st=etree.SubElement(pr,w('pStyle'));st.set(w('val'),'FootnoteText')
        r=etree.SubElement(p,w('r'));rp=etree.SubElement(r,w('rPr'))
        rs=etree.SubElement(rp,w('rStyle'));rs.set(w('val'),'FootnoteReference')
        etree.SubElement(r,w('footnoteRef'))
        pattern='('+'|'.join(re.escape(x) for x in sorted(ITALICS,key=len,reverse=True))+')'
        for piece in re.split(pattern,' '+text):
            if not piece:continue
            r=etree.SubElement(p,w('r'))
            if piece in ITALICS:
                rp=etree.SubElement(r,w('rPr'));etree.SubElement(rp,w('i'))
            t=etree.SubElement(r,w('t'));t.set(qn('xml:space'),'preserve');t.text=piece
    with zipfile.ZipFile(path) as z:
        files={name:z.read(name) for name in z.namelist()}
    rels=etree.fromstring(files['word/_rels/document.xml.rels'])
    rel=etree.SubElement(rels,'{'+REL+'}Relationship')
    rel.set('Id','rIdFootnotes');rel.set('Type',R+'/footnotes');rel.set('Target','footnotes.xml')
    ct=etree.fromstring(files['[Content_Types].xml'])
    ov=etree.SubElement(ct,'{'+CT+'}Override')
    ov.set('PartName','/word/footnotes.xml');ov.set('ContentType','application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml')
    files['word/footnotes.xml']=xmlbytes(root)
    files['word/_rels/document.xml.rels']=xmlbytes(rels)
    files['[Content_Types].xml']=xmlbytes(ct)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in files.items():z.writestr(name,data)

def main():
    text=SOURCE.read_text(encoding='utf-8')
    text=text.replace('Discovering Psychology The Science of Mind','Discovering Psychology: The Science of Mind')
    text=text.replace('Acupuncture and Counselling for Depression in Primary Care A Randomised Controlled Trial','Acupuncture and Counselling for Depression in Primary Care: A Randomised Controlled Trial')
    notes=dict(re.findall(r'^\[\^(\d+)\]: (.+)$',text,re.M))
    body=re.split(r'^\[\^1\]:',text,flags=re.M)[0]
    for key,(name,box) in SOURCES.items():
        Image.open(PHOTO/name).crop(box).save(WORK/(key+'.jpg'),quality=96)
    doc=Document()
    # Remove decorative rules inherited from the bundled default template.
    for border in list(doc.styles.element.xpath('.//w:pBdr')):
        border.getparent().remove(border)
    compat=doc.settings.element.find(qn('w:compat'))
    if compat is not None:
        for entry in compat.findall(qn('w:compatSetting')):
            if entry.get(qn('w:name'))=='compatibilityMode':
                entry.set(qn('w:val'),'15')
    section=doc.sections[0]
    section.page_width=Cm(21);section.page_height=Cm(29.7)
    section.top_margin=Cm(2.2);section.bottom_margin=Cm(2.2)
    section.left_margin=Cm(2.4);section.right_margin=Cm(2.4)
    section.header_distance=Cm(1);section.footer_distance=Cm(1)
    section.different_first_page_header_footer=True
    font_style(doc.styles['Normal'],11)
    doc.styles['Normal'].paragraph_format.line_spacing=1.12
    doc.styles['Normal'].paragraph_format.space_after=Pt(8)
    for name,size in [('Title',21),('Heading 1',14),('Heading 2',12)]:
        font_style(doc.styles[name],size,True)
        doc.styles[name].paragraph_format.space_before=Pt(14)
        doc.styles[name].paragraph_format.space_after=Pt(7)
        doc.styles[name].paragraph_format.keep_with_next=True
    font_style(doc.styles['Caption'],9.5)
    doc.styles['Caption'].font.italic=True
    doc.styles['Caption'].paragraph_format.space_after=Pt(10)
    if 'Footnote Text' not in doc.styles:
        doc.styles.add_style('Footnote Text',WD_STYLE_TYPE.PARAGRAPH)
    if 'Footnote Reference' not in doc.styles:
        doc.styles.add_style('Footnote Reference',WD_STYLE_TYPE.CHARACTER)
    font_style(doc.styles['Footnote Text'],9)
    doc.styles['Footnote Text'].paragraph_format.line_spacing=1.0
    doc.styles['Footnote Text'].paragraph_format.space_after=Pt(2)
    doc.styles['Footnote Reference'].font.superscript=True
    doc.styles['Footnote Reference'].font.size=Pt(8)
    p=section.footer.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');p._p.append(fld)
    doc.core_properties.author='Lou Yu'
    doc.core_properties.title='Supporting Student Health through Chinese Food Therapy'
    doc.core_properties.subject='GEC1044 Final Project'
    doc.core_properties.comments=''

    p=doc.add_paragraph('GEC1044 Chinese Medicine Theory and Practice')
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before=Pt(92)
    p=doc.add_paragraph('Supporting Student Health\nthrough Chinese Food Therapy',style='Title')
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before=Pt(26)
    p.paragraph_format.space_after=Pt(25)
    for t in ['Final Project','Student Name  Lou Yu','Student ID  [Add student ID]']:
        p=doc.add_paragraph(t);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    content=body[body.index('## 1 Introduction'):]
    for block in content.strip().split('\n\n'):
        block=block.strip()
        if not block:continue
        if block.startswith('## '):
            title=block[3:]
            if title.startswith('9 '):doc.add_page_break()
            doc.add_heading(title,level=1)
        elif block.startswith('### '):doc.add_heading(block[4:],level=2)
        elif block=='[[BIBLIOGRAPHY]]':
            for t in BIBLIOGRAPHY:
                p=doc.add_paragraph(t)
                p.paragraph_format.left_indent=Cm(.65)
                p.paragraph_format.first_line_indent=Cm(-.65)
                p.paragraph_format.space_after=Pt(8)
                p.paragraph_format.line_spacing=1.0
                for r in p.runs:r.font.size=Pt(9.5)
        elif block.startswith('[[PHOTO '):
            key=block[8:-2]
            p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next=True
            p.add_run().add_picture(str(WORK/(key+'.jpg')),width=Inches(6.1))
        elif block=='[[TABLE recipe]]':add_table(doc,RECIPE,[1.5,1.2,3.45])
        elif block=='[[TABLE properties]]':add_table(doc,PROPERTIES,[1.05,1.35,1.3,2.45])
        elif block.startswith('[[PLACEHOLDER '):add_placeholder(doc,block[14:-2])
        elif re.match(r'^Figure \d+  ',block):
            p=doc.add_paragraph(style='Caption');p.alignment=WD_ALIGN_PARAGRAPH.CENTER;write_text(p,block)
        else:
            p=doc.add_paragraph();write_text(p,block)
    for p in doc.paragraphs:decorate_paragraph(p)
    doc.save(OUT)
    add_notes(OUT,notes)
    with zipfile.ZipFile(OUT) as z:
        root=etree.fromstring(z.read('word/document.xml'))
        nroot=etree.fromstring(z.read('word/footnotes.xml'))
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    refs=root.xpath('//w:footnoteReference/@w:id',namespaces=ns)
    assert sorted(refs,key=int)==sorted(notes,key=int)
    assert len(refs)==len(set(refs))==25
    # Count text before bibliography and all citation text, including table cells and captions.
    parts=[]
    for el in root.find('w:body',ns):
        t=' '.join(el.xpath('.//w:t/text()',namespaces=ns))
        if t=='9 Bibliography':break
        parts.append(t)
    count_text=' '.join(parts)+' '+' '.join(notes.values())
    count=len(re.findall(r"\b[\w]+(?:[-’][\w]+)*\b",count_text))
    assert count<3500,(count,'Over assignment limit')
    manifest={'docx':str(OUT),'estimated_words_including_notes':count,'footnotes':len(refs),'photos':SOURCES,'pending':['Student ID','Cooking photographs','Cooking and tasting record','Clinical chronology']}
    (WORK/'build_check.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({k:v for k,v in manifest.items() if k!='photos'},ensure_ascii=False))

if __name__=='__main__':main()
