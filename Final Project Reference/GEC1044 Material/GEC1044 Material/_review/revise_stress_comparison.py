from pathlib import Path
from copy import deepcopy
import re, json, hashlib
from docx import Document
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

root = Path(__file__).resolve().parents[1]
source = root / 'GEC1044_Tong_Keow_Final_Polish.docx'
output = root / 'GEC1044_Tong_Keow_Stress_Comparison_Revision.docx'
doc = Document(source)

def find(prefix):
    ps = [p for p in doc.paragraphs if p.text.startswith(prefix)]
    assert len(ps) == 1, (prefix, len(ps))
    return ps[0]

def rewrite(p, value):
    size = p.runs[0].font.size if p.runs else None
    p.clear()
    for part in re.findall(r'[\u3400-\u9fff]+|[^\u3400-\u9fff]+', value):
        r = p.add_run(part)
        if size: r.font.size = size
        if re.search(r'[\u3400-\u9fff]', part):
            r.font.name = 'SimSun'
            r._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), 'SimSun')

rewrite(find('Staff associated late nights,'),
    'Staff associated late nights, long work hours, stress and prolonged phone use with demand for liver-care or mood-support products. The supplied photograph illustrates this category with Nature’s Green Mind Soothe Capsules. Its English name accompanies the TCM language of soothing Liver-related constraint, 疏肝解郁. We interpret this wording as connecting therapeutic vocabulary to familiar concerns about daily life. “Liver” retains its distinct TCM meaning.')
rewrite(find('Official labour data sharpen this reading:'),
    'Comparative surveys place this retail language in a wider setting. Reporting on ADP’s 2023 survey, Kumari (2024) gives 68% of Singapore workers experiencing work-related stress at least weekly, compared with 61% in the surveyed Asia-Pacific markets; 12% reported daily stress. Gallup’s 2026 report records 43% of Singapore employees experiencing stress during much of the previous day, above the Southeast Asia average of 25% and global average of 40%, and below the Philippines’ 50% (Gallup, 2026a, 2026b). ManpowerGroup’s June 2025 survey places Singapore’s Well-Being Index at 63%, compared with 67% across its 19 surveyed countries (ManpowerGroup, 2025a, 2025b). These surveys use different measures, but provide context for the staff’s descriptions of strain. We interpret the shop’s product language as making TCM relevant to familiar pressures and daily routines, supporting our argument that traditional goods acquire new everyday uses through adaptation.')
p = find('Lower-demand examples further explain')
rewrite(p, p.text.replace('which make selection and portioning part of the shop’s service.', 'which shift selection and portioning to the shop.'))
p = find('This revision keeps the central argument')
rewrite(p, p.text.replace('work-hours discussion', 'workplace-stress comparisons'))
p = find('Field visit 13 September 2026')
for run in p.runs:
    run.text = run.text.replace('Revised 4 October 2026', 'Revised 5 October 2026')

# The work-hours source is no longer cited after the requested replacement.
obsolete = find('Ministry of Manpower. (2026, February 3).')
obsolete._p.getparent().remove(obsolete._p)

ref_template = deepcopy(find('Accounting and Corporate Regulatory Authority.')._p)
def insert_ref(before, prefix, title, suffix):
    element = deepcopy(ref_template)
    before._p.addprevious(element)
    p = Paragraph(element, before._parent)
    p.clear()
    p.add_run(prefix)
    p.add_run(title).italic = True
    p.add_run(suffix)

health = find('Health Sciences Authority. (2025a,')
insert_ref(health, 'Gallup. (2026a). ', 'State of the Global Workplace: Philippines country-level data',
    '. https://www.gallup.com/workplace/706778/state-global-workplace-philippines-country-level-data.aspx')
insert_ref(health, 'Gallup. (2026b). ', 'State of the Global Workplace: Singapore country-level data',
    '. https://www.gallup.com/workplace/707066/state-global-workplace-singapore-country-level-data.aspx')
lim = find('Lim, M. K.,')
insert_ref(lim, 'Kumari, J. (2024, January 24). ', '68% of Singapore workers experience weekly stress at the workplace: Survey',
    '. People Matters. https://sea.peoplemattersglobal.com/news/organisational-culture/68-of-singapore-workers-experience-weekly-stress-at-the-workplace-survey-40095')
mss = find('Meteorological Service Singapore. (n.d.).')
insert_ref(mss, 'ManpowerGroup. (2025a, June). ', 'Global Talent Barometer June 2025: Global report',
    '. https://www.manpowergroup.com/-/media/project/manpowergroup/mpg-marketing/PDF/Insights/MPG-Global-Talent-Barometer-June-2025-Global-Report.pdf')
insert_ref(mss, 'ManpowerGroup. (2025b, June 24). ', 'ManpowerGroup releases its Global Talent Barometer 2025, Volume 1',
    '. https://www.manpower.com.sg/insights/blogs/2025/06/global-talent-barometer-singapore-june-2025')

# Added references shift the old manual break onto a nearly empty page.
# Let the existing bibliography flow continuously instead.
find('Unschuld, P. U. (2018).').paragraph_format.page_break_before = False

doc.save(output)
check = Document(output)
original = Document(source)
assert [t._tbl.xml for t in check.tables] == [t._tbl.xml for t in original.tables]
pics = lambda d: [hashlib.sha256(s._inline.xml.encode()).hexdigest() for s in d.inline_shapes]
assert pics(check) == pics(original)
text = '\n'.join(p.text for p in check.paragraphs)
assert '44.2' not in text and '41.4' not in text
assert 'Ministry of Manpower' not in text and 'MOM' not in text
assert '疏肝解郁' in text and '辨证论治' in text
assert 'second highest' not in text
assert all(s in text for s in ['68%', '12%', '43%', '25%', '40%', '50%', '63%', '67%'])
assert text.count('Lecture 5') == 4
result = {'output': str(output), 'pictures_preserved': len(check.inline_shapes), 'tables_unchanged': True,
          'new_references': 5, 'obsolete_work_hours_reference_removed': True,
          'ADP_figures_attributed_to_2024_secondary_report': True,
          'Gallup_previous_day_measure_used': True}
(root/'_review/stress_comparison_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
