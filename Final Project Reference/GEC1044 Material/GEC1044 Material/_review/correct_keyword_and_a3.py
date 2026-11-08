from pathlib import Path
from copy import deepcopy
import shutil, re, json
from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

root = Path(__file__).resolve().parents[1]
target = root / 'GEC1044_Tong_Keow_First_Draft.docx'
backup = root / '_review/GEC1044_Tong_Keow_before_keyword_A3_correction.docx'
if not backup.exists():
    shutil.copy2(target, backup)
d = Document(target)
picture_count = len(d.inline_shapes)

def set_text(p, value):
    template = deepcopy(p.runs[0]._r.rPr) if p.runs and p.runs[0]._r.rPr is not None else None
    p.clear()
    for part in re.findall(r'[\u3400-\u9fff]+|[^\u3400-\u9fff]+', value):
        run = p.add_run(part)
        if template is not None:
            run._r.insert(0, deepcopy(template))
        if re.search(r'[\u3400-\u9fff]', part):
            run.font.name = 'SimSun'
            run._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), 'SimSun')

def replace(prefix, value):
    matches = [p for p in d.paragraphs if p.text.startswith(prefix)]
    assert len(matches) == 1, prefix
    set_text(matches[0], value)

# The source contains six correctly spelled instances; make their glyphs clearer.
keyword_count = 0
for p in d.paragraphs:
    for run in p.runs:
        if '辨证论治' in run.text:
            assert run.text == '辨证论治'
            run.text = '辨证论治'
            run.font.name = 'Microsoft YaHei'
            fonts = run._r.get_or_add_rPr().get_or_add_rFonts()
            for key in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
                fonts.set(qn('w:' + key), 'Microsoft YaHei')
            fonts.attrib.pop(qn('w:eastAsiaTheme'), None)
            keyword_count += 1
assert keyword_count == 6

# Preserve the existing product photograph and change only its labels and evidence.
row = d.tables[2].rows[3]
assert len(row.cells[0].paragraphs) == 3
set_text(row.cells[0].paragraphs[1], 'Mind Soothe Capsules\n舒肝解郁胶囊')
set_text(row.cells[0].paragraphs[2], 'Nature’s Green 绿叶\nFinished CPM')
set_text(row.cells[1].paragraphs[0], 'Ingredient origins and Singapore cultivation are unverified.')
set_text(row.cells[2].paragraphs[0], 'HSA lists Tong Jum Chew as manufacturer and Singapore as the manufacturing country (HSA, 2025b).')
set_text(row.cells[3].paragraphs[0], 'Nature’s Green is the brand; this is a finished Chinese Proprietary Medicine, not evidence of local herb cultivation.')

replace('The staff member described raw materials as coming mainly from China',
    'The staff member described raw materials as coming mainly from China, citing variety and cost, and described limited local cultivation. Cactus 仙人掌, roselle 洛神花, patent medicines 中成药, Five Flower Tea 五花茶 and monk-fruit tea 罗汉果茶 remain the five locally linked examples in Table A3. These are not five verified Singapore-grown products. The supplied photograph identifies Nature’s Green Mind Soothe Capsules as an example of the finished-medicine category, without proving it was the unnamed preparation meant by the staff member. Secondary evidence from HSA lists this product as a Chinese Proprietary Medicine manufactured by Tong Jum Chew in Singapore (HSA, 2025b); its ingredient origins remain unverified. Statements about climatic limits on cultivation and the relative cost of Chinese supply remain the interviewee’s explanations, not an agronomic or price comparison conducted by the group.')
replace('The staff account names five examples',
    'The five locally linked examples distinguish cultivation, manufacture, processing, packing and branding. Nature’s Green is a brand, not a locality category. Its pictured Mind Soothe Capsules are classified here as a Singapore-manufactured finished Chinese Proprietary Medicine, corroborated by HSA’s product list (HSA, 2025b), rather than as Singapore-grown herbs.')
replace('Note. NParks photographs show reference plants;',
    'Note. NParks photographs show reference plants; the interview did not identify a cactus species or stock origins. The Wing Joo Loong image and monk-fruit ingredient image do not identify Tong Keow’s tea products. HSA’s listing corroborates Singapore manufacture of Mind Soothe Capsules; it does not establish ingredient origins or independently audit the photographed batch.')

# Distinguish the two HSA sources dated 2025 in APA author-date citations.
for p in d.paragraphs:
    if p.text.startswith('Health Sciences Authority. (2025, January).'):
        set_text(p, p.text.replace('(2025, January)', '(2025a, January)'))
        anchor = p
    elif 'HSA, 2025)' in p.text:
        for r in p.runs:
            r.text = r.text.replace('HSA, 2025)', 'HSA, 2025a)')
    elif 'Health Sciences Authority, 2025)' in p.text:
        for r in p.runs:
            r.text = r.text.replace('Health Sciences Authority, 2025)', 'Health Sciences Authority, 2025a)')
ref = deepcopy(anchor._p)
anchor._p.addnext(ref)
set_text(Paragraph(ref, anchor._parent),
    'Health Sciences Authority. (2025b). Listing of licensed Chinese Proprietary Medicine products [Data set; updated August 7, 2026]. data.gov.sg. Retrieved October 4, 2026, from https://data.gov.sg/datasets/d_2ae2e6beb458d059318c1c14ad899f98/view')
d.save(target)
check = Document(target)
assert len(check.inline_shapes) == picture_count
assert sum(p.text.count('辨证论治') for p in check.paragraphs) == 6
assert not any(re.search(r'辩论论治|辨\s+证论治|辩证论治|证论治', p.text.replace('辨证论治','')) for p in check.paragraphs)
checks = {'correct_keyword_instances': keyword_count, 'inline_pictures_preserved': picture_count,
          'a3_classification': 'Singapore-manufactured finished Chinese Proprietary Medicine',
          'manufacturer': 'Tong Jum Chew Pte Ltd', 'raw_ingredient_origin': 'unverified'}
(root / '_review/keyword_a3_correction_checks.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf8')
print(json.dumps(checks, ensure_ascii=False, indent=2))
