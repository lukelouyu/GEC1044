from pathlib import Path
from copy import deepcopy
import shutil,re,json,hashlib
from docx import Document
from docx.shared import Inches,Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image

R=Path(__file__).resolve().parents[1]
F=R/'GEC1044_Tong_Keow_First_Draft.docx'
B=R/'_review/GEC1044_Tong_Keow_before_appendix_pictures.docx'
if not B.exists():shutil.copy2(F,B)
d=Document(B)
A=R/'_review/appendix_images'
photo=A/'natures-green-mind-soothe.png'
shutil.copy2(Path(r'C:\Users\lukel\AppData\Local\Temp\codex-clipboard-563a9d0a-49df-4d69-bde6-6372ab4d4aea.png'),photo)
HA=R/'_review/herb_table_assets'

def text(p,tx,size=None,bold=None):
 for part in re.findall(r'[\u3400-\u9fff]+|[^\u3400-\u9fff]+',tx):
  r=p.add_run(part)
  if size:r.font.size=Pt(size)
  if bold is not None:r.bold=bold
  if re.search(r'[\u3400-\u9fff]',part):
   r.font.name='SimSun';r._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'SimSun')
 return p
def find(prefix):
 pp=[p for p in d.paragraphs if p.text.startswith(prefix)]
 assert len(pp)==1,(prefix,len(pp))
 return pp[0]
def replace(prefix,tx):
 p=find(prefix);p.clear();text(p,tx);return p
def image(p,f,maxw=1.08,maxh=.73,crop=None,alt=''):
 w,h=Image.open(f).size
 if crop:
  l,t,r,b=crop;w*=1-l-r;h*=1-t-b
 width=min(maxw,maxh*w/h)
 shape=p.add_run().add_picture(str(f),width=Inches(width),height=Inches(width*h/w))
 shape._inline.docPr.set('descr',alt)
 if crop:
  bf=shape._inline.xpath('.//pic:blipFill')[0]
  sr=OxmlElement('a:srcRect')
  for k,v in zip(['l','t','r','b'],crop):sr.set(k,str(round(v*100000)))
  bf.insert(1,sr)
 return shape
def piccell(ti,ri,labels,images):
 c=d.tables[ti].cell(ri,0)
 c.text=''
 p=c.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 p.paragraph_format.space_after=Pt(3);p.paragraph_format.keep_with_next=True
 for i,spec in enumerate(images):
  if i:p.add_run(' ')
  image(p,**spec)
 for k,tx in enumerate(labels):
  p=c.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
  p.paragraph_format.space_after=Pt(2);p.paragraph_format.line_spacing=1.05
  text(p,tx,10.5 if k==0 else 8.5,k==0)
def cell(ti,ri,ci,tx):
 c=d.tables[ti].cell(ri,ci);c.text=''
 text(c.paragraphs[0],tx,10.5)
def note_after(ti,tx):
 t=d.tables[ti]
 p=d.add_paragraph();t._tbl.addnext(p._p)
 p.paragraph_format.space_before=Pt(5);p.paragraph_format.space_after=Pt(8)
 p.paragraph_format.keep_together=True
 text(p,tx,10)

# Native Word crop keeps the original photograph intact in the DOCX.
brand_crop=(.1667,.21875,.3271,.14453)
piccell(1,6,['养肝／疏肝解郁','Nature’s Green 绿叶\nMind Soothe Capsules\n舒肝解郁胶囊','Supplied product photograph'],[dict(f=photo,maxh=1.04,crop=brand_crop,alt='Nature’s Green Mind Soothe Capsules box, marked Made in Singapore')])
cell(1,6,3,'Staff described Liver nourishment and soothing constraint; the box uses “Mind Soothe” language.')
cell(1,6,4,'Staff linked use to late nights and stress; the photograph identifies an example, without clinical assessment.')
replace('The categories, their uses and their order match','The eight categories, their uses and their order match presentation slide 4. The supplied photograph identifies Nature’s Green Mind Soothe Capsules as an illustrated example for liver care and mood support; the interview did not record its brand. Exact formulas and popularity ranks remain unverified. The five-column layout follows Table A1, without assigning a whole-product profile from one ingredient.')
replace('Note. Uses follow the interview or presentation.','Note. Uses follow the interview or presentation. The supplied Nature’s Green photograph identifies the illustrated product; other reference illustrations do not verify stock. The front label does not establish its formula, efficacy or clinical suitability.')

piccell(2,1,['Cactus 仙人掌','Reference cactus\n(NParks, n.d.-b)'],[dict(f=A/'cactus.jpg',alt='Reference Opuntia cochenillifera cactus; interview species not identified')])
piccell(2,2,['Roselle 洛神花','Reference plant\n(NParks, n.d.-a)'],[dict(f=A/'roselle.jpg',alt='Reference Hibiscus sabdariffa roselle plant')])
piccell(2,3,['Patent medicines 中成药','Nature’s Green example\nSupplied photograph'],[dict(f=photo,crop=brand_crop,maxh=.8,alt='Mind Soothe Capsules packaging example')])
cell(2,3,2,'Staff described a Singapore-made preparation; the pictured box also states “Made in Singapore”.')
cell(2,3,3,'The photograph identifies this example, without independently verifying its factory or supply chain.')
piccell(2,4,['Five Flower Tea 五花茶','External product example\n(Wing Joo Loong, n.d.)'],[dict(f=A/'five-flower-tea.jpg',alt='Wing Joo Loong Five Flower Tea reference product ingredients; not verified outlet stock')])
piccell(2,5,['Monk fruit tea 罗汉果茶','Reference fruit only\n(PolyU, n.d.-j)'],[dict(f=HA/'grosvenor-momordica-fruit.jpg',alt='Monk fruit reference ingredient, not an identified finished tea')])
replace('The staff account names five examples','The staff account names five examples but does not verify five locally grown or manufactured products. Cultivation, manufacture, processing, packing and branding are different claims. The supplementary product photograph identifies a Nature’s Green preparation marked “Made in Singapore”; that label supplements the staff account without independently verifying manufacture.')
note_after(2,'Note. NParks photographs show reference plants; the interview did not identify a cactus species or the origin of the stock. The Wing Joo Loong image is an external Five Flower Tea example, and monk fruit illustrates an ingredient. Neither identifies Tong Keow’s tea product. The Nature’s Green photograph shows a label, not independently audited manufacture.')

piccell(3,1,['Qing Bu Liang 清补凉','Fieldwork soup display\nExact pack unconfirmed'],[dict(f=R/'photo/photo_2026-09-13_10-50-00.jpg',maxw=1.08,maxh=.75,alt='Tong Keow soup display context, not an identified Qing Bu Liang recipe')])
piccell(3,2,['Dang Shen and Huang Qi soup\n党参北芪补气汤','Named ingredients only\n(PolyU, n.d.-m, n.d.-l)'],[dict(f=HA/'tangshen.jpg',maxw=.8,maxh=.58,alt='Reference Dang Shen'),dict(f=HA/'milkvetch-root.jpg',maxw=.8,maxh=.58,alt='Reference Huang Qi')])
piccell(3,3,['Yu Zhu and Huai Shan soup\n玉竹淮山润燥汤','Named ingredients only\n(PolyU, n.d.-g, n.d.-f)'],[dict(f=HA/'fragrant-solomonseal-rhizome.jpg',maxw=.8,maxh=.58,alt='Reference Yu Zhu'),dict(f=HA/'common-yam-rhizome.jpg',maxw=.8,maxh=.58,alt='Reference Huai Shan')])
piccell(3,4,['Goji and red date soup\n枸杞红枣养生汤','Named ingredients only\n(PolyU, n.d.-b, n.d.-d)'],[dict(f=HA/'barbary-wolfberry-fruit.jpg',maxw=.8,maxh=.58,alt='Reference goji berries'),dict(f=HA/'chinese-date.jpg',maxw=.8,maxh=.58,alt='Reference red dates')])
piccell(3,5,['Five Finger Fig soup\n五指毛桃健脾汤','Reference root only\n(DH, n.d.)'],[dict(f=A/'fig-3.jpg',maxw=1.12,maxh=.71,crop=(.46,0,0,0),alt='Five Finger Fig dried root reference from Hong Kong Department of Health')])
note_after(3,'Note. Ingredient photographs illustrate only the materials named in the soup labels; they are not complete formulas or photographs of the finished soups. PolyU supplies the six familiar herb images; Hong Kong’s Department of Health (DH, n.d.) supplies the Five Finger Fig root image. The Qing Bu Liang image shows field display context only.')
for ti in [2,3]:
 for row in d.tables[ti].rows:
  trpr=row._tr.get_or_add_trPr()
  if trpr.find(qn('w:cantSplit')) is None:trpr.append(OxmlElement('w:cantSplit'))
  for ci,c in enumerate(row.cells):
   for p in c.paragraphs:
    p.paragraph_format.keep_with_next=False if row!=d.tables[ti].rows[0] else True
    p.paragraph_format.line_spacing=1.05
 # Ensure a repeated header and readable first-column layout.
 trpr=d.tables[ti].rows[0]._tr.get_or_add_trPr()
 if trpr.find(qn('w:tblHeader')) is None:trpr.append(OxmlElement('w:tblHeader'))
find('A3 Five locally linked').paragraph_format.page_break_before=True
find('A4 Five soup therapies').paragraph_format.page_break_before=True

# Update only passages made inaccurate by the newly supplied primary image.
p=find('The staff member associated late nights')
replace('The staff member associated late nights',p.text.replace('We did not verify a causal relation between any habit and a purchase, diagnose customers or identify the exact preparation for mood support.','We did not verify a causal relation between any habit and a purchase or diagnose customers. The supplementary photograph identifies Nature’s Green Mind Soothe Capsules as an illustrated example, without proving it was the exact preparation meant in the interview.'))
p=find('The staff member described raw materials')
replace('The staff member described raw materials',p.text.replace('The staff member described a proprietary preparation for mood support as Singapore-made, but we did not record its identity or producer.','The staff member described a proprietary preparation for mood support as Singapore-made, without recording its identity in the interview. A supplementary photograph identifies Nature’s Green Mind Soothe Capsules, with “Made in Singapore” on the front; this is product-label evidence, not an independent manufacturing audit.'))
p=find('Item-level sourcing, complete soup recipes')
replace('Item-level sourcing, complete soup recipes',p.text.replace('Item-level sourcing, complete soup recipes, the identity of a staff-reported Singapore-made preparation and chain purchasing arrangements remain unverified.','Item-level sourcing, complete soup recipes and chain purchasing arrangements remain unverified. The supplementary photograph identifies a Nature’s Green product labelled “Made in Singapore”, but does not establish its factory, complete formula or whether it was the exact preparation intended in the interview.'))

refs=[
 ('National Parks Board. (n.d.-a). ','Hibiscus sabdariffa L.',' Flora & Fauna Web. https://www.nparks.gov.sg/florafaunaweb/flora/2/0/2096'),
 ('National Parks Board. (n.d.-b). ','Opuntia cochenillifera.',' Flora & Fauna Web. https://www.nparks.gov.sg/florafaunaweb/flora/2/2/2281'),
 ('Department of Health, Hong Kong. (n.d.). ','五指毛桃與斷腸草 [Five Finger Fig root and Gelsemium].',' Chinese Medicine Regulatory Office. https://www.cmro.gov.hk/files/gcmti/research/mmi/ech_search/041_RF_vs_HGE_tc.pdf'),
 ('Wing Joo Loong. (n.d.). ','Lung soothing summer tea.',' https://www.wjl.com.sg/products/wing-joo-loong-lung-soothing-summer-tea'),
]
reference_pars=[];inrefs=False
for p in d.paragraphs:
 if p.text=='References':inrefs=True;continue
 if inrefs and p.style.name.startswith('Heading'):break
 if inrefs and p.text.strip():reference_pars.append(p)
for author,title,tail in refs:
 full=author+title+tail
 key=full.lower()
 anchor=next((p for p in reference_pars if p.text.removeprefix('The ').lower()>key),None)
 if anchor is None:anchor=find('Appendix B')
 p=anchor.insert_paragraph_before()
 if reference_pars[0]._p.pPr is not None:p._p.insert(0,deepcopy(reference_pars[0]._p.pPr))
 text(p,author);text(p,title)
 for r in p.runs[len(re.findall(r'[\u3400-\u9fff]+|[^\u3400-\u9fff]+',author)):]:r.italic=True
 text(p,tail)

# Compact repeated provenance labels; the notes retain all source distinctions.
for ti in [1,2,3]:
 for row in d.tables[ti].rows:
  for c in row.cells:
   for p in c.paragraphs:
    p.paragraph_format.space_before=Pt(0)
    p.paragraph_format.space_after=Pt(1)
    p.paragraph_format.line_spacing=1.0
for ti,ri,labels in [
 (1,6,['养肝／疏肝解郁','Nature’s Green 绿叶\nMind Soothe Capsules','Supplied photograph']),
 (2,1,['Cactus 仙人掌','(NParks, n.d.-b)']),
 (2,2,['Roselle 洛神花','(NParks, n.d.-a)']),
 (2,3,['Patent medicines\n中成药','Nature’s Green example']),
 (2,4,['Five Flower Tea\n五花茶','(Wing Joo Loong, n.d.)']),
 (2,5,['Monk fruit tea\n罗汉果茶','Reference: monk fruit\n(PolyU, n.d.-j)']),
 (3,1,['Qing Bu Liang 清补凉','Field display context only']),
 (3,2,['Dang Shen and Huang Qi soup\n党参北芪补气汤','Named ingredients only']),
 (3,3,['Yu Zhu and Huai Shan soup\n玉竹淮山润燥汤','Named ingredients only']),
 (3,4,['Goji and red date soup\n枸杞红枣养生汤','Named ingredients only']),
 (3,5,['Five Finger Fig soup\n五指毛桃健脾汤','Reference root only (DH, n.d.)']),
]:
 c=d.tables[ti].cell(ri,0)
 for p in list(c.paragraphs)[1:]:p._p.getparent().remove(p._p)
 for i,tx in enumerate(labels):
  p=c.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
  p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(1);p.paragraph_format.line_spacing=1.0
  text(p,tx,10.5 if i==0 else 8.5,i==0)
for ti in [2,3]:
 for row in d.tables[ti].rows[1:]:
  for p in row.cells[0].paragraphs:
   for shape in p._p.xpath('.//wp:inline'):
    extent=shape.find(qn('wp:extent'));h=int(extent.get('cy'));w=int(extent.get('cx'))
    cap=Inches(.60 if ti==2 else .61)
    if h>cap:
     ratio=cap/h;extent.set('cy',str(cap));extent.set('cx',str(round(w*ratio)))
     ext=shape.xpath('.//a:xfrm/a:ext')[0];ext.set('cy',str(cap));ext.set('cx',str(round(w*ratio)))
replace('Note. Ingredient photographs illustrate','Note. Images show named materials, not complete formulas or finished soups. PolyU supplies Dang Shen, Huang Qi, Yu Zhu, Huai Shan, goji and red dates (n.d.-m, n.d.-l, n.d.-g, n.d.-f, n.d.-b, n.d.-d); Hong Kong’s Department of Health (DH, n.d.) supplies Five Finger Fig root. The Qing Bu Liang image shows field display context only.')
replace('The eight categories, their uses','The eight categories follow presentation slide 4. The supplied photograph identifies Nature’s Green Mind Soothe Capsules as an example, while formulas and sales ranks remain unverified. The five-column layout follows Table A1; an ingredient’s profile is not assigned to an unidentified finished product.')
p=find('The staff member associated late nights')
replace('The staff member associated late nights',p.text.replace('We did not verify a causal relation between any habit and a purchase or diagnose customers. The supplementary photograph identifies Nature’s Green Mind Soothe Capsules as an illustrated example, without proving it was the exact preparation meant in the interview.','We did not verify causal links or diagnose customers. The photograph identifies a Nature’s Green example; its connection to the staff’s exact preparation remains unconfirmed.'))
p=find('The staff member described raw materials')
replace('The staff member described raw materials',p.text.replace('The staff member described a proprietary preparation for mood support as Singapore-made, without recording its identity in the interview. A supplementary photograph identifies Nature’s Green Mind Soothe Capsules, with “Made in Singapore” on the front; this is product-label evidence, not an independent manufacturing audit.','Staff described a Singapore-made preparation without naming it. The supplied Nature’s Green Mind Soothe Capsules photograph shows a “Made in Singapore” label, without independently verifying manufacture.'))
for row in d.tables[6].rows:
 for c in row.cells:
  for p in c.paragraphs:
   p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(1);p.paragraph_format.line_spacing=1.0
# APA references retain double spacing without additional inter-entry spacing.
find('7 Limitations and remaining evidence gaps').paragraph_format.page_break_before=False
find('This account follows Unschuld').paragraph_format.keep_together=True
in_synthesis=False
for p in d.paragraphs:
 if p.text.startswith('6 Pattern differentiation'):in_synthesis=True
 if p.text.startswith('7 Limitations'):in_synthesis=False
 if in_synthesis and not p.style.name.startswith('Heading'):
  p.paragraph_format.space_after=Pt(2)
inrefs=False
for p in d.paragraphs:
 if p.text=='References':inrefs=True;continue
 if inrefs and p.style.name.startswith('Heading'):break
 if inrefs:
  p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(0)
   # Keep the final related references on a balanced final bibliography page.
  if inrefs and p.text.startswith('Unschuld, P. U. (2018).'):
   p.paragraph_format.page_break_before=True

d.save(F)
before=Document(B)
checks={
 'A3_every_row_has_picture':all(row.cells[0]._tc.xpath('.//a:blip') for row in d.tables[2].rows[1:]),
 'A4_every_row_has_picture':all(row.cells[0]._tc.xpath('.//a:blip') for row in d.tables[3].rows[1:]),
 'brand_picture_used':len(d.tables[1].cell(6,0)._tc.xpath('.//a:blip'))==1 and 'Nature’s Green' in d.tables[1].cell(6,0).text,
 'core_table_records_unchanged':all([[c.text for c in row.cells] for row in before.tables[i].rows]==[[c.text for c in row.cells] for row in d.tables[i].rows] for i in [0,4,5,6]),
 'headings_preserved':[p.text for p in before.paragraphs if p.style.name.startswith('Heading')]==[p.text for p in d.paragraphs if p.style.name.startswith('Heading')],
 'all_five_soup_rows_retained':len(d.tables[3].rows)==6,
 'all_five_local_examples_retained':len(d.tables[2].rows)==6,
}
assert all(checks.values()),checks
(R/'_review/appendix_picture_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2));print('Inline pictures:',len(d.inline_shapes))
