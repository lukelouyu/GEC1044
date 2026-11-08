from pathlib import Path
import shutil, re, json
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

R=Path(__file__).resolve().parents[1]
F=R/'GEC1044_Tong_Keow_First_Draft.docx'
B=R/'_review/GEC1044_Tong_Keow_before_final_polish.docx'
if not B.exists(): shutil.copy2(F,B)
d=Document(B)
ps=list(d.paragraphs)
def replace(i,text):
    ps[i].clear(); ps[i].add_run(text)
def delete(i):
    el=ps[i]._p; el.getparent().remove(el)

replace(6,'This revision retains the presentation’s fieldwork findings within the thematic analysis of everyday care, convenience and localisation. It separates business registration from the chain-model interpretation, condenses commercial comparisons into one explicitly comparative paragraph, and makes Section 6 a critical synthesis centred on 辨证论治. Illustrated Tables A2 and A5 keep the five-column herb-table format with shorter entries; notes and photograph captions state their evidential limits. References follow a consistent APA 7 format. The group presentation and Google Doc template remain unchanged.')
replace(16,'The presentation dates the original Toa Payoh shop to 1968; a directory’s account of its fiftieth anniversary in 2018 supports that reported heritage. ACRA records distinguish Tong Keow Medicine and Provision Shop, registered on 29 March 1975, from Tong Keow Medical Hall Pte. Ltd., incorporated on 1 January 2015; succession between them was not documented. Both list 70 Lorong 4 Toa Payoh #01-333, Toa Payoh Vista, as their registered address. Their primary and secondary activity codes, 47723 and 47102, correspond to Chinese medicine shops and mini-marts, convenience stores and provision shops. These records support a mixed retail classification, not a verified headquarters or warehouse (Accounting and Corporate Regulatory Authority [ACRA], n.d.; Healthcare.com.sg, n.d.; Singapore Department of Statistics [DOS], n.d.).')
replace(17,'The tutor identifies Tong Keow as a chain, and the directory links its Toa Payoh and Hougang outlets. The photographs directly show herbs, soup packs, grains and other foods, including Tong Keow branding. This is our interpretation: the mixed retail model places medicinal and culinary shopping within one neighbourhood business, while the chain format raises the possibility of shared purchasing and product presentation. We did not compare branches, interview management or inspect purchasing records. Common branding establishes visual identity; shared procurement and central assembly remain unverified explanations for the Hougang shelves.')
delete(18)
replace(38,'4.2 Comparative industry examples')
replace(39,'Comparative industry examples illustrate strategies for changing access; they are not academic or population-level evidence of young Singaporeans’ preferences. NYP describes Heng Foh Tong’s redesign of herbal drinks for everyday millennial consumption (Nanyang Polytechnic [NYP], n.d.). Amacha markets TCM-inspired milk teas; a founder interview reports over 150,000 cups sold in eight months and customers including working adults and families, without audited sales or age-disaggregated data (Amacha, n.d.; Angelynn T., 2026). Teck Soon’s owner reported a 30% sales increase after replacing drawer storage with storefront herb displays in 1982 (Chin, 2024). Eu Yan Sang’s halal product category illustrates certification-oriented market presentation, not halal status at Tong Keow (Eu Yan Sang, n.d.). This is our interpretation: formats, visibility and dietary accessibility are deliberate industry responses, making the presentation’s adaptation theme plausible. These promotional and journalistic accounts cannot establish that convenience caused purchases at our outlet, that younger consumers share one preference, or that cross-cultural consumption entails acceptance of TCM theory.')
delete(40);delete(41)
replace(57,'This is our interpretation: shared shopping space, shared consumption and shared therapeutic understanding are separate claims requiring separate evidence. Culinary familiarity offers a point of contact without requiring a common medical framework. The industry examples in Section 4.2 show deliberate attempts to widen accessibility elsewhere; they do not establish certification, customer beliefs or an effect on racial harmony at this outlet.')
replace(59,'6.1 Retail associations and the assessment they cannot replace')
replace(60,'WHO defines the four examinations 望闻问切 as inspection, listening and smelling, inquiry and palpation; their findings inform pattern differentiation 辨证 and treatment reasoning 论治 (WHO, 2022). This is our interpretation: the decisive distinction is between recognising a familiar complaint and assessing its configuration within an individual. A traditional function or a symptom–product association compresses that reasoning into a retail shortcut. Table A6 records such associations, while the visit supplied no observed examination, justified pattern, dosage or treatment duration. Retail familiarity therefore cannot be treated as evidence that 辨证论治 occurred.')
replace(61,'This is our interpretation: consumption format and diagnostic individualisation are distinct dimensions. Prepared products can follow an individual assessment, and raw herbs can be bought without one. Packaging may move selection and preparation to a producer or retailer, but it does not itself determine whether clinical reasoning is retained. Likewise, climatic context can inform questions about a person’s circumstances; it cannot diagnose that person. The analytical boundary is the evidence connecting assessed signs to selection, rather than the material’s appearance or the weather surrounding its sale.')
delete(62)
replace(64,'This is our interpretation: everyday care, convenience and localisation form connected mechanisms of access. Food use brings medicinal vocabulary into household routines; prepared formats redistribute effort; mixed retail, branding and regulated product information make materials available and recognisable locally. Adaptation also redistributes expertise among producers, staff, household cooks, consumers and, where involved, clinicians. These mechanisms explain how contact with TCM is organised without making access equivalent to individually appropriate treatment.')
replace(65,'The course’s historical account treats Chinese medicine as shaped by selection and adaptation (Unschuld, 2018); Yang (2022) situates its Singapore development within migration, community institutions and changing professional arrangements. This is our interpretation: the Tong Keow case adds the retail setting to that account of continuity. Its contribution is to identify how familiar use settings and changing forms make inherited knowledge usable. 辨证论治 supplies the critical test of what that adaptation preserves: accessibility and recognisable language can persist even when the individual assessment needed for a treatment decision is undocumented.')
delete(66)
replace(68,'This study covers one visit, one staff interview and one outlet. Common-seller and lower-demand lists are unranked reports, without sales totals or a verified twelve-month period; customer age, ethnicity and motives were not measured. Neighbourhood figures use different geographical boundaries, and the older-adult study concerns a sample rather than the shop’s catchment. Promotional and journalistic industry examples demonstrate particular strategies, not causal effects, national preferences or Tong Keow customer behaviour. They are contextual comparisons, distinct from academic research and official statistics.')
replace(69,'Item-level sourcing, complete soup recipes, the identity of a staff-reported Singapore-made preparation and chain purchasing arrangements remain unverified. The presentation’s 1968 heritage account is distinguished from registration dates, and climatic explanations are not individual diagnoses. An in-house physician was not clearly confirmed: physician availability and the clinical survey requirements remain not established, rather than evidence of absence. MOH describes professional registration, but the interview establishes neither the staff member’s credentials nor an assessed clinical encounter (Ministry of Health [MOH], 2026). Follow-up would require product labels, sourcing records, branch comparisons, customer data and documented consultations.')
# Preserve the wider complementary-care context without repeating it in the synthesis.
extra=ps[69].insert_paragraph_before('MOH reported that nearly 40% of TCM users in the 2022 National Population Health Survey combined TCM and Western medicine for the same condition (MOH, 2025). This contextual figure does not establish our customers’ treatment choices or motivations. External reference images in Tables A1, A2 and A5 add no observed stock; neither those images nor the field photographs establish therapeutic efficacy, regulatory compliance, botanical authenticity or a community’s medical beliefs.')
# Put this final limitations paragraph after the preceding evidence-gap paragraph.
ps[69]._p.addnext(extra._p)
replace(71,'At Tong Keow, TCM is made usable through household nourishment, redistributed preparation and a neighbourhood shop that combines medicinal and culinary retail. The fieldwork’s herbs, soups, product categories and staff accounts show the concrete settings through which people encounter it; the thematic analysis connects those settings rather than treating the survey as a sequence of answers.')
replace(72,'This is our interpretation: continuity is sustained through adapting ways of access and settings of use, rather than preserving raw-material forms alone. Yet adaptation is not 辨证论治. Retail associations make products intelligible, while an individual treatment decision requires assessed signs and justified selection. The report’s central contribution is to explain how TCM becomes usable while keeping that clinical distinction visible.')

# Short data cells, leaving the name/image/attribution column intact.
rows2=[
['Formula varies; see Table A1.','Formula not recorded.','Staff associated tonics with fatigue, Qi support and immunity.','Prepared tonics were described without age-specific sales data.'],
['Reference fruit: sweet and cool.','Reference fruit: Lung and Large Intestine.','Staff associated it with throat comfort and cooling.','Fruit and drink forms were described, with recipes unrecorded.'],
['Mixture not recorded.','Mixture not recorded.','Staff described everyday wellness uses.','Staff linked simple brewing to younger buyers.'],
['Complete recipe unknown.','Formula not recorded.','Presentation: light nourishment.','Preselected dried packs still require cooking.'],
['Supplement formula unknown.','Whole-product affinities unrecorded.','Staff associated supplements with immunity support.','No immune response or clinical outcome was measured.'],
['Formula not recorded.','Whole-product affinities unrecorded.','Staff used 养肝 and 疏肝解郁 language.','Staff linked use to late nights and stress, without recorded assessment.'],
['Exact formula unidentified.','Whole-product affinities unrecorded.','Staff associated this category with cold symptoms.','The retail association has no recorded patient assessment.'],
['Topical formula unidentified.','No meridian assigned.','Staff associated oils with aches and injuries.','Staff described external use, including by older customers.'],
]
rows5=[
['Sweet, bitter and cold.','Liver, Lung and Kidney.','Reference: clears heat and toxins, resolves stasis and promotes urination.','Reference uses include sores, throat swelling and oedema.'],
['Varies by formula.','Varies by formula.','Specific function cannot be assigned to an unidentified combination.','Staff described limited appeal when selection and preparation require guidance.'],
['Formula not recorded.','Formula not recorded.','Presentation: intensive replenishment 大补.','The presentation associated lower appeal with suitability and climate.'],
]
for ti,rows in [(1,rows2),(4,rows5)]:
    for row,values in zip(d.tables[ti].rows[1:],rows):
        for j,tx in enumerate(values,1):
            c=row.cells[j]; c.text=tx
            for p in c.paragraphs:
                p.paragraph_format.line_spacing=1.05
                p.paragraph_format.space_after=Pt(2)
                p.paragraph_format.keep_with_next=False
                p.alignment=WD_ALIGN_PARAGRAPH.CENTER if j<3 else WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name='Times New Roman';r.font.size=Pt(10.5)
                    r._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Microsoft YaHei')

# Notes immediately below the corresponding table, rather than before its caption.
replace(83,'Note. Functions and uses are staff reports or presentation summaries. Reference images and the Fei Fah illustration do not verify outlet stock; shelf images show display context only. Unidentified formulas have no assigned whole-product nature or meridian.')
replace(96,'Note. Ban Zhi Lian properties are PolyU reference information. The cabinet image identifies no second low-demand herb, and the ginseng illustration does not identify a strong-tonic formula. Lower demand is staff-reported, not a verified ranking.')
for idx,ti in [(78,0),(83,1),(96,4)]:
    d.tables[ti]._tbl.addnext(ps[idx]._p)
    ps[idx].paragraph_format.keep_with_next=False
    ps[idx].paragraph_format.space_before=Pt(4)
    ps[idx].paragraph_format.space_after=Pt(7)
    for r in ps[idx].runs:r.font.size=Pt(10)

replace(156,'Note. The frontage shows branded soup packs and a family cooking image; it does not establish recipes or a sales ranking. Photograph by the group, Tong Keow Healthcare, 13 September 2026.')
replace(161,'Note. The display shows preselected dried soup ingredients requiring preparation; it does not confirm all five soup labels or local manufacture. Photograph by the group, Tong Keow Healthcare, 13 September 2026.')
replace(166,'Note. Labels distinguish American ginseng and claim sulphur-free Dang Shen; they do not verify authenticity, production methods or safety. Photograph by the group, Tong Keow Healthcare, 13 September 2026.')

# Format existing, verified reference metadata; no new source claims are introduced.
refspec=[]
for i in range(108,150):
    tx=ps[i].text
    tx=re.sub(r' \(Records:.*\)$','',tx)
    tx=tx.replace(' (section 5).','.').replace(' (pp. 11–12).','.')
    tx=tx.replace(' (First published online August 11, 2025.)','')
    tx=tx.replace('[Product photograph used as an external illustration]','[Product photograph]')
    tx=tx.replace('https://www.hdb.gov.sg/-/media/hdb-pulse/reports/annual-reports-and-financial-statements/HDB-KS-FY23.pdf','https://www.hdb.gov.sg/hdb-pulse/reports/annual-reports-and-financial-statements')
    if i in (143,144):
        tx=re.sub(r'https://www.singstat.gov.sg/files/[^ ]+','https://www.singstat.gov.sg/find-data/explore-data-themes/population/geographic-distribution/latest-news-data',tx)
    ital=[]
    if i==110:ital=['This S’pore biz is turning TCM into milk tea—8 mths in, it now has 3 outlets & sold 150K+ cups']
    elif i==111:ital=['The Straits Times']
    elif i==112:ital=['Ageing & Society']
    elif i==135:ital=['Complementary Therapies in Medicine, 13']
    elif i==136:ital=['International Journal of Multilingualism, 23']
    elif i==149:ital=['Routledge handbook of Chinese medicine']
    else:
        m=re.search(r'\)\. (.*?)(?= \[|\. https?://|\. Retrieved|\. Chinese Herbal|\. Data.gov|\. Roots| \(B\. Andrews| \(Vol\.)',tx)
        if m: ital=[m[1]]
        elif i==147:ital=['Huang Di nei jing su wen: An annotated translation of Huang Di’s Inner Classic—Basic Questions']
    # Books with a translator: exclude translator/publisher from italic title.
    if i==146:ital=['Traditional Chinese medicine: Heritage and adaptation']
    refspec.append((tx,ital))

def refkey(item):
    tx=item[0];m=re.search(r'\((n\.d\.(?:-[a-z])?|\d{4}[a-z]?)',tx)
    author=tx[:m.start()].strip().lower().removeprefix('the ')
    date=m[1];datekey=(0,date) if date.startswith('n.d.') else (1,date)
    return author,datekey
refspec.sort(key=refkey)
for i,(tx,ital) in zip(range(108,150),refspec):
    p=ps[i];p.clear()
    intervals=[]
    for fragment in ital:
        a=tx.find(fragment)
        if a>=0:intervals.append((a,a+len(fragment)))
    cuts=sorted(set([0,len(tx)]+[x for ab in intervals for x in ab]))
    for a,b in zip(cuts,cuts[1:]):
        run=p.add_run(tx[a:b]);run.italic=any(a>=x and b<=y for x,y in intervals)
        run.font.name='Times New Roman';run.font.size=Pt(11)
    p.paragraph_format.left_indent=Inches(.5)
    p.paragraph_format.first_line_indent=Inches(-.5)
    p.paragraph_format.line_spacing=2
    p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(0)
    p.paragraph_format.keep_together=True;p.paragraph_format.keep_with_next=False
ps[107].alignment=WD_ALIGN_PARAGRAPH.CENTER
delete(150)

# Refresh the crosswalk after moving physician qualifications to limitations.
for ri,tx in [(1,'A1; Section 3.1'),(6,'A6; Section 7')]:
    p=d.tables[6].rows[ri].cells[2].paragraphs[0]
    p.clear();run=p.add_run(tx);run.font.size=Pt(10.5)
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER

# Chinese terminology is preserved as exact text; no OCR substitutions needed.
for p in d.paragraphs:
    if p.style.name not in ('Title','Subtitle','Caption','Heading 1','Heading 2') and p not in ps[108:150]:
        for run in p.runs:
            run._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'Microsoft YaHei')
d.save(F)
alltext='\n'.join(p.text for p in d.paragraphs)
assert alltext.count('8 Conclusion')==1
assert not re.search(r'辨\s+证论治|辨证\s+论治|疏肝\s+解郁|望闻\s+问切|研解都',alltext)
assert len(d.inline_shapes)==23
assert len(d.tables)==7
assert all(len(c._tc.xpath('.//a:blip')) for ti in [1,4] for row in d.tables[ti].rows[1:] for c in row.cells[:1])
print(json.dumps({'file':str(F),'paragraphs':len(d.paragraphs),'tables':len(d.tables),'pictures':len(d.inline_shapes),'references':len(refspec),'words':len(alltext.split())},ensure_ascii=False))
