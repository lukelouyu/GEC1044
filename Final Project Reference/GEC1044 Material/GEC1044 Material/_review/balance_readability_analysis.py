from pathlib import Path
from copy import deepcopy
import re, json, hashlib
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

root = Path(__file__).resolve().parents[1]
source = root / 'GEC1044_Tong_Keow_Readability_Revision.docx'
output = root / 'GEC1044_Tong_Keow_Readability_Revision_v2.docx'
d = Document(source)

def find(prefix):
    found = [p for p in d.paragraphs if p.text.startswith(prefix)]
    assert len(found) == 1, (prefix,len(found))
    return found[0]

def rewrite(p, value):
    size = p.runs[0].font.size if p.runs else None
    p.clear()
    for part in re.findall(r'[\u3400-\u9fff]+|[^\u3400-\u9fff]+', value):
        r = p.add_run(part)
        if size: r.font.size = size
        if re.search(r'[\u3400-\u9fff]', part):
            font = 'Microsoft YaHei' if part == '辨证论治' else 'SimSun'
            r.font.name = font
            r._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),font)

rewrite(d.paragraphs[1], 'Everyday care, convenience, localisation and pattern differentiation')
rewrite(find('The report brings the group’s fieldwork findings'),
    'This revision organises the findings around everyday care, convenience and localisation, with all seven survey records retained in Appendix A. Staff accounts, photographs and our interpretations remain distinct. Industry examples are identified as promotional, journalistic or public-relations sources. Section 6 uses the contrasting ginseng profiles to explain the difference between retail advice and pattern differentiation. It also connects the themes to Tong Keow’s mixed retail model and Hougang neighbourhood while retaining the simpler language of the readability revision.')
rewrite(find('6 Bringing the findings together'),
    '6 Bringing the findings together: pattern differentiation and adaptation')
rewrite(find('6.1 Household care and clinical practice'),
    '6.1 Retail advice and pattern differentiation')

industry = find('Other businesses offer useful comparisons.')
rewrite(industry, industry.text.replace(
    'These institutional, promotional and media accounts describe attempts to change how customers encounter herbal goods. They provide industry comparisons for our convenience theme, rather than a survey of young Singaporeans or Tong Keow’s customers.',
    'These are promotional, journalistic or institutional public-relations accounts, not peer-reviewed studies. They describe deliberate changes in product formats and displays, and serve as industry comparisons rather than data on young Singaporeans or Tong Keow’s customers.'))

rewrite(find('Our visit centred on retail advice and household care.'),
    'Our visit centred on retail advice and household care. Clinical TCM involves assessing a person’s signs and symptoms before selecting treatment, a process known as 辨证论治, or pattern differentiation and treatment (WHO, 2022). Table A1 gives a concrete contrast: ginseng has a neutral nature, while American ginseng is cool and nourishes Yin. A customer’s description of fatigue alone leaves this choice unresolved. The staff’s fatigue–tonic pairing in Table A6 helps explain a retail product association; choosing an individual treatment would require a fuller assessment. We did not observe a clinical consultation.')

conclusion = find('We conclude that the continuity of TCM in this case')
rewrite(conclusion,
    'We conclude that the continuity of TCM in this case depends partly on adapting how people encounter and use it. The ingredients remain part of the tradition, while their packaging, preparation and settings of use change. Tong Keow offers a concrete view of this process through shopping and cooking. Retail advice makes products easier to approach, while individual treatment still calls for assessment of the person.')

rewrite(find('A6 Staff descriptions of product uses'),
    'A6 Staff-described product uses without confirmed clinical prescriptions')
rewrite(find('Table A6 Product uses described by staff'),
    'Table A6 Staff-described product uses without confirmed clinical prescriptions')
rewrite(d.tables[5].cell(0,2).paragraphs[0], 'Clinical details not recorded')
d.tables[5].cell(0,2).paragraphs[0].runs[0].bold = True
for ri in (1,2):
    rewrite(d.tables[5].cell(ri,2).paragraphs[0], 'Formula and patient assessment not recorded.')
rewrite(d.tables[5].cell(3,2).paragraphs[0], 'Staff used fatigue and Qi-support language; no patient assessment recorded.')
rewrite(d.tables[5].cell(4,2).paragraphs[0], 'Staff described immunity support; no patient assessment recorded.')
rewrite(d.tables[5].cell(5,2).paragraphs[0], 'Staff linked use to daily pressures; no diagnosis recorded.')
rewrite(d.tables[5].cell(6,2).paragraphs[0], 'Staff described external use; no injury assessment recorded.')

lim = find('The report draws on one visit and one staff interview.')
rewrite(lim, lim.text.replace(
    'industry examples are institutional, promotional or journalistic accounts used for comparison.',
    'industry examples are promotional, journalistic or institutional public-relations accounts used for comparison.'))

# Trim repeated synthesis and limitations so the conclusion stays with the main text.
rewrite(find('Food use gives herbs a familiar purpose,'),
    'Food use gives herbs a familiar purpose, preselected packs reduce preparation work, and packaging explains intended uses. Local branding and manufacture connect some products to Singapore’s businesses and regulation. Together, these changes bring TCM into ordinary cooking, shopping and daily care.')
rewrite(find('Tong Keow’s mixed medicine-and-food business'),
    'Tong Keow’s mixed medicine-and-food business gives these activities a shared location. Its branding connects the branch to a wider business, while Hougang’s established neighbourhood provides the setting for the clientele described by staff. We see traditional materials presented in forms suited to local household routines.')
rewrite(find('This reading connects with Unschuld’s'),
    'This reading connects Unschuld’s (2018) account of adaptation and Yang’s (2022) history with an everyday retail setting: soup displays and packaged products in a shop that also sells food.')
rewrite(lim,
    'This report draws on one visit and one staff interview. Demand and customer preferences come from staff descriptions; we collected no sales or customer data and made no branch comparison. Neighbourhood statistics describe the surrounding population. The industry accounts provide comparisons, not peer-reviewed evidence.')
rewrite(find('We did not obtain complete soup recipes,'),
    'Complete soup recipes and sourcing and purchasing records were unavailable. The pictured Nature’s Green capsules are listed as Singapore-manufactured, but their ingredient origins remain unknown. Physician presence was unclear, and we recorded no consultation, prescription or patient outcome. MOH (2026) provides the wider professional-registration context.')
rewrite(find('The appendix identifies traditional reference profiles'),
    'The appendix distinguishes reference profiles and external images from field photographs. Customer interviews and further visits could deepen this account.')
rewrite(find('At Tong Keow, TCM enters daily life'),
    'At Tong Keow, familiar ingredients, soup packs and prepared products sit alongside food. Staff linked this range to nourishment, convenience and customers’ routines. Hougang’s residential setting and the mixed retail model help explain how these uses share one neighbourhood shop.')
rewrite(conclusion,
    'In this case, TCM continues through changes in how people encounter and use it. Traditional ingredients take new forms through packaging and preparation, becoming part of shopping and cooking. Retail advice makes products easier to approach, while individual treatment still calls for assessment of the person.')

# Keep the complete A7 group together without adding a new forced page break.
find('A7 Survey coverage and sources').paragraph_format.keep_with_next = True
find('Table A7 Survey coverage and details not recorded').paragraph_format.keep_with_next = True
t = d.tables[6]
for ri,row in enumerate(t.rows):
    props = row._tr.get_or_add_trPr()
    if props.find(qn('w:cantSplit')) is None:
        props.append(OxmlElement('w:cantSplit'))
    for c in row.cells:
        for p in c.paragraphs:
            p.paragraph_format.keep_with_next = ri < len(t.rows)-1
            p.paragraph_format.keep_together = True

# Keep the two conclusion paragraphs together.
find('At Tong Keow, familiar ingredients').paragraph_format.keep_with_next = True
conclusion.paragraph_format.keep_together = True

# Use a heading page break rather than a spare paragraph that can become a blank page.
appendix = find('Appendix A Detailed fieldwork evidence')
previous = appendix._p.getprevious()
if previous is not None and not ''.join(previous.itertext()).strip() and previous.findall('.//' + qn('w:br')):
    previous.getparent().remove(previous)
appendix.paragraph_format.page_break_before = True

d.save(output)
check = Document(output)
body = '\n'.join(p.text for p in check.paragraphs)
assert body.count('辨证论治') == 1
assert 'Tong Jum Chew' in body and '玉竹淮山润燥汤' in body and 'Liver-related' in body
for token in ('Tongum Chew','玉竹准山润燥汤','Liverrelated','辩论论治','辨 证论治'):
    assert token not in body,token
assert 'This is our interpretation' not in body
assert not re.search(r'\bproves?\b',body[:body.index('References')],re.I)
pics = lambda x:[hashlib.sha256(s._inline.xml.encode()).hexdigest() for s in x.inline_shapes]
assert pics(check)==pics(Document(source))
assert len(check.inline_shapes)==36
assert [[c.text for c in r.cells] for r in check.tables[0].rows] == [[c.text for c in r.cells] for r in Document(source).tables[0].rows]
checks = {'output':str(output),'pictures_preserved':36,'keyword_instances':1,
          'subtitle_restored':check.paragraphs[1].text,
          'industry_evidence_level_explicit': 'not peer-reviewed studies' in body,
          'herb_profiles_unchanged':True,'A7_kept_together':True}
(root/'_review/balanced_readability_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(checks,ensure_ascii=False,indent=2))
