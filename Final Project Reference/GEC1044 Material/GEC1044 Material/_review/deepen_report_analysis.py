from pathlib import Path
from zipfile import ZipFile
import shutil, re, hashlib, json
from docx import Document
from docx.oxml.ns import qn

R=Path(__file__).resolve().parents[1]
F=R/'GEC1044_Tong_Keow_First_Draft.docx'
B=R/'_review/GEC1044_Tong_Keow_before_content_deepening.docx'
if not B.exists():shutil.copy2(F,B)
d=Document(B)

def find(prefix):
    pp=[p for p in d.paragraphs if p.text.startswith(prefix)]
    assert len(pp)==1,(prefix,len(pp))
    return pp[0]

def write(p,text):
    p.clear()
    for part in re.findall(r'[\u3400-\u9fff]+|[^\u3400-\u9fff]+',text):
        run=p.add_run(part)
        if re.search(r'[\u3400-\u9fff]',part):
            run.font.name='SimSun'
            fonts=run._r.get_or_add_rPr().get_or_add_rFonts()
            fonts.set(qn('w:eastAsia'),'SimSun')
    return p

p=find('These comparative industry examples')
old='This is our interpretation: these strategies show deliberate adaptation of access, but do not establish national youth preferences, causes of purchases at our outlet or acceptance of TCM theory.'
assert p.text.endswith(old)
new='What these accounts do document is that businesses deliberately redesign formats and presentation to change how customers encounter herbal goods. This is our interpretation: that documented strategy makes the presentation’s convenience theme analytically plausible; national youth preferences and its effect on Tong Keow purchases remain unmeasured.'
write(p,p.text[:-len(old)]+new)

write(find('This is our interpretation: shared shopping'),'This is our interpretation: a shared retail space can support everyday contact without requiring shared therapeutic interpretation. Here cultural adaptation concerns the range of uses attached to the medicine hall: a culinary purchase can coexist with a wellness purchase while drawing on different meanings. Cultural accessibility may therefore expand through overlapping routines rather than agreement about Qi or meridians. The reported purchases identify routes into that shared space; they do not demonstrate interaction between customers or a historical shift in their beliefs.')

p=find('This is our interpretation: format does not determine')
newp=p.insert_paragraph_before()
write(newp,'The staff’s fatigue pairing with ginseng or Dang Shen in Table A6 illustrates the gap. The presentation groups ginseng and American ginseng, but Table A1 distinguishes the former’s neutral nature from the latter’s cool nature and Yin-nourishing functions (The Hong Kong Polytechnic University [PolyU], n.d.-a, n.d.-h). This is our interpretation: fatigue alone identifies neither the relevant pattern nor which profile, if either, suits a person.')

write(find('This is our interpretation: everyday care'),'This is our interpretation: everyday care, convenience and localisation form connected mechanisms of access. Food use supplies the household setting; preselected packs reduce ingredient-selection work while retaining cooking; local branding and product information present materials in recognisable forms. The mechanisms reinforce one another: familiar use gives selection a purpose, while packaging carries that intended use into the shop and home. Adaptation also redistributes expertise among producers, staff, household cooks, consumers and, where involved, clinicians. None of these mechanisms alone establishes that consumers understand the pattern logic behind a product or receive individually appropriate treatment.')

p=find('The course’s historical account')
newp=p.insert_paragraph_before()
write(newp,'Sections 2.2–2.3 make the setting part of the explanation. The mixed business classification and branded display connect medicinal–culinary retail to Tong Keow’s organisational identity. Hougang’s established housing and older population, with long residence in the study sample, contextualise the staff-described clientele. This is our interpretation: branding links the branch to a wider business, while household food and wellness routines give the model a neighbourhood setting. These conditions help explain its local fit; shared procurement, repeat purchasing and their causal weights remain unmeasured.')
write(p,'This account follows Unschuld’s (2018) emphasis on selection and adaptation and Yang’s (2022) history of Singapore’s community and professional institutions. This is our interpretation: the medicine hall adds a retail mechanism to that history. 辨证论治 provides the critical distinction between making inherited knowledge accessible and documenting an individually justified treatment decision.')

write(find('This revision retains the presentation’s fieldwork'),'This revision retains the presentation’s fieldwork findings within the thematic analysis of everyday care, convenience and localisation. It distinguishes evidence from interpretation and treats industry examples as promotional or journalistic rather than peer-reviewed studies. The analysis now tests retail associations against contrasting ginseng profiles, separates cultural contact from shared therapeutic understanding, and connects access mechanisms to the chain and neighbourhood context. Chinese typography, explicit appendix numbering, illustrated five-column tables and APA 7 references are retained. The group presentation and Google Doc template are unchanged.')

d.save(F)
def media(path):
    with ZipFile(path) as z:return {n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('word/media/')}
before=Document(B)
checks={
    'all_images_unchanged':media(B)==media(F),
    'tables_unchanged':[t._tbl.xml for t in before.tables]==[t._tbl.xml for t in d.tables],
    '23_pictures_retained':len(d.inline_shapes)==23,
    'main_and_appendix_headings_unchanged':[p.text for p in before.paragraphs if p.style.name.startswith('Heading')]==[p.text for p in d.paragraphs if p.style.name.startswith('Heading')],
    'concrete_example_added':'fatigue alone identifies neither the relevant pattern' in '\n'.join(p.text for p in d.paragraphs),
    'observations_not_invented':'do not demonstrate interaction between customers' in '\n'.join(p.text for p in d.paragraphs),
    'causal_weights_not_assumed':'causal weights remain unmeasured' in '\n'.join(p.text for p in d.paragraphs),
}
assert all(checks.values()),checks
(R/'_review/content_deepening_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
