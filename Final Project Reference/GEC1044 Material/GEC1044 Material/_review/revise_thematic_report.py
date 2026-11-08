from pathlib import Path
from copy import deepcopy
import shutil, re, json, hashlib
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image

R=Path(__file__).resolve().parents[1]
F=R/'GEC1044_Tong_Keow_First_Draft.docx'
B=R/'_review/GEC1044_Tong_Keow_First_Draft_before_thematic_revision.docx'
if not B.exists(): shutil.copy2(F,B)
d=Document(B)
oldtables=[deepcopy(t._tbl) for t in d.tables]
oldrefs=[]; collecting=False
for p0 in d.paragraphs:
    if p0.text=='References': collecting=True; continue
    if p0.text.startswith('Source note.'): collecting=False
    if collecting and p0.text.strip(): oldrefs.append(p0.text)
photos=[]; after=False
for p0 in d.paragraphs:
    if p0.text=='Appendix Fieldwork photographs': after=True; continue
    if after: photos.append(deepcopy(p0._p))
mapping={'a':'a','b':'b','c':'d','d':'f','e':'g','f':'h','g':'j','h':'l','i':'m'}
for n in oldtables[0].iter(qn('w:t')):
    n.text=re.sub(r'n\.d\.\-([a-i])',lambda m:'n.d.-'+mapping[m[1]],n.text or '')
for child in list(d.element.body):
    if child.tag!=qn('w:sectPr'): d.element.body.remove(child)
def p(text='',style=None):
    pp=d.add_paragraph(style=style)
    for i,x in enumerate(text.split('**')): pp.add_run(x).bold=bool(i%2)
    return pp
def h(text,level=1): return d.add_heading(text,level)
def note(text):
    pp=p('Note. '+text); pp.paragraph_format.space_after=Pt(7)
    for r in pp.runs:r.font.size=Pt(10)
    return pp
def reuse(title,xml):
    pp=p(title,'Caption'); pp.paragraph_format.keep_with_next=True
    d.element.body.insert(len(d.element.body)-1,deepcopy(xml))
    p('').paragraph_format.space_after=Pt(0)
def table(title,heads,rows,widths):
    cap=p(title,'Caption');cap.paragraph_format.keep_with_next=True
    t=d.add_table(rows=1,cols=len(heads));t.autofit=False
    for c,w in zip(t.columns,widths): c.width=Inches(w)
    for j,tx in enumerate(heads):t.cell(0,j).text=tx
    for row in rows:
        cs=t.add_row().cells
        for j,tx in enumerate(row):cs[j].text=tx
    format_table(t,widths)
    p('').paragraph_format.space_after=Pt(0)
    return t
def format_table(t,widths):
    pr=t._tbl.tblPr
    borders=OxmlElement('w:tblBorders')
    for edge in ['top','left','bottom','right','insideH','insideV']:
        e=OxmlElement('w:'+edge)
        for k,v in [('val','single'),('sz','4'),('color','D9D9D9')]:e.set(qn('w:'+k),v)
        borders.append(e)
    pr.append(borders)
    for ri,row in enumerate(t.rows):
        trpr=row._tr.get_or_add_trPr();trpr.append(OxmlElement('w:cantSplit'))
        if ri==0:trpr.append(OxmlElement('w:tblHeader'))
        for j,c in enumerate(row.cells):
            c.width=Inches(widths[j]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            mar=OxmlElement('w:tcMar')
            for edge,val in [('top','85'),('bottom','85'),('left','100'),('right','100')]:
                e=OxmlElement('w:'+edge);e.set(qn('w:w'),val);e.set(qn('w:type'),'dxa');mar.append(e)
            c._tc.get_or_add_tcPr().append(mar)
            if ri==0:
                sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'E8E8E8');c._tc.get_or_add_tcPr().append(sh)
            for pp in c.paragraphs:
                pp.paragraph_format.space_after=Pt(2);pp.paragraph_format.line_spacing=1.05
                pp.paragraph_format.keep_with_next=ri==0
                if j<3:pp.alignment=WD_ALIGN_PARAGRAPH.CENTER
                for run in pp.runs:run.font.size=Pt(10.5);run.bold=ri==0
def image_table(title,rows):
    t=table(title,['Product or category','Nature & Flavour','Meridian','Function','Application'],[[r[0],*r[3:]] for r in rows],[1.42,.92,.87,1.61,1.98])
    for ri,r in enumerate(rows,1):
        c=t.cell(ri,0); c.text=''
        pp=c.paragraphs[0]; pp.alignment=WD_ALIGN_PARAGRAPH.CENTER
        im=Image.open(r[1]);w0,h0=im.size
        w=min(1.06,1.05*w0/h0)
        pp.add_run().add_picture(str(r[1]),width=Inches(w))
        pp=c.add_paragraph(r[0]);pp.alignment=WD_ALIGN_PARAGRAPH.CENTER
        for run in pp.runs:run.font.size=Pt(10.5);run.bold=True
        pp=c.add_paragraph(r[2]);pp.alignment=WD_ALIGN_PARAGRAPH.CENTER
        for run in pp.runs:run.font.size=Pt(8.5)
        for pp in c.paragraphs:pp.paragraph_format.space_after=Pt(3);pp.paragraph_format.line_spacing=1.05
    return t

p('Traditional Chinese Medicine at Tong Keow Healthcare','Title')
p('Localisation everyday care and pattern differentiation','Subtitle')
p('GEC1044 Group Fieldwork Report   •   Revised complete draft')
p('TD3 Group 2\nLou Yu Luke · Chang Tze Yi Othniel · Li Xudong\nCurtis Chang Kai Xian · Hu Zhixuan Shirley\nTutor Lin Shi Ting')
p('Field visit 13 September 2026\nBlock 809 Hougang Central #01-170 Singapore 530809\nRevised 4 October 2026')
h('Revision note',2)
p('This revision develops the group presentation around everyday food care, convenient consumption forms and localisation, following the tutor’s feedback. All eight herb entries, eight product categories, five locally linked examples, five soup labels, lower-demand examples and retail symptom associations are retained in Appendix A. Former Sections 3.2 and 3.5 become illustrated Tables A2 and A5 in the same five-column style as the herb table. New sources supply business, neighbourhood and industry context; staff testimony, photographic evidence and our interpretations remain distinct. The presentation itself has not been changed.')
h('1 Introduction')
p('Tong Keow’s Hougang outlet provides a small-scale case of **continuity through adaptation** in Traditional Chinese Medicine (TCM). Our field photographs show medicinal materials and packaged soups within a shop selling everyday foods. The staff member described nourishment, throat comfort, fatigue and lifestyle concerns as reasons for purchasing herbs and prepared products. This is our interpretation: TCM becomes usable through familiar meals, selected ingredients and convenient formats that change how consumers encounter traditional knowledge. These adaptations help explain access to TCM without establishing the effectiveness of any treatment or the beliefs of individual customers.')
p('The report asks how that accessibility is produced. Everyday food therapy places herbs within household routines; convenience changes the work needed to select and prepare them; and localisation concerns retail organisation, processing, packaging and cultural contact. These themes deepen the presentation’s account of preventive care, generational differences and local adaptation. The detailed survey record is preserved in Appendix A so that the analysis can follow the relationships among findings rather than the order of questionnaire requirements.')
p('Our critical concept is **pattern differentiation and treatment according to the identified pattern 辨证论治**. Retail language can associate fatigue with a tonic or a cold with a familiar remedy, but an individual treatment decision requires assessment of the person’s configuration of signs and symptoms. The same format can therefore widen access while simplifying the reasoning through which a remedy is selected. We investigate that tension without presenting this retail visit as an observed clinical consultation.')
h('2 Fieldwork method and the neighbourhood medicine hall')
h('2.1 Sources and levels of evidence',2)
p('We observed the shop, photographed displays and conducted a semi-structured interview with one staff member on 13 September 2026. The group presentation organises the fieldwork record; the interview transcripts, presentation script and photographs are used to check its claims. Because the transcripts contain recognition errors, we paraphrase clear statements rather than invent exact quotations. References to “the staff member” below refer to this interview (Tong Keow staff member, personal communication, September 13, 2026). Reports about other TCM institutions provide structural comparison only and are not evidence of our own patient encounters.')
p('**Staff reports** document the interviewee’s descriptions of demand, clientele and sourcing. **Direct observations** identify what photographs and displays visibly show. **Our interpretations** connect those findings to course concepts; they are marked explicitly. **Secondary evidence** is cited where it establishes historical, demographic, regulatory or industry context. We obtained no numerical sales records, customer survey, clinical case notes or supply-chain documentation. “Commonly sold” and “popular” retain the presentation’s terminology but do not mean a verified twelve-month sales ranking.')
h('2.2 Tong Keow history and its mixed retail model',2)
p('The presentation describes an original Toa Payoh shop dating to 1968. A healthcare directory’s account of a fiftieth anniversary in 2018 is consistent with that heritage narrative, but neither establishes the date of legal incorporation. ACRA’s open records identify Tong Keow Medicine and Provision Shop, formerly Tong Keow Medicine Hall, as registered on 29 March 1975. They separately identify Tong Keow Medical Hall Pte. Ltd. as incorporated on 1 January 2015. We retain the presentation’s history as a reported account and distinguish it from the registration chronology; succession between these entities was not independently documented (Accounting and Corporate Regulatory Authority [ACRA], n.d.; Healthcare.com.sg, n.d.).')
p('Both records list 70 Lorong 4 Toa Payoh #01-333, Toa Payoh Vista, as the registered address. This is evidence of an address, not proof of a headquarters or central warehouse. Their primary activity code is 47723 and secondary code 47102. SingStat maps these to Chinese medicine shops and mini-marts, convenience stores and provision shops respectively (ACRA, n.d.; Singapore Department of Statistics [DOS], n.d.). The photographs show a similarly mixed range of herbs, soups, grains and other food products. This is our interpretation: food retail is compatible with the business model rather than an incidental departure from a narrowly medicinal shop.')
p('The tutor’s feedback identifies Tong Keow as a chain with multiple outlets, and the directory links its Toa Payoh and Hougang locations. Our study concerns only the Hougang shop. This is our interpretation: a multi-outlet business could share suppliers, packaging and brand decisions, making part of a branch’s stock selection a chain-level choice. We did not interview management, compare branches or obtain purchasing records, so shared procurement remains a question raised by the chain format rather than an established explanation for the observed shelves. Branded Tong Keow packs demonstrate common visual identity; they do not establish how the contents were purchased or assembled.')
h('2.3 Hougang context and the reported customer base',2)
p('The staff member described the clientele as mainly Chinese, middle-aged and older, including people in their forties and fifties. Official neighbourhood figures provide a context for that impression, with different geographical units kept separate. Hougang planning area had 228,140 residents in June 2024. HDB reported 57,557 dwelling units managed in Hougang and 165,450 residents housed in its flats as at 31 March 2024. The planning-area total includes other housing and is not interchangeable with the HDB-town figure (DOS, 2024; Housing & Development Board [HDB], 2024, pp. 11–12).')
p('In the official June 2025 table, Hougang Central subzone has 4,620 residents. Summing its rounded age bands from 65–69 through 90 and over gives approximately 1,070 people aged 65 or above, or about 23% of the subzone population. We calculated this from the total-sex, total-dwelling rows, not by adding dwelling subtotals. These are resident-population figures rounded to the nearest ten; the subzone is a contextual boundary rather than a measured catchment for the shop (DOS, 2025).')
p('An older-adult study offers a separate view of established neighbourhood life. Among 647 Hougang respondents, 17% lived alone, compared with 15% among 552 respondents in Taman Jurong; the difference was not statistically significant. The Hougang respondents had an average age of 69 and residential tenure of 22 years. These are sample characteristics, not evidence that 17% of Singapore’s solitary older residents live in Hougang or that solitary living causes medicine-hall purchases (Chua et al., 2025). This is our interpretation: long residence and repeated use of local amenities provide a plausible setting for familiar neighbourhood retail relationships, although the study did not measure purchases at Tong Keow.')
p('NHB’s history of Tou Mu Kung records a Teochew community in Hougang associated with fishing, farming and rubber cultivation (National Heritage Board [NHB], n.d.). This supplies historical context for the presentation’s discussion of Chinese medicine within local community life. It does not establish the dialect identity of current customers. This is our interpretation: established housing, a substantial older population and Chinese community history make the staff’s account contextually intelligible. They cannot demonstrate causation, determine consumer preferences by ethnicity or show that every visitor lives nearby. The reported forty- and fifty-year-old clientele also cannot be equated with the demographic category aged 65 and over.')
h('3 Everyday care and food therapy')
h('3.1 Medicinal materials within household nourishment',2)
p('The presentation’s eight common-herb entries are ginseng/American ginseng, Dang Shen, Huang Qi, Yu Zhu, Huai Shan, red dates, goji and monk fruit. Table A1 retains these entries while separating the two ginseng materials into distinct reference profiles. The staff member described Dang Shen, Huang Qi, Yu Zhu, Huai Shan, red dates and goji as common soup ingredients. This is evidence of their reported use in cooking, not a complete prescription. The photographs show prepared ingredient packs and a family cooking image on the soup display (Figures 1–2). They corroborate a domestic food setting without establishing how often households cook or consume these preparations.')
p('This is our interpretation: the overlap between herbs and familiar foods gives medicinal vocabulary an ordinary setting. **Nourishing life 养生** concerns everyday maintenance, while the idea of **medicine and food sharing a source 药食同源** helps describe the movement of materials between nourishment and treatment. An ingredient does not automatically perform the same role in every preparation. Lim et al.’s (2005) earlier survey of complementary and alternative medicine in multiracial Singapore provides evidence that health maintenance was a significant use context; it does not supply present-day sales or customer data for our outlet. Yang’s (2022) history similarly places Chinese medicine within changing community and institutional arrangements. These sources contextualise the field account rather than verify its product claims.')
h('3.2 Soup packs and the meanings of light replenishment',2)
p('The presentation names Qing Bu Liang 清补凉, Dang Shen–Huang Qi soup 党参北芪补气汤, Yu Zhu–Huai Shan soup 玉竹淮山润燥汤, goji–red date soup 枸杞红枣养生汤 and Five Finger Fig soup 五指毛桃健脾汤. Table A4 preserves all five and distinguishes named ingredients from unknown complete recipes. The interview supplied an ingredient list rather than five fully documented formulas; the photographs do not independently confirm every presentation label. This qualification keeps the written report aligned with the slides while making the evidential status of their synthesis explicit.')
p('The staff member and presentation associated these soups with maintenance, digestion, moistening and **light replenishment 清补**, rather than intensive tonification 大补. This is our interpretation: such positioning makes replenishment compatible with ordinary meals, without requiring consumers to describe themselves as patients. The Five Phases association of Earth with the Spleen helps explain traditional digestive-support language; Wood and the Liver help contextualise the mood-related language discussed later. These refer to TCM functional relations, not direct equivalents of biomedical organs (World Health Organization [WHO], 2022). Soup labels and functional vocabulary describe intended use; they do not demonstrate a diagnosed pattern, a recovery outcome or a clinically appropriate dose.')
h('3.3 Climate as a retail explanation rather than a diagnosis',2)
p('The staff member linked monk fruit’s popularity and lighter soups to Singapore’s environment. MSS describes an equatorial climate with high temperatures, abundant rainfall and high humidity throughout the year, with monsoon and inter-monsoon periods (Meteorological Service Singapore [MSS], n.d.). That is an independently documented climatic background. It does not independently verify the staff’s explanation of sales. The phrase “without four distinct seasons” in the presentation is therefore treated as a broad description of tropical conditions rather than a claim that Singapore lacks seasonal weather variation.')
p('The course reading of the Suwen relates seasonal conduct to the maintenance of health (Unschuld & Tessenow, 2011, pp. 45–57). This is our interpretation: the staff’s account shows environmental reasoning being adapted from a seasonal vocabulary to an equatorial retail setting. It remains a situated interpretation. High ambient heat does not mean every individual has a heat pattern; high humidity does not establish dampness in every body. Yu Zhu’s moistening association is not synonymous with eliminating dampness. 辨证论治 requires the person’s signs and circumstances to justify selection, so climatic context cannot substitute for individual assessment.')
h('4 Convenience and changing consumption forms')
h('4.1 Generational accounts and redistributed preparation',2)
p('The staff member described younger customers as buying fewer raw herbs and preferring teas, supplements and simpler preparations. The eight categories in Table A2 retain exactly the presentation’s list: ginseng tonics, monk-fruit products, flower/herbal teas, soup packs, Lingzhi supplements, liver-care/mood-support products, Yin Qiao-type remedies and medicated oils. We did not interview consumers or measure purchases by age. The generational account is therefore staff testimony about this outlet, not evidence that all young Singaporeans have the same preference or have abandoned traditional medicine.')
p('The photographs show preselected dried packs, packaged goods and a multi-buy promotion. Selection and portioning have already been performed for the buyer, but the photographed soups still require cooking. This is our interpretation: convenience redistributes effort rather than necessarily eliminating it. A packer selects the combination, staff explain its purpose and a household completes preparation. A ready-to-drink tea would shift brewing to the seller, whereas a capsule changes both preparation and consumption. We did not confirm a ready-to-drink range at Tong Keow. This distinction develops the slides’ convenience argument without adding an unobserved product to the field inventory.')
h('4.2 Industry comparisons and the limits of claims about youth',2)
p('Nanyang Polytechnic documents a collaboration with Heng Foh Tong to position herbal drinks for daily consumption among millennials. Business students worked on market positioning, design students on bottle identity and a vending concept, and applied-science work addressed sugar reduction and stability (Nanyang Polytechnic [NYP], n.d.). This is evidence of a specific industry strategy, not a national estimate of young consumers’ preferences. Its relevance to Tong Keow is comparative: formats and presentation can be deliberately redesigned to create everyday entry points into herbal consumption.')
p('Amacha supplies a more recent comparison. In a founder interview, Angelynn T. (2026) reported the business’s claim of more than 150,000 cups sold within eight months and three outlets by January 2026. The founder described customers as largely working adults and also families introducing children to herbal drinks. Those statements are not audited sales or an age-disaggregated customer survey. The article also describes daily brewing before sale, illustrating how convenience for the purchaser can depend on preparation retained by the producer. Amacha’s own menu presents TCM-inspired milk teas, including monk-fruit combinations (Amacha, n.d.). Neither source establishes sales or customer behaviour at Tong Keow.')
p('This is our interpretation: the two comparisons strengthen the plausibility of the presentation’s convenience theme by showing that businesses actively change formats and communication. They cannot prove that convenience caused young people’s purchases at our site. Teck Soon’s owner reported a 30% sales increase after replacing drawer storage with storefront herb displays in 1982 (Chin, 2024). This historical comparison concerns visibility as a form of access. Tong Keow’s photographed frontage similarly makes preparations visible, but we have no before-and-after sales data to test its effect.')
h('4.3 Lifestyle language and what lower demand reveals',2)
p('The staff member associated late nights, long work hours, stress and prolonged phone use with liver-care or mood-support preparations. This is our interpretation: wellness marketing can turn a diffuse lifestyle concern into a familiar product choice, linking the presentation’s account of pressure to its account of convenient forms. We did not verify a causal relation between any habit and a purchase, diagnose customers or identify the exact mood-related preparation. 疏肝解郁 describes soothing Liver-related constraint in a TCM vocabulary; it does not itself establish depression treatment or a biomedical hepatic disorder.')
p('National labour data also qualify a simple story of ever-increasing work intensity. MOM reported average usual weekly working hours of 41.4 among employed residents in 2025, down from 44.2 a decade earlier (Ministry of Manpower [MOM], 2026). An average does not describe each customer’s schedule or stress. It provides context while preventing us from turning staff accounts of pressure into an unsupported claim that national working hours are continually rising. Preparation effort, work routines and product use would need to be studied together through customer interviews before this suggested relationship could be tested.')
p('The presentation’s low-demand examples are Ban Zhi Lian 半枝莲, specialist herbs requiring combinations and strong tonic formulas 大补方. Table A5 retains one named material and two categories, rather than inventing three ranked herbs. The staff member linked lower appeal to unfamiliarity, preparation and the need for guidance; the presentation also linked strong tonics to climatic suitability. This is our interpretation: reduced demand for a more demanding format need not imply rejection of TCM as a whole. The staff also described stocking less of poorly selling items, so observed availability is partly selected by the retailer and cannot independently validate a bottom-three ranking.')
h('5 Localisation through processing packaging and cultural contact')
h('5.1 Separating cultivation manufacture and retail selection',2)
p('The staff member described raw materials as coming mainly from China, citing variety and cost, and described limited local cultivation. Cactus 仙人掌, roselle 洛神花, patent medicines 中成药, Five Flower Tea 五花茶 and monk-fruit tea 罗汉果茶 remain the five locally linked examples in Table A3. They were not verified as five Singapore-grown or Singapore-manufactured items. The staff member described a mood-related proprietary preparation as Singapore-made, but we did not record its identity or producer. Statements about climatic limits on cultivation and the relative cost of Chinese supply remain the interviewee’s explanations, not an agronomic or price comparison conducted by the group.')
p('The photographs show Tong Keow branding, selected soup materials and geographical labels on the cabinet. This is our interpretation: localisation can occur at several stages, including assembling ingredients into a familiar soup, portioning, naming and presenting them for local use. Visible branding supports retail adaptation. It does not establish the place where a specific ingredient was grown or a pack was assembled. This distinction refines the presentation’s statement that imported materials are processed and packaged locally: that account is retained as staff-reported, while product-level local processing remains unverified.')
p('Singapore’s Chinese Proprietary Medicines (CPM) framework establishes that local manufacture and assembly are formal regulated activities. HSA’s dealer guidance requires the relevant licences for importing and wholesale supply, and a valid manufacturer’s licence and GMP compliance for local manufacturing or assembly facilities. Its consumer guidance includes re-packers among regulated dealers and requires product listing before a CPM is imported, manufactured or sold (Health Sciences Authority [HSA], 2026c, 2026d). These obligations concern finished Chinese Proprietary Medicines and the activities performed by a dealer. They do not automatically classify every raw herb, food, tea or soup pack as a CPM, or prove that Tong Keow operates a licensed assembly facility. We did not audit its licences or identified products.')
h('5.2 Packaging as regulatory and cultural translation',2)
p('HSA’s CPM listing guidelines require full labelling in English and allow additional languages, whose text must correspond to the English information. Required particulars include product and ingredient information, batch and expiry details, with relevant manufacturer, importer or assembler details on outer packaging (HSA, 2025, section 5). These requirements show how a finished medicinal product must become legible within Singapore’s regulatory setting. Listing is not evidence that its therapeutic effects have been proven (HSA, 2026b). The photographs of Tong Keow packs establish branding and packaged form, but our images and records are insufficient for a complete bilingual label or compliance audit.')
p('A packaging study provides a regional comparison rather than Singapore-specific field evidence. Liu et al. (2026) examined Chinese herbal medicines sold in Malaysia and showed how legal constraints shape translated product names and therapeutic statements. Their account helps frame translation as a negotiation between medical vocabulary, permissible claims and consumer communication. Malaysia’s rules and sampled products cannot substitute for HSA requirements or evidence about Tong Keow’s labels. This is our interpretation: packaging can alter how inherited knowledge is encountered, but changes in language, dosage form or branding alone do not establish that a customer understands the underlying pattern logic.')
p('Quality language also affects that encounter. The staff member emphasised fresh colour, visible freshness and sulphur-free materials. Figure 3 shows the sulphur-free Dang Shen claim and separate American ginseng label. It verifies the presence of the claims rather than production methods, authenticity or safety. HSA’s supplement-claims guidance rejects the implication that natural origin guarantees safety (HSA, 2026a). This is our interpretation: reassuring labels can support retail trust, but neither a quality claim nor convenient packaging resolves individual suitability under 辨证论治.')
h('5.3 A shared shopping space and differing meanings of use',2)
p('The staff member described Malay customers buying dessert ingredients and Indian customers buying nuts, alongside a largely Chinese clientele. We did not independently identify customers’ ethnicity or ask them about medical beliefs. The photographs show a product mix compatible with culinary shopping, but cannot verify the reported purchasing pattern. This is our interpretation: the medicine hall’s combined food and medicinal range offers reasons for contact across cultural boundaries. Buying a dessert ingredient in this space does not show acceptance of Qi, meridians or pattern differentiation.')
p('Eu Yan Sang’s Singapore website provides an industry example through a halal product category containing preparations with ingredients such as goji and red dates (Eu Yan Sang, n.d.). This is evidence of another company’s certification-oriented market presentation, not halal status at Tong Keow. This is our interpretation: dietary certification and familiar food uses can make products accessible across communities while meanings remain diverse. Shared shopping space, shared consumption and shared therapeutic understanding require different evidence. The fieldwork supports an account of possible contact through everyday retail, not a demonstrated effect on racial harmony or uniform TCM adoption.')
h('6 Pattern differentiation and continuity through adaptation')
h('6.1 What is missing between a complaint and a remedy',2)
p('WHO terminology describes the four examinations 望闻问切 through inspection, listening and smelling, inquiry and palpation. These contribute to pattern differentiation 辨证; treatment reasoning 论治 then follows the identified pattern (WHO, 2022). This is our interpretation: the analytical issue is the route from information about a person to a justified choice. An ingredient’s traditional function, a product label or a familiar complaint cannot alone supply that route. Table A1 illustrates the distinction through the separate ginseng and American ginseng profiles: their different traditional nature and Yin-related functions prevent a general fatigue association from making them interchangeable.')
p('The six pairings in Table A6 are exactly the presentation’s retail associations: colds with Yin Qiao-type remedies; diarrhoea with Huoxiang Zhengqi-type remedies; fatigue/Qi-deficiency language with ginseng or Dang Shen; lower-immunity language with Lingzhi or supplements; late nights/stress with liver-care or mood-support products; and aches/injuries with medicated oils. We did not observe the signs, examination, reasoning, dosage or duration supporting an individual prescription. Fatigue alone does not establish Qi deficiency, and the marketing term “immunity” is not a direct equivalent of Qi. These findings document accessible retail explanations rather than eight physician-treated symptoms or eight clinical prescriptions.')
p('An in-house physician was not clearly confirmed. That means physician availability and the survey’s clinical requirements remain **not established**, not that the outlet has no physician. MOH’s practitioner information supplies a context of professional registration, but our interview does not establish the staff member’s role or credentials (Ministry of Health [MOH], 2026). Prepared products can be selected through an individual clinical assessment; raw herbs can also be purchased without one. This is our interpretation: format and diagnostic individualisation are distinct dimensions, so convenience should not be treated as proof that pattern differentiation has disappeared.')
h('6.2 Connecting everyday routines formats and local institutions',2)
p('This is our interpretation: the three themes reveal connected mechanisms of access. Food use places traditional materials within household maintenance; convenient forms redistribute selection and preparation; retail organisation and packaging make them available and recognisable in a Singapore neighbourhood. Climate enters through the staff’s account of local suitability, regulation through formal product requirements, and cultural contact through different culinary and wellness uses. Chain purchasing and neighbourhood habits remain plausible contextual influences whose operation at this outlet still needs direct investigation.')
p('This understanding follows the course’s treatment of Chinese medicine as historically shaped by selection and adaptation (Unschuld, 2018). Yang (2022) describes Singapore’s history through migration, community institutions and changing professional arrangements. The outlet adds a retail perspective to that history without proving a change from an earlier Tong Keow clinic to its present form. MOH reported that nearly 40% of TCM users in the 2022 National Population Health Survey combined TCM and Western medicine for the same condition (MOH, 2025). That wider context supports the possibility of complementary use, not evidence about our customers’ treatment choices. We did not establish motivations such as avoiding side effects or preferring “natural” medicine.')
p('This is our interpretation: adaptation can preserve visible ingredients and functional vocabulary while changing where expertise resides, among a packer, staff member, household cook, consumer and, when involved, clinician. The distinction supplied by 辨证论治 prevents retail familiarity from being mistaken for clinical reasoning. The fieldwork shows mechanisms that make TCM approachable; it cannot determine how frequently those mechanisms lead to an assessed, individually suitable treatment.')
h('7 Limitations and remaining evidence gaps')
p('The study covers one visit, one staff interview and one outlet. Its common-seller and lower-demand lists are unranked accounts, with no sales totals or verified twelve-month period. Customer age, ethnicity and motives were not measured. We lack item-level sourcing, complete soup formulas and an identified locally manufactured preparation. Reference herb photographs and external product illustrations added to Tables A1, A2 and A5 are visibly labelled as such; they add no observed stock or new fieldwork findings. Demographic boundaries, older-adult samples and industry comparisons provide context rather than a substitute for outlet data.')
p('The presentation is retained as the main synthesis of our findings, with its limits made explicit. Its 1968 heritage account is distinguished from registration dates; its local-processing statement remains staff-reported; and its climatic preferences are not applied as diagnoses to all residents. Follow-up evidence would need to identify exact product and soup labels, clarify a physician’s role, compare chain purchasing practices and obtain a defensible demand record. Until then, the clinical survey answers remain unestablished. No conclusion about therapeutic efficacy, regulatory compliance or a whole ethnic group’s beliefs follows from the photographed shelves.')
h('8 Conclusion')
p('Tong Keow’s case shows how TCM can be made usable through specific arrangements of everyday access. The group’s herbs, soups and product categories connect nourishment to familiar household practices; packaged forms redistribute the work of selection and preparation; and the mixed retail model accommodates medicinal and culinary shopping. The staff’s accounts of younger buyers, lighter replenishment and local processing add situated explanations whose limits remain visible. Verified business records, neighbourhood statistics and comparative industry cases deepen those accounts without replacing the fieldwork.')
p('Our contribution is an account of **continuity through adaptation** at the retail counter. The case reveals how ingredients, formats, language and use settings can sustain contact with TCM. It also shows why that contact should be distinguished from **辨证论治**: a complaint–product association is a compressed retail explanation, while an individual treatment requires assessed signs and justified selection. Keeping the two levels separate allows the report to explain accessibility and cultural change without converting availability, packaging or climatic context into evidence of effective personalised care.')

d.add_page_break()
h('Appendix A Detailed fieldwork evidence')
p('These records preserve the presentation’s substantive inventory. A1–A5 correspond to former Sections 3.1–3.5; the questionnaire sequence is retained here for checking completeness, while Sections 3–5 supply the thematic analysis. Traditional applications are reference information or reported positioning, not evidence of clinical efficacy.')
h('A1 Eight herb entries with separate reference profiles',2)
p('The presentation groups ginseng and American ginseng in one entry. Nine reference rows therefore represent eight reported entries, not a ninth seller or an annual ranking. The field cabinet independently labels American ginseng.')
note('Reference photographs and traditional profiles are adapted from the Hong Kong Polytechnic University database (PolyU); they were not photographed at Tong Keow. Meridian names refer to TCM functional systems. Applications depend on assessed patterns, not a symptom alone. ')
reuse('Table A1 Traditional herb profiles in the eight presentation entries',oldtables[0])
h('A2 Eight reported product categories with illustrations',2)
p('The categories, their uses and their order match presentation slide 4. They are not identified brands, exact formulas or measured popularity ranks. The five-column layout follows Table A1. Nature and meridians are not assigned to an unidentified finished product from the properties of one illustrated ingredient.')
note('Ingredient images are illustrative references, not photographs of the finished products sold at the outlet. “Display context” images show fieldwork shelves without confirming the named category’s exact item. The Fei Fah red-flower oil image is an external category example, not verified Tong Keow stock. Photographs and properties do not add products to the field inventory.')
HA=R/'_review/herb_table_assets'; IA=R/'_review/revision_research/table_images'; PH=R/'photo'
rows=[
('人参／西洋参\nGinseng tonics',HA/'ginseng.jpg','Reference material: ginseng\n(PolyU, n.d.-h)','Depends on formula; ginseng and American ginseng differ (Table A1).','Formula not recorded.','Staff: fatigue and Qi support; also described in immunity language.','Prepared tonic form; product-specific age profile unknown. Fatigue alone is not a pattern.'),
('罗汉果\nMonk-fruit products',HA/'grosvenor-momordica-fruit.jpg','Reference material: monk fruit\n(PolyU, n.d.-j)','Fruit reference: sweet, cool. Whole product not identified.','Fruit reference: Lung, Large Intestine.','Staff: throat/lung comfort and cooling or moistening positioning.','Fruit or prepared drinks; staff linked demand to local heat. Exact formulation unknown.'),
('花茶／凉茶\nFlower and herbal teas',IA/'chrysanthemum-flower.jpg','Reference flower: chrysanthemum\n(PolyU, n.d.-e)','Mixture dependent; complete tea formulas not recorded.','Mixture dependent; not recorded.','Staff: everyday wellness; purpose depends on mixture.','Simple brewing; staff associated teas with younger buyers. The flower image does not establish a recorded tea recipe.'),
('药材汤包\nSoup packs',PH/'photo_2026-09-13_10-50-00.jpg','Fieldwork soup display\n13 September 2026','Varies; complete recipes unknown.','Varies; formula not recorded.','Presentation: light nourishment and maintenance.','Preselected dried ingredients; photographed packs still require cooking. Five labels in Table A4.'),
('灵芝保健品\nLingzhi supplements',IA/'glossy-ganoderma.jpg','Reference material: Lingzhi\n(PolyU, n.d.-i)','Finished supplement not identified; no single profile assigned.','Finished formula not recorded.','Staff: “immune support” or general wellness positioning.','Supplement form; no measured immune outcome. Reference fungus is not an identified capsule.'),
('养肝／疏肝解郁\nLiver care and mood support',PH/'photo_2026-09-13_10-49-49.jpg','Fieldwork display context only\nExact preparation unidentified','Exact formula and properties not recorded.','TCM Liver language reported; actual formula affinities unknown.','Staff: liver-care or mood-support language related to stress and late nights.','Proprietary form; not evidence of biomedical liver disease or depression treatment. Display does not identify the reported item.'),
('银翘类\nYin Qiao-type remedies',IA/'japanese-honeysuckle-flower.jpg','Reference material: honeysuckle\nNot the finished remedy\n(PolyU, n.d.-k)','Exact formulation not recorded.','Formula not recorded.','Staff associated these remedies with colds.','Retail association only; no patient pattern or prescription recorded. Ingredient illustration does not verify the formula.'),
('红花油／红油精\nMedicated oils',IA/'red-flower-oil.jpg','External red-flower oil example\n(Fei Fah, n.d.)','Topical formulation; exact outlet product not recorded.','No product-specific affinity established.','Staff: aches and injury-related discomfort.','External use form; staff particularly associated oils with older customers. Illustrated brand not verified at Tong Keow.')]
image_table('Table A2 Illustrated profiles of the eight presentation product categories',rows)
h('A3 Five locally linked examples and production status',2)
p('The staff account names five examples but does not verify five locally grown or manufactured products. Local cultivation, finished-product manufacture, processing, packing and branding are different claims. One mood-related preparation was described as Singapore-made, with its identity unrecorded.')
reuse('Table A3 Locally linked examples retained from the presentation',oldtables[2])
h('A4 Five soup therapies retained from the presentation',2)
p('The five labels match slide 6. The staff separately named Dang Shen, Huang Qi, Yu Zhu, Huai Shan, red dates and goji as common soup ingredients, without supplying five complete recipes. These are maintenance and climatic-wellness positions rather than documented clinical recovery cases.')
reuse('Table A4 Soup labels ingredients and reported purposes',oldtables[3])
h('A5 Three comparatively lower-demand examples with illustrations',2)
p('This table preserves former Section 3.5 and presentation slide 8. It contains one named herb and two broad categories. Neither a verified bottom-three rank nor three distinct medicinal species was recorded. Broad categories cannot be given a single nature or meridian profile.')
note('Ban Zhi Lian’s image and traditional profile are database references, not extra staff testimony. The cabinet photograph illustrates the setting in which specialist materials are encountered and does not identify a particular low-selling herb. The ginseng picture illustrates tonic materials only, not an identified strong-tonic formula.')
low=[
('半枝莲 Ban Zhi Lian\nBarbated skullcup herb',IA/'barbated-skullcup-herb.jpg','Reference material\n(PolyU, n.d.-c)','Sweet, bitter; cold (reference profile).','Liver, Lung, Kidney (reference profile).','Reference: clears heat and toxin, resolves stasis and promotes urination. Staff: bought less often.','Traditional reference: sores, throat swelling and oedema. Staff discussed combinations but recorded no individual diagnosis, dose or outcome; rank unverified.'),
('Specialist herbs requiring combinations',PH/'photo_2026-09-13_10-49-57.jpg','Field cabinet context only\nNo second herb identified','Varies; materials not individually identified.','Varies; not recorded.','Purpose depends on the combination and assessed pattern.','Staff linked lower appeal to preparation, unfamiliarity and need for guidance. Category, not a second named product.'),
('大补方\nStrong tonic formulas',HA/'ginseng.jpg','Tonic material illustration only\n(PolyU, n.d.-h)','Formula dependent; no recipe identified.','Formula dependent; not recorded.','Presentation: intensive replenishment; no specific formula supplied.','Presentation linked lower appeal to preference for 清补 in local conditions. Climate is a retail interpretation, not an individual suitability assessment.')]
image_table('Table A5 Illustrated profiles of the lower-demand examples',low)
h('A6 Physician evidence and separate retail associations',2)
p('Physician presence was not clearly confirmed. Accordingly, eight physician prescriptions and eight physician-treated symptoms remain not established. The six associations below are staff-reported retail pairings retained from slide 9. Patient examination, exact formulations, doses and treatment durations were not recorded.')
reuse('Table A6 Retail symptom associations without confirmed clinical prescriptions',oldtables[5])
h('A7 Survey coverage and evidential status',2)
audit=json.loads((R/'_review/draft_sources/evidence_audit.json').read_text(encoding='utf-8'))['rows']
locations={'A':'A1; Sections 3.1 and 6.1','B':'A2; Section 4','C':'A3; Section 5.1','D':'A4; Section 3.2','E':'A5; Section 4.3','F':'A6; Section 6.1','G':'A6; Section 6.1'}
coverage=[
['A','Eight herb entries; nine reference profiles',locations['A'],'No verified twelve-month sales ranking.'],
['B','Eight product categories',locations['B'],'Exact products and comparative sales unknown.'],
['C','Five locally linked examples',locations['C'],'Cultivation and manufacture unverified by item.'],
['D','Five soup labels',locations['D'],'Complete recipes and all pack identities unconfirmed.'],
['E','One named herb and two categories',locations['E'],'No verified bottom-three ranking.'],
['F','Physician prescriptions not established',locations['F'],'Physician role not confirmed; no clinical cases recorded.'],
['G','Six separate retail associations',locations['G'],'Not eight physician-treated symptoms or case records.']]
table('Table A7 Coverage of the seven survey requirements',['Survey item','Record retained','Location','Evidence limit'],coverage,[.75,2.05,1.45,2.55])

d.add_page_break()
h('References')
refs=[x for x in oldrefs if not x.startswith('The Hong Kong Polytechnic University.')]
refs=[x.replace('Retrieved October 3, 2026','Retrieved October 4, 2026') for x in refs]
refs += [
'Accounting and Corporate Regulatory Authority. (n.d.). ACRA information on corporate entities (T) [Data set]. Data.gov.sg. Retrieved October 4, 2026, from https://data.gov.sg/datasets/d_72f37e5c5d192951ddc5513c2b134482/view (Records: Tong Keow Medicine and Provision Shop, UEN 06799800C; Tong Keow Medical Hall Pte. Ltd., UEN 201500103H.)',
'Amacha. (n.d.). Amacha herbal milk tea [Menu and brand website]. Retrieved October 4, 2026, from https://www.amacha.sg/',
'Angelynn T. (2026, January 5). This S’pore biz is turning TCM into milk tea—8 mths in, it now has 3 outlets & sold 150K+ cups. Vulcan Post. https://vulcanpost.com/907853/amacha-herbal-milk-tea/',
'Chin, S. F. (2024, May 26). Innovation amid tradition: How Chinatown merchants move with the times. The Straits Times. https://www.straitstimes.com/singapore/innovation-amid-tradition-how-chinatown-merchants-move-with-the-times',
'Chua, V., Feng, C.-C., & Ho, E. L.-E. (2025). Ageing in networks: Living alone but connected. Ageing & Society. Advance online publication. https://doi.org/10.1017/S0144686X25100329',
'Fei Fah. (n.d.). Red flower ointment 50 ml [Product photograph used as an external illustration]. Retrieved October 4, 2026, from https://feifah.com/zh/products/red-flower-ointment-50ml',
'Healthcare.com.sg. (n.d.). Tong Keow Medical Hall (Hougang Central). Retrieved October 4, 2026, from https://www.healthcare.com.sg/item/tong-keow-medical-hall-hougang-central/',
'Health Sciences Authority. (2025, January). Guidelines on Chinese Proprietary Medicines product listing (section 5). https://file.go.gov.sg/hsa-cpm-listing-fsc-guidelines.pdf',
'Health Sciences Authority. (2026c, March 13). Overview of dealer’s licences for Chinese Proprietary Medicines. https://www.hsa.gov.sg/chinese-proprietary-medicines/manufacturing-import-wholesale/dealers-licence/overview/',
'Health Sciences Authority. (2026d, May 29). Safety precautions when buying Chinese medicinal pills and capsules. https://www.hsa.gov.sg/announcements/safety-precautions-when-buying-chinese-medicinal-pills-and-capsules/',
'Housing & Development Board. (2024). Key statistics: HDB annual report 2023/2024 (pp. 11–12). https://www.hdb.gov.sg/-/media/hdb-pulse/reports/annual-reports-and-financial-statements/HDB-KS-FY23.pdf',
'Liu, Y., Yang, Q., & Hu, Y. (2026). Translation variations under legal constraints in the packaging information of traditional Chinese herbal medicine sold in Malaysia. International Journal of Multilingualism, 23(1), 973–1000. https://doi.org/10.1080/14790718.2025.2537184 (First published online August 11, 2025.)',
'Nanyang Polytechnic. (n.d.). From tradition to trend: NYP’s collaborative journey with Heng Foh Tong in revolutionising herbal drinks. https://www.nyp.edu.sg/industry/projects/revolutionise-herbal-drinks-heng-foh-tong',
'National Heritage Board. (n.d.). Tou Mu Kung. Roots. https://www.roots.gov.sg/places/places-landing/Places/national-monuments/tou-mu-kung',
'Singapore Department of Statistics. (n.d.). Coverage of Singapore retail trade industry 2021 [SSIC 2020 codes]. https://www.singstat.gov.sg/-/media/files/find_data/industry/coverage-retail.pdf',
'Singapore Department of Statistics. (2024). Resident population by planning area/subzone, age group and type of dwelling, June 2024 [Data set]. https://www.singstat.gov.sg/files/3bbefdea-b6fb-461d-97b0-ef20b04abd9f.xlsx',
'Singapore Department of Statistics. (2025). Resident population by planning area/subzone, age group and type of dwelling, June 2025 [Data set]. https://www.singstat.gov.sg/files/b96b9a33-3301-4f17-8eda-9db4d9e8fc4e.xlsx']
herbs=[('american-ginseng','American ginseng'),('barbary-wolfberry-fruit','Barbary wolfberry fruit'),('barbated-skullcup-herb','Barbated skullcup herb'),('chinese-date','Chinese date'),('chrysanthemum-flower','Chrysanthemum flower'),('common-yam-rhizome','Common yam rhizome'),('fragrant-solomonseal-rhizome','Fragrant solomonseal rhizome'),('ginseng','Ginseng'),('glossy-ganoderma','Glossy Ganoderma'),('grosvenor-momordica-fruit','Grosvenor momordica fruit'),('japanese-honeysuckle-flower','Japanese honeysuckle flower'),('milkvetch-root','Milkvetch root'),('tangshen','Tangshen')]
for i,(slug,title) in enumerate(herbs):refs.append(f'The Hong Kong Polytechnic University. (n.d.-{chr(97+i)}). {title}. Chinese Herbal Medicine Database. https://herbaltcm.sn.polyu.edu.hk/herbal/{slug}')
for tx in sorted(refs,key=lambda x:x.removeprefix('The ').lower()):
    pp=p(tx);pp.paragraph_format.left_indent=Inches(.25);pp.paragraph_format.first_line_indent=Inches(-.25);pp.paragraph_format.space_after=Pt(7)
    for run in pp.runs:run.font.size=Pt(10)
note('The staff interview, group presentation, presentation script and photographs are the group’s fieldwork records. Personal communication is cited in the text and excluded from the published reference list. Access dates for current websites are 4 October 2026. Secondary comparisons do not supply missing field-site findings.')

d.add_page_break()
h('Appendix B Fieldwork photographs')
for xml in photos:
    texts=xml.xpath('.//w:t')
    joined=''.join(n.text or '' for n in texts)
    if joined.startswith('Note.'):
        joined=joined.replace('Sections 3.4 and 4.1','Sections 3.1–3.2 and 4.1').replace('Table 4','Table A4')
        pp=p(joined)
        for run in pp.runs:run.font.size=Pt(10)
    else:d.element.body.insert(len(d.element.body)-1,xml)
for st in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:
    d.styles[st].font.color.rgb=RGBColor(0,0,0)
    for e in d.styles[st].element.findall('.//'+qn('w:color')):
        for k in ['themeColor','themeTint','themeShade']:e.attrib.pop(qn('w:'+k),None)
for sec in d.sections:
    for pp in sec.footer.paragraphs:
        for run in pp.runs:run.text=run.text.replace('First draft','Revised draft')
d.core_properties.title='Traditional Chinese Medicine at Tong Keow Healthcare: Localisation, everyday care and pattern differentiation'
d.core_properties.subject='GEC1044 fieldwork report revised from tutor feedback'
d.save(F)
alltext='\n'.join([x.text for x in d.paragraphs]+[c.text for t in d.tables for row in t.rows for c in row.cells])
(R/'_review/revision_research/revised_text.txt').write_text(alltext,encoding='utf-8')
print('SAVED',F)
print('paragraphs',len(d.paragraphs),'tables',len(d.tables),'inline pictures',len(d.inline_shapes),'words',len(alltext.split()))
print('reference count',len(refs))
