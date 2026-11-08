from pathlib import Path
from copy import deepcopy
from zipfile import ZipFile
import hashlib
import json
import shutil
from docx import Document
from docx.text.paragraph import Paragraph
from docx.oxml import OxmlElement
from docx.shared import Pt, Inches, RGBColor
from docx.oxml.ns import qn

root=Path(__file__).resolve().parent.parent
target=root/'GEC1044_Tong_Keow_Final_Polish.docx'
backup=root/'_review'/'Final_Polish_before_company_background.bak'
source_sha=hashlib.sha256(target.read_bytes()).hexdigest()
def media(path):
    with ZipFile(path) as z:
        return {n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
before_media=media(target)
d=Document(target)
before_text=[p.text for p in d.paragraphs]
before_tables=[[[c.text for c in row.cells] for row in t.rows] for t in d.tables]
heading=next(p for p in d.paragraphs if p.text.startswith('2.2 Tong Keow'))
chain=next(p for p in d.paragraphs if p.text.startswith('The tutor described Tong Keow as a chain'))
assert heading._p.getnext() is chain._p, 'Section 2.2 has changed; inspect before inserting.'

def font(r):
    r.font.name='Times New Roman'
    r.font.size=Pt(12)
    r.font.color.rgb=RGBColor(0,0,0)
    r._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'Microsoft YaHei')

def before(anchor,text,reference=False):
    node=OxmlElement('w:p')
    anchor._p.addprevious(node)
    p=Paragraph(node,anchor._parent)
    if anchor._p.pPr is not None:
        p._p.append(deepcopy(anchor._p.pPr))
    p.style=d.styles['Normal']
    pf=p.paragraph_format
    pf.page_break_before=False
    pf.keep_with_next=False
    pf.keep_together=reference
    pf.widow_control=True
    pf.line_spacing=2.0 if reference else 1.15
    pf.space_before=Pt(0)
    pf.space_after=Pt(0 if reference else 6)
    pf.left_indent=Inches(.5 if reference else 0)
    pf.first_line_indent=Inches(-.5 if reference else 0)
    r=p.add_run(text)
    font(r)
    return p

company='Tong Keow Medical Hall is an established traditional Chinese medicine (TCM) shop and clinic with roots in Toa Payoh. Its company profile traces its founding to 1968 and describes a business now run by the second generation of family owners. Its range includes raw herbal materials such as American ginseng and monk fruit, alongside cooling teas, pills and medicinal plasters. This combination places traditional herbal goods alongside products for everyday care (Tong Keow Medical Hall, 2022; “Instagram Reel About Tong Keow Medical Hall,” n.d.).'
clinic='The company’s promotional profile also describes consultations with registered TCM physicians and services such as acupuncture and cupping for concerns including indigestion, common colds and joint sprains (“Instagram Reel About Tong Keow Medical Hall,” n.d.). These services form part of the wider business’s advertised clinical role. Our Hougang visit focused on retail displays and staff accounts, with no consultation or clinical prescription recorded.'
before(chain,company)
before(chain,clinic)

# Attach the retained directory claim to the reference already present in the report.
old_chain=chain.text
new_chain=old_chain.replace('its Toa Payoh and Hougang outlets.', 'its Toa Payoh and Hougang outlets (Healthcare.com.sg, n.d.).')
assert new_chain!=old_chain
for r in list(chain.runs):
    r._r.getparent().remove(r._r)
font(chain.add_run(new_chain))

instagram_anchor=next(p for p in d.paragraphs if p.text.startswith('Kumari, J.'))
instagram=before(instagram_anchor,'',True)
r=instagram.add_run('[Instagram reel about Tong Keow Medical Hall].'); r.italic=True; font(r)
font(instagram.add_run(' (n.d.). Instagram. https://www.instagram.com/reel/DYn5mkylQw9/'))
fb_anchor=next(p for p in d.paragraphs if p.text.startswith('Unschuld, P. U. (2018).'))
fb=before(fb_anchor,'',True)
font(fb.add_run('Tong Keow Medical Hall. (2022, August 29). '))
r=fb.add_run('Serving the community with heart since 1968'); r.italic=True; font(r)
font(fb.add_run(' [Status update]. Facebook. https://www.facebook.com/TKmedical/photos/603606751228617/'))

added=[company,clinic,instagram.text,fb.text]
actual=[p.text for p in d.paragraphs]
for text in added:
    actual.remove(text)
expected=[text.replace(old_chain,new_chain) for text in before_text]
assert actual==expected, 'Unrelated paragraph content changed.'
assert before_tables==[[[c.text for c in row.cells] for row in t.rows] for t in d.tables]
assert hashlib.sha256(target.read_bytes()).hexdigest()==source_sha, 'Source changed during authoring.'
if not backup.exists(): shutil.copyfile(target,backup)
d.save(target)
assert media(target)==before_media
audit={'file':str(target),'backup':str(backup),'added_paragraphs':added,'chain_before':old_chain,'chain_after':new_chain,'tables_preserved':len(d.tables),'pictures_preserved':len(d.inline_shapes),'social_media_verification':'Links could not be retrieved; descriptions attributed to the user-supplied company profile.'}
(root/'_review'/'company_background_checks.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print('Inserted company background and references in the existing report. Unrelated content and all images preserved.')
