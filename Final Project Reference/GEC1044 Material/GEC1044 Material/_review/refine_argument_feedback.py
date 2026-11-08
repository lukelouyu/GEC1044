from pathlib import Path
import re, json, hashlib
from collections import Counter
from docx import Document
from docx.oxml.ns import qn

root = Path(__file__).resolve().parents[1]
source = root / 'GEC1044_Tong_Keow_Argument_Revision.docx'
output = root / 'GEC1044_Tong_Keow_Argument_Revision_v2.docx'
d = Document(source)

def find(prefix):
    found = [p for p in d.paragraphs if p.text.startswith(prefix)]
    assert len(found) == 1, (prefix, len(found))
    return found[0]

def rewrite(p, value):
    size = p.runs[0].font.size if p.runs else None
    p.clear()
    for part in re.findall(r'[\u3400-\u9fff]+|[^\u3400-\u9fff]+', value):
        r = p.add_run(part)
        if size: r.font.size = size
        if re.search(r'[\u3400-\u9fff]', part):
            face = 'Microsoft YaHei' if part == '辨证论治' else 'SimSun'
            r.font.name = face
            r._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), face)

rewrite(d.paragraphs[1], 'Everyday care, convenience, localisation, and pattern differentiation')
rewrite(find('This revision connects the fieldwork'),
    'This revision keeps the central argument focused on how Tong Keow fits traditional materials into household practices. Course connections are concentrated in four analytical passages, while the work-hours discussion and conclusion explain the findings’ significance more fully. Staff accounts, photographs and interpretations remain distinct. The seven survey records stay in Appendix A, and industry sources retain their stated status.')
rewrite(find('Staff descriptions refer to the interview;'),
    'Staff descriptions refer to the interview; descriptions of displays refer to our photographs. We identify our interpretations when explaining their significance. Published sources provide historical and industry context, while course concepts guide our reflection. Accounts of popular and lower-demand products represent the staff member’s retail experience.')
rewrite(find('Soup gives herbs a familiar household purpose.'),
    'Soup gives herbs a familiar household purpose. Lecture 5 describes Chinese medicine as a cultural framework that enters everyday food and health habits. This helps us interpret the display through nourishing life, 养生, and medicine and food sharing a source, 药食同源. Lim et al. (2005) identify health maintenance as a significant reason for use, while Yang (2022) situates medicine in changing community life. The fieldwork gives this idea a concrete form: herbal materials enter the household through cooking.')
rewrite(find('Lecture 5’s concept of geographical locality'),
    'The Suwen reading relates seasonal habits to maintaining health (Unschuld & Tessenow, 2011, pp. 45–57). We interpret the staff’s discussion of lighter soups as environmental reasoning expressed in retail advice. Singapore’s weather supplies a local context for explaining their appeal. The ingredient profiles make this account more specific: Yu Zhu, for example, is associated with moistening dryness. Climate provides context for the staff account, while the named ingredients retain their particular TCM functions.')
rewrite(find('Official labour data sharpen this reading:'),
    'Official labour data sharpen this reading: average usual weekly working hours among employed residents fell from 44.2 a decade earlier to 41.4 in 2025 (Ministry of Manpower [MOM], 2026). The falling average means the staff’s remarks are best understood as accounts of perceived strain in customers’ routines, rather than evidence that national working hours are rising. For our argument, the important link is how products are presented through familiar concerns about stress and daily habits. This places the retail account within everyday experience while keeping the wider work-hour trend accurate.')
local = find('Lecture 5 treats localisation as adaptation')
rewrite(local, local.text.replace(' ("A Brief Introduction," n.d., sec. 8)', ''))
rewrite(find('Lecture 5 discusses how the same herb'),
    'Lecture 5 uses senna to explain how the same plant can acquire different meanings in Chinese and Malay medicine. This offers a useful lens for Tong Keow’s shared shopping space: people may encounter the same range of goods through different habits and purposes. We interpret the staff’s account of dessert ingredients and nuts as cultural contact through ordinary purchases. The shop can become familiar across communities while allowing varied understandings of its products. This brings the course discussion into a retail setting; the field evidence concerns shopping routines.')
clinical = find('The ginseng profiles clarify the importance')
rewrite(clinical, clinical.text.replace(' ("A Brief Introduction," n.d., sec. 20)', ''))
rewrite(find('Lecture 5 traces TCM’s changing position'),
    'Modern TCM also forms part of overlapping practices of care. MOH reported that nearly 40% of TCM users in the 2022 National Population Health Survey combined TCM and Western medicine for the same condition (Ministry of Health [MOH], 2025). This national finding gives context to the medicine hall’s everyday role: a purchase for nourishment or household care may be one part of a person’s wider health routine.')
rewrite(find('Lecture 5 makes adaptation central'),
    'Unschuld’s (2018) account of adaptation and Yang’s (2022) history help frame these connections. Our fieldwork extends the discussion into retail: traditional ingredients acquire practical household uses through familiar foods and prepared goods. Continuity becomes visible in how a neighbourhood shop arranges, explains and sells them.')
rewrite(find('Tong Keow makes TCM available through food,'),
    'Tong Keow makes TCM available through food, prepared products and a mixed medicine hall. Soup displays connect herbs to cooking and light nourishment. Prepared packs shift selection and portioning work to the seller, helping households begin with cooking. Local branding and manufacture place some goods within Singapore’s retail setting, while the mixed food range offers different communities familiar reasons to enter. Together, the displays and staff accounts support our argument that traditional materials gain everyday uses through adaptation.')
rewrite(find('Our interpretation is that adaptation gives'),
    'The case brings continuity through adaptation into focus at the scale of a Hougang shop. Food use provides a household purpose, convenience changes the effort involved, and localisation gives products a recognisable form. These retail adaptations sustain opportunities to encounter TCM. Choosing treatment remains a separate task requiring assessment of the person’s pattern of signs and symptoms. The shop’s role in making products approachable and the clinical work of individual assessment are therefore distinct parts of the wider practice of care.')

# This supplied note summary has no verified lecturer or date. Use the user's
# requested narrative course attribution without inventing bibliographic metadata.
lecture_ref = find('A brief introduction to Chinese medicine in Singapore. (n.d.).')
lecture_ref._p.getparent().remove(lecture_ref._p)

d.save(output)
check = Document(output)
original = Document(source)
text = '\n'.join(p.text for p in check.paragraphs)
pics = lambda doc: [hashlib.sha256(s._inline.xml.encode()).hexdigest() for s in doc.inline_shapes]
assert pics(check) == pics(original)
assert [t._tbl.xml for t in check.tables] == [t._tbl.xml for t in original.tables]
assert text.count('Lecture 5') == 4
assert text.count('辨证论治') == 1
assert '辩证论治' not in text
assert 'A Brief Introduction' not in text
assert 'supplied by the user' not in text
assert not re.search(r'\bn\.d\., secs?\.', text)
assert next(p for p in check.paragraphs if p.text.startswith('3.2 Soup packs')).style.name == 'Heading 2'
assert 'A7 Survey coverage and sources' in text
assert '7 Limitations' in text
assert '7 Survey coverage and sources' not in [p.text for p in check.paragraphs]
assert 'not peer-reviewed studies' in text
j = next(i for i,p in enumerate(check.paragraphs) if p.text == 'References')
k = next(i for i,p in enumerate(check.paragraphs) if p.text.startswith('Appendix B'))
refs = [p.text for p in check.paragraphs[j+1:k] if p.text.strip()]
assert all(n == 1 for n in Counter(refs).values())
result = {'output':str(output),'lecture_connections':4,'correct_keyword_instances':1,
          'unverified_lecture_reference_removed':True,'reference_duplicates':0,
          'pictures_preserved':len(check.inline_shapes),'tables_unchanged':True,
          'MOM_interpretation_expanded':True,'conclusion_expanded':True}
(root/'_review/argument_v2_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
