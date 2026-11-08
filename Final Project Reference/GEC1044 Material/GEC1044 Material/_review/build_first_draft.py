from pathlib import Path
import json, re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT

ROOT = Path(r'C:\Users\lukel\Downloads\GEC1044 Material')
OUT = ROOT / 'GEC1044_Tong_Keow_First_Draft.docx'
audit = [
 ['A','Presentation and staff account','Ginseng or American ginseng; Dang Shen; Huang Qi; Yu Zhu; Huai Shan; red dates; goji; monk fruit','Staff report with selected shelf corroboration','Eight presentation entries; first groups two herbs; no numerical 12 month ranking'],
 ['B','Presentation and interview','Ginseng tonics; monk fruit products; flower teas; soup packs; Lingzhi; liver care or mood support; Yin Qiao; medicated oils','Staff report and observation','Eight categories rather than identified SKUs; no audited popularity ranking'],
 ['C','Presentation and interview','Cactus; roselle; patent medicines; Five Flower Tea; monk fruit tea','Staff report','No item level origin or five verified local products; imported processing general claim'],
 ['D','Presentation slide 6 and interview','Qing Bu Liang; Dang Shen Huang Qi; Yu Zhu Huai Shan; goji red date; Five Finger Fig','Presentation synthesis and soup shelf observation','Five labels preserved; interview lists ingredients not complete recipes; photographs do not confirm all labels'],
 ['E','Interview and presentation','Ban Zhi Lian; combination dependent herbs; strong tonics','Staff report','One named herb and two categories; no bottom three ranking'],
 ['F','No physician verified','None','Missing evidence','Not established; cannot reconstruct from retail lists'],
 ['G','No physician verified','None; six separate retail pairings','Staff report','Retail associations not physician case or prescription records']
]
feedback = {
 'Clear analytical themes':'Sections 4 and 5 organise preventive food care, convenience, climate, lifestyle and multicultural localisation',
 'Connect lifestyle and packaged forms':'Sections 4.1 and 4.4 explain redistributed preparation and interpretive work',
 'Generational differences':'Section 4.1 attributes age patterns to one staff member and avoids abandonment claims',
 'Localisation and cultural change':'Sections 4.5 and 5 distinguish cultivation from production and retail translation',
 'Staff versus observation versus interpretation':'Method, table notes, figure captions and analytical qualifiers',
 'Chain and neighbourhood context':'Section 2 considers retail model and Hougang outlet selection without invented demographics',
 'More depth than slides':'Section 4.2 makes pattern differentiation a conceptual test of retail adaptation'
}
(ROOT / '_review' / 'draft_sources' / 'evidence_audit.json').write_text(json.dumps({'columns':['Required question','Evidence from fieldwork','Exact items identified','Evidence type','Confidence and limitation'],'rows':audit,'feedback':feedback},ensure_ascii=False,indent=2),encoding='utf-8')

d = Document()
s = d.sections[0]
s.page_width, s.page_height = Inches(8.5), Inches(11)
s.top_margin, s.bottom_margin = Inches(.8), Inches(.75)
s.left_margin, s.right_margin = Inches(.85), Inches(.85)
s.header_distance, s.footer_distance = Inches(.3), Inches(.3)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3','Caption']:
 st=d.styles[name]; st.font.name='Times New Roman'; st.font.color.rgb=RGBColor(0,0,0)
 st.element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'),'Microsoft YaHei')
 for key in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:
  st.element.rPr.rFonts.attrib.pop(qn('w:'+key),None)
 for border in list(st.element.findall('.//'+qn('w:pBdr'))): border.getparent().remove(border)
st=d.styles['Normal']; st.font.size=Pt(11); st.paragraph_format.line_spacing=1.15; st.paragraph_format.space_after=Pt(7)
for name,size in [('Title',24),('Subtitle',13),('Heading 1',15),('Heading 2',12),('Heading 3',11)]:
 st=d.styles[name]; st.font.size=Pt(size); st.font.bold=name.startswith('Heading'); st.paragraph_format.space_before=Pt(12); st.paragraph_format.space_after=Pt(6)
d.styles['Title'].paragraph_format.space_before=Pt(0)
d.styles['Caption'].font.size=Pt(10)
d.styles['Caption'].font.italic=False
f=s.footer.paragraphs[0]; f.alignment=WD_ALIGN_PARAGRAPH.RIGHT
f.add_run('First draft   |   ')
fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); f._p.append(fld)
for r in f.runs: r.font.size=Pt(9)

def p(text,style=None):
 para=d.add_paragraph(style=style)
 for i,part in enumerate(text.split('**')):
  r=para.add_run(part); r.bold=bool(i%2)
 return para
def h(text,level=1): return d.add_heading(text,level)
def table(title,heads,rows,widths):
 cap=p(title,'Caption'); cap.paragraph_format.keep_with_next=True
 t=d.add_table(rows=1,cols=len(heads)); t.autofit=False
 for c,w in zip(t.columns,widths): c.width=Inches(w)
 borders=OxmlElement('w:tblBorders')
 for edge in ['top','left','bottom','right','insideH','insideV']:
  e=OxmlElement('w:'+edge); e.set(qn('w:val'),'single'); e.set(qn('w:sz'),'4'); e.set(qn('w:color'),'D9D9D9'); borders.append(e)
 t._tbl.tblPr.append(borders)
 for j,txt in enumerate(heads): t.rows[0].cells[j].text=txt
 repeat=OxmlElement('w:tblHeader'); t.rows[0]._tr.get_or_add_trPr().append(repeat)
 for row in rows:
  cells=t.add_row().cells
  for j,txt in enumerate(row): cells[j].text=txt
 for ri,row in enumerate(t.rows):
  ns=OxmlElement('w:cantSplit'); row._tr.get_or_add_trPr().append(ns)
  for j,cell in enumerate(row.cells):
   cell.width=Inches(widths[j]); cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   pr=cell._tc.get_or_add_tcPr()
   mar=OxmlElement('w:tcMar')
   for edge,val in [('top','85'),('bottom','85'),('left','100'),('right','100')]:
    e=OxmlElement('w:'+edge); e.set(qn('w:w'),val); e.set(qn('w:type'),'dxa'); mar.append(e)
   pr.append(mar)
   if ri==0:
    sh=OxmlElement('w:shd'); sh.set(qn('w:fill'),'E8E8E8'); pr.append(sh)
   for par in cell.paragraphs:
    par.paragraph_format.space_after=Pt(0); par.paragraph_format.line_spacing=1.05
    for r in par.runs: r.font.size=Pt(10.5); r.bold=ri==0
 p('') .paragraph_format.space_after=Pt(0)
 return t

p('Traditional Chinese Medicine at Tong Keow Healthcare','Title')
p('Localisation everyday care and pattern differentiation','Subtitle')
p('GEC1044 Group Fieldwork Report   •   Complete first draft')
p('TD3 Group 2\nLou Yu Luke · Chang Tze Yi Othniel · Li Xudong\nCurtis Chang Kai Xian · Hu Zhixuan Shirley\nTutor Lin Shi Ting')
p('Field visit 13 September 2026\nBlock 809 Hougang Central #01-170 Singapore 530809\nDraft prepared 3 October 2026')
h('1 Introduction')
p('Our visit to Tong Keow Healthcare shows how Chinese medicinal knowledge can enter everyday life through soup ingredients, herbal teas, supplements and familiar household remedies. Raw herbs and packaged products occupied the same retail space. The staff member associated particular products with nourishment, fatigue, throat comfort and contemporary lifestyle concerns, while describing differences between older and younger customers. These findings suggest that continuity in Traditional Chinese Medicine (TCM) can depend on changes in the way consumers encounter and prepare it.')
p('This report examines that process through a single medicine hall in Hougang. We first address all seven requirements of the Medical Hall Product and Prescription Survey, then develop three connected arguments: changing formats can sustain engagement among younger consumers; food and retail access can create opportunities for cross-cultural contact; and Singapore’s environmental and social conditions shape how traditional ideas are presented. Our argument is that Tong Keow illustrates **continuity through adaptation**: inherited medicinal categories remain visible while their retail forms and meanings are adjusted to local conditions. One outlet cannot establish how TCM survives throughout Singapore, but it can reveal mechanisms through which tradition is made usable in a contemporary neighbourhood.')
p('A central question is what happens to **pattern differentiation and treatment according to the identified pattern 辨证论治** when medicinal knowledge is presented as a readily understood association between a complaint and a product. Clinical pattern differentiation concerns a person’s configuration of signs, symptoms and circumstances. The interview, by contrast, mainly documented retail associations. Keeping these levels distinct helps us explain both the accessibility of modern TCM products and the limits of what a retail field visit can establish.')

h('2 Fieldwork method and site context')
p('We conducted shop observation, took photographs and held a semi-structured interview with one staff member on 13 September 2026. Questions covered commonly purchased herbs, proprietary and wellness products, soup ingredients, sourcing, less popular items, customer profiles and quality. The presentation prepared after the visit serves as our main organised record; the interview transcript and photographs are used to corroborate or qualify it. The transcript contains recognition errors, so we paraphrase its clearer passages rather than reproduce uncertain quotations. The sample report on another institution informed structure only; none of its patient encounters or clinical observations is treated as our own evidence.')
p('Three evidence levels are identified throughout. **Staff reports** describe the interviewee’s account of demand, customer preferences and sourcing. **Direct observations** concern visible products, packaging and displays. **Our interpretations** connect those findings to course concepts and contextual research. We did not obtain numerical sales records, conduct a consumer survey, observe a diagnostic consultation or independently trace supply chains. A prominent shelf display demonstrates availability and merchandising, rather than sales volume or clinical effectiveness.')
p('Tong Keow operates as a retail chain with multiple outlets, as noted in the tutor feedback supplied with our fieldwork materials. We studied only its Hougang outlet. The photographs show products displayed along a neighbourhood shop frontage, combining medicinal materials with teas, grains, dessert ingredients and packaged soup preparations. This arrangement offers several reasons to enter the shop beyond seeking treatment for illness. The chain format also raises the possibility that branded packs and product selections reflect shared purchasing and merchandising practices; we did not compare outlets or interview management to test that possibility.')
p('The staff member described customers as mainly middle-aged and older, especially people in their forties and fifties, and mainly Chinese (Tong Keow staff member, personal communication, September 13, 2026). These are impressions rather than a measured demographic profile. The Hougang location and neighbourhood retail setting may influence who visits, but we did not collect residents’ age, ethnicity or income data. We therefore interpret the reported pattern as an outlet-specific observation rather than a representative account of younger people or ethnic groups across Singapore. Historically, Chinese medicine in Singapore developed through migration, community institutions and later professionalisation and regulation, providing a wider context for this neighbourhood encounter (Yang, 2022).')

h('3 Medical Hall Product and Prescription Survey')
p('The seven required questions are addressed below. Table order follows the presentation and is **not a verified rank**. Unless otherwise stated, the uses are traditional or retail-stated purposes recorded in the presentation and staff interview, not findings of clinical efficacy. The interview is cited as personal communication and is not included in the published reference list.')
h('3.1 Eight herbs identified as commonly sold',2)
p('Requirement A asks for eight best-selling herbs by sales volume over the preceding 12 months. Our materials identify eight entries but contain no transaction totals, quantities or reliable comparative order. Table 1 therefore records fieldwork-identified common sellers, without claiming a numerical annual ranking.')
table('Table 1  Eight herb entries in the fieldwork presentation', ['Herb and Chinese name','Traditional or staff described purpose','Evidence qualification'], [
 ['Ginseng / American ginseng\n人参／西洋参','Qi support and fatigue','Grouped as one presentation entry; these are distinct herbs, not interchangeable names.'],
 ['Dang Shen 党参','Qi support and digestion','Named in the interview as a common soup ingredient.'],
 ['Huang Qi 黄芪','Qi support; “immunity” in retail language','Named as a common soup ingredient; immunity is a staff claim.'],
 ['Yu Zhu 玉竹','Nourishing and moistening','Named among common soup ingredients.'],
 ['Huai Shan 淮山','Spleen and digestive support in TCM terms','Named among common soup ingredients.'],
 ['Red dates 红枣','Everyday nourishment','Named among common soup ingredients.'],
 ['Goji berries 枸杞','General wellness and nourishment','Named among common soup ingredients.'],
 ['Monk fruit 罗汉果','Throat and lung comfort; associated with local heat','Staff linked its appeal to the Singapore environment.']
 ],[2.05,2.05,2.7])
p('The first entry requires care: the presentation combines ginseng and American ginseng, while the cabinet photograph separately labels American ginseng. We preserve the presentation’s eight entries without treating the two materials as one botanical ingredient or inventing a ninth ranking. The overlap between medicinal materials and soup ingredients is analytically significant. Several herbs enter routine cooking rather than appearing only in a clinical prescription.')
h('3.2 Eight popular medical and wellness product categories',2)
p('Requirement B is answered at the category level because the presentation did not consistently identify brands, formulations or stock-keeping units. No comparative sales figures were supplied. Customer comments apply to broader formats and should not be read as a measured profile for each product.')
table('Table 2  Eight product categories and their reported uses',['Category and form','Main traditional or retail stated purpose','Customer pattern or use context'],[
 ['Ginseng tonics\nPrepared tonic products','Fatigue and Qi support; staff also mentioned immunity','Prepared format reduces handling of raw material; product-specific age distribution unknown.'],
 ['Monk fruit products\nFruit or prepared drinks','Throat and lung comfort; cooling or moistening positioning','Staff related demand to local heat; exact formulations varied or were not recorded.'],
 ['Flower and herbal teas\nDried brewing mixtures','Everyday wellness; purpose depends on mixture','Staff associated teas with younger customers and simple brewing.'],
 ['Soup packs\nPreselected dried ingredients','Nourishment and routine health maintenance','Convenient ingredient selection; cooking is still required for the photographed packs.'],
 ['Lingzhi supplements\nPrepared supplements','Marketed or described for “immunity”','Staff associated supplements with wellness concerns; no measured immune outcomes.'],
 ['Liver care and mood support products\nProprietary preparations','养肝 or 疏肝解郁 language; late nights and stress','Staff linked these products to lifestyle complaints; not evidence of liver disease or depression treatment.'],
 ['Yin Qiao type remedies\nProprietary cold remedies','Staff associated them with colds','Retail symptom association; no patient assessment or prescription observed.'],
 ['Medicated oils\nTopical preparations','Aches and injury related discomfort','Staff particularly associated these with older customers; examples included red medicated oils.']
 ],[1.9,2.3,2.6])
p('These categories combine traditional vocabulary, ordinary complaints and contemporary wellness language. “Qi support” and “immunity” may appear together in retail explanations, but they are not equivalent concepts. Similarly, a supplement category does not establish that a product prevents infection. The absence of exact formulations also prevents us from assigning every category to one regulatory class or judging its clinical indications.')
h('3.3 Five locally linked examples and production status',2)
p('Requirement C cannot be answered as five verified Singapore-grown or Singapore-manufactured items. The staff member described limited local cultivation, mentioned cactus and roselle as possible local examples, and stated that imported materials could be processed or packed in Singapore. A mood-related proprietary preparation was described as Singapore-made, but its exact identity and manufacturer were not recorded. This is useful evidence of a retail account of localisation, not an independently verified origin audit.')
table('Table 3  Locally linked examples in the presentation',['Example','Raw origin and grown in Singapore','Manufacture in Singapore','Processing packaging or brand link'],[
 ['Cactus\n仙人掌','Named as a possible locally grown example; origin of stock unknown','Not established','No specific product or producer identified.'],
 ['Roselle\n洛神花','Named as a possible locally grown example; origin of stock unknown','Not established','No specific product or producer identified.'],
 ['Patent medicines\n中成药','Imported ingredients discussed generally; item origin unknown','Staff described one mood-related product as Singapore-made; exact item unknown','Local processing and packing described generally; not verified for each product.'],
 ['Five Flower Tea\n五花茶','Not established','Not established','Locally linked in the presentation; item-specific processor, packer and brand unknown.'],
 ['Monk fruit tea\n罗汉果茶','Not established for the tea product','Not established','Locally linked in the presentation; item-specific processor, packer and brand unknown.']
 ],[1.45,1.9,1.65,1.8])
p('**[VERIFY]** Obtain item-level labels or supplier details for these five examples, including cultivation country, manufacturing site, processor, packer and brand owner. A Singapore company’s name or retail address alone cannot establish local cultivation or manufacture. No online product was substituted for an unidentified item from our visit. The defensible finding is that localisation may take place through selection, processing, packaging and selling imported materials; five locally produced items remain unverified.')
h('3.4 Five soup therapies recorded in the presentation',2)
p('Requirement D is addressed using the five labels in the presentation. The interview more clearly identifies six common ingredients—Dang Shen, Huang Qi, Yu Zhu, Huai Shan, red dates and goji—than five complete recipes. The photographs establish a substantial soup-pack display, but do not independently confirm every name or formula below. Named ingredients are therefore distinguished from a full ingredient list.')
table('Table 4  Five presentation soup labels and stated purposes',['Soup label','Ingredients available from the record','Purpose and main use'],[
 ['Qing Bu Liang 清补凉','Complete recipe not recorded','Light nourishment and climatic wellness; health maintenance in the presentation’s interpretation.'],
 ['Dang Shen and Huang Qi soup\n党参北芪补气汤','Dang Shen and Huang Qi are named; complete recipe unknown','Qi support and nourishment; maintenance rather than documented clinical recovery.'],
 ['Yu Zhu and Huai Shan soup\n玉竹淮山润燥汤','Yu Zhu and Huai Shan are named; complete recipe unknown','Moistening and nourishment; climatic wellness positioning.'],
 ['Goji and red date soup\n枸杞红枣养生汤','Goji and red dates are named; complete recipe unknown','Everyday nourishment and health maintenance.'],
 ['Five Finger Fig soup\n五指毛桃健脾汤','Five Finger Fig is named; other ingredients not recorded','Spleen and digestive support in traditional terms; maintenance positioning.']
 ],[2.2,2.2,2.4])
p('**[VERIFY]** Confirm the exact retail name and complete ingredient list of each of the five soup preparations with the shop. Table 4 preserves the presentation’s labels rather than reconstructing recipes from generic online formulas. No verified top-five sales ranking or post-illness recovery outcome was obtained.')
p('The staff member contrasted lighter replenishment 清补 with stronger tonification 大补, describing the former as more typical locally. This preference connects the soup findings to the less popular tonic category and to the climate discussion below. Figure 1 shows soup promotion through a family cooking image, while Figure 2 shows visible dried ingredients in branded packs. Together they support an interpretation of soup as an everyday vehicle for medicinal ideas. They do not prove that every displayed pack has a diagnosed therapeutic indication.')
h('3.5 Three examples of comparatively lower demand',2)
p('Requirement E asks for three least-used products. Although the interview did not establish a verified bottom-three ranking, the staff member and presentation identified the following lower-demand examples. Only one is a named herb; the others are broad categories.')
table('Table 5  Lower demand examples rather than a bottom three sales ranking',['Example','Available explanation','Limit of the answer'],[
 ['Ban Zhi Lian 半枝莲','Staff identified it as less frequently purchased and discussed combining herbs','One named material; volume and comparative rank unknown.'],
 ['Herbs needing specialist combinations','Preparation and selection can require knowledge or guidance','Category rather than a second named product; relative demand not quantified.'],
 ['Strong tonic formulas\n大补方','Presentation linked lower appeal to preference for lighter replenishment in local conditions','Broad formula category rather than a third identified product; climate explanation remains interpretive.']
 ],[1.8,2.6,2.4])
p('The evidence suggests that the effort and knowledge needed to use a product may matter alongside its traditional purpose. However, slow sales can also depend on price, stock selection or individual prescribing patterns. We did not measure those factors. The staff member’s remark that poorly selling items are less likely to be stocked also means the visible range may already exclude low-demand products.')
h('3.6 Physician prescriptions',2)
p('**Requirement F — Not established.** An in-house physician was not clearly confirmed during the visit. We therefore cannot reliably identify eight commonly prescribed herbs or prescriptions. The interview’s general references to common Chinese medicinal materials do not identify a physician, patient records, formula composition or prescription frequency. **[VERIFY]** Confirm whether this outlet has an in-house registered physician and, if so, obtain an appropriate aggregate account of common prescriptions. Until then, missing clinical findings are not replaced with retail lists.')
h('3.7 Physician treated symptoms and corresponding remedies',2)
p('**Requirement G — Not established.** Without a confirmed in-house physician or clinical case information, we cannot identify eight symptoms most frequently treated by that physician or their corresponding remedies. This uncertainty does not establish that the shop has no physician; it establishes the limit of our evidence. The Ministry of Health’s practitioner portal distinguishes practitioner registration from voluntary listing of TCM dispensers, reinforcing the need to identify the role of the person interviewed rather than assume clinical authority from employment in a medicine hall (Ministry of Health, 2026).')
h('3.8 Separate retail symptom and product associations',2)
p('The interview nevertheless supplied six retail associations, shown below. They provide evidence about how complaints are explained in the shop, and do not complete the physician-specific survey questions. No diagnostic consultation, dose, treatment duration or individual prescription was recorded.')
table('Table 6  Staff described retail associations',['Complaint or wellness concern','Associated retail product','Interpretive qualification'],[
 ['Colds','Yin Qiao type remedies','A broad complaint does not establish the pattern for which a formulation is suitable.'],
 ['Diarrhoea','Huoxiang Zhengqi type remedies','Staff association; no individual cause or pattern assessed.'],
 ['Fatigue or Qi deficiency language','Ginseng or Dang Shen','Fatigue alone does not demonstrate Qi deficiency.'],
 ['Perceived lower immunity','Lingzhi or supplements','Wellness claim rather than measured immune dysfunction.'],
 ['Late nights stress and long work hours','Liver care or mood support products','Retail lifestyle framing; no liver disease or mental health diagnosis established.'],
 ['Aches or injuries','Medicated oils','Reported topical retail use; no clinical injury assessment recorded.']
 ],[1.9,1.8,3.1])

h('4 What Tong Keow reveals about modern TCM in Singapore')
h('4.1 Everyday nourishment and changing forms of consumption',2)
p('The strongest direct evidence of everyday TCM is the coexistence of soup ingredients, grains, dessert materials and medicinal products. The staff member repeatedly named Dang Shen, Huang Qi, Yu Zhu, Huai Shan, red dates and goji as soup ingredients. Rather than confining medicinal knowledge to an illness episode, these products permit consumers to incorporate nourishment into familiar household routines. The cooking poster in Figure 1 reinforces this domestic setting. Our interpretation is that the medicine hall sells not only materials but also a practical way to make health maintenance part of a meal.')
p('This observation connects to health preservation 养生 and the course discussion of food and medicine. Chapter 2 of the Huangdi Neijing Suwen relates conduct to environmental rhythms and presents care before disorder becomes established as an ideal (Unschuld & Tessenow, 2011, pp. 45–57). The relevance is a concern with ongoing management of life, rather than a claim that a modern soup pack reproduces a classical instruction exactly. An earlier Singapore housing-estate survey likewise found that complementary and alternative medicine was used more for health maintenance than for illness treatment (Lim et al., 2005). That study provides historical context, not a measure of Tong Keow’s customers in 2026.')
p('The reported generational difference helps explain why product form matters. According to the staff member, younger customers bought fewer raw herbs and preferred teas, supplements and simpler preparations. Our photographs corroborate the availability of these formats, but not the ages or motivations of their purchasers. A packet can reduce the need to identify separate herbs, select quantities and seek ingredients from several containers. Brewing tea may also require less work than preparing a decoction. Packaged soup ingredients simplify selection while still requiring cooking; convenience is therefore a matter of degree, not a single category of ready-to-consume products.')
p('This changes how knowledge is distributed. Some work previously performed by a knowledgeable purchaser or household cook may be transferred to the packer’s selection and the retailer’s description. The consumer encounters a legible purpose such as nourishment or throat comfort rather than learning a full formula. Such changes can preserve engagement with medicinal ideas while reducing opportunities to learn their distinctions. The evidence supports a change in access and format, not the stronger claim that young people have abandoned TCM. It also does not establish whether younger consumers understand or value the underlying concepts in the same way as older customers.')
p('The photographs also complicate a simple story of modern products replacing traditional practices. Loose and sliced herbs remain visible alongside branded packs, and the packs themselves can contain dried materials that need cooking. Modernisation and traditional preparation therefore coexist within the same shop. Multi-buy offers on bottled products show a further commercial dimension: health-related goods are presented through familiar retail promotions. Such offers demonstrate merchandising, without establishing affordability for particular households or their effect on purchasing. Branding may make an unfamiliar ingredient easier to approach, but it can also encourage selection by a product’s stated purpose rather than a deeper understanding of its use.')
h('4.2 Pattern differentiation and the limits of retail translation',2)
p('The fieldwork becomes more analytically useful when examined through **辨证论治**, commonly rendered as treatment based on pattern identification. The World Health Organization (2022) distinguishes this process from merely attaching a treatment to a disease name: information from diagnostic examination is analysed to identify a pattern, which then informs the therapeutic approach. The four examinations are inspection 望, listening and smelling 闻, inquiry 问 and palpation 切. They bring together signs and symptoms rather than isolating a complaint from the person experiencing it. This describes a clinical principle; our visit did not document its application to a patient.')
p('Within that framework, a symptom such as fatigue is information to investigate, rather than a sufficient diagnosis. Assessment could consider the symptom’s course, accompanying manifestations, sleep, digestion and other findings. Heat and cold, excess and deficiency, and organ-system relationships are possible dimensions of the resulting interpretation. **辨证** concerns identifying the pattern; **论治** concerns deciding treatment on that basis. A complaint can therefore lead to different treatment approaches depending on its wider configuration, while apparently different complaints may share a pattern. This is an explanation of the principle, not a reconstruction of any Tong Keow customer’s condition.')
p('The retail association “fatigue → ginseng or Dang Shen” makes one traditional idea readily understandable: depletion can be discussed through Qi support. Yet the association does not establish that a person’s fatigue results from Qi deficiency, that the two herbs have identical properties, or that either belongs in an appropriate individual formula. The presentation’s grouping of ginseng and American ginseng demonstrates the same problem at the level of classification. A compact sales category can conceal distinctions that would matter when choosing a medicinal material. Similarly, “diarrhoea → Huoxiang Zhengqi” records how the staff answered a retail question; it does not document the diagnostic reasoning needed to justify a particular preparation.')
p('The climate argument must pass the same test. Singapore’s humidity can provide a context for discussing dampness in TCM, but it cannot diagnose dampness or damp-heat in everyone who lives here. A general preference for lighter soups also cannot establish that strong tonics are inappropriate for every individual. **Environmental localisation and individual pattern differentiation operate at different levels.** The first concerns which products a retailer makes available and how they are explained; the second concerns how a practitioner interprets a particular person’s condition. Keeping both in view allows us to analyse adaptation without turning climate or a lifestyle complaint into a universal prescription.')
p('Packaged forms are not inherently incompatible with 辨证论治. An identified pattern could inform the choice of a standard preparation, provided clinical judgement remains part of the process. Conversely, a raw-herb purchase does not by itself prove that differentiation occurred. The decisive issue is the relationship between assessment and selection, not whether an item is old, loose, branded or convenient. Our evidence shows accessible retail expressions of TCM reasoning, but leaves the degree of individualisation unknown. This is why the unconfirmed physician status is an analytical boundary as well as a missing survey answer.')
h('4.3 Adapting environmental medicine to a tropical setting',2)
p('The staff member linked monk fruit to throat comfort in Singapore and described lighter replenishment as more common than heavy tonification. The presentation also emphasised Qing Bu Liang, Yu Zhu and moistening soup preparations. These findings suggest that local environmental conditions form part of the explanation offered to shoppers. Singapore’s official meteorological account describes an equatorial climate with high temperatures, abundant rainfall and high humidity throughout the year. It nevertheless has monsoon and inter-monsoon periods, so the staff’s remark that Singapore lacks China’s four seasons should be understood as the absence of four sharply differentiated temperate seasons, not an absence of climatic variation (Meteorological Service Singapore, n.d.).')
p('The Suwen’s environmental framework makes this a question of interpretation rather than simple geographical transplantation. Chapter 2 relates bodily care and behaviour to seasonal conditions (Unschuld & Tessenow, 2011, pp. 45–57). In Singapore, the relevant question is how care responds to a persistently warm and humid setting, rather than how shoppers should copy every temperate seasonal prescription. The preference reported at Tong Keow can be read as one local response: familiar concepts of replenishment are retained, while the emphasis falls on lighter preparations suitable for everyday consumption as described by the staff.')
p('Yin and Yang help explain why more nourishment is not automatically better within the theoretical language used in the course. Heat and cold or excess and deficiency concern relationships requiring assessment; they do not support a universal equation of tropical heat with bodily heat. Likewise, moistening and managing dampness are different therapeutic ideas. We cannot treat every cooling tea, moistening ingredient and light soup as the same remedy simply because each appears in a hot climate. The presentation identifies a local retail emphasis; it does not establish the internal properties or clinical suitability of every formulation.')
p('Five Phases 五行 becomes relevant where the record uses spleen-related digestive support and liver-related mood language. In the course’s correspondence framework, spleen and Earth and liver and Wood describe functional relationships rather than isolated anatomical organs. This helps explain why digestion, nourishment and mood can be discussed through organ-system terms. It does not prove that Huai Shan repairs an anatomical spleen or that a liver-care product treats biomedical liver disease. Nor did the staff articulate a complete Five Phases diagnosis. We use this framework to clarify the language surrounding products, while treating a damp-heat explanation of local demand as a plausible interpretation that remains untested.')
h('4.4 Lifestyle pressure convenience and complementary care',2)
p('The staff member connected late nights, long work hours, stress and prolonged phone use to demand for liver-care or mood-support preparations. This account extends the convenience argument: the same routines that make preparation difficult may also supply the complaints around which wellness products are positioned. A packaged preparation can translate a diffuse concern about tiredness or stress into a manageable purchase. The fieldwork therefore suggests a relationship between everyday pressures and changes in consumption, although it cannot establish that those pressures caused particular sales or that customers experienced relief.')
p('Current labour statistics prevent an exaggerated account of increasing work intensity. The Ministry of Manpower (2026) reported average usual weekly hours of 41.4 among employed residents in 2025, down from 44.2 a decade earlier. This does not measure the stress of individual customers, and averages do not describe every schedule. It does mean our report should avoid claiming that Singaporeans’ working hours are continually rising. The staff’s account is evidence of a way contemporary concerns are interpreted in the shop; the national figures supply context rather than confirmation of that account.')
p('The phrase 疏肝解郁, broadly concerning soothing liver-related constraint in TCM language, is especially useful for analysing this translation. It brings a contemporary mood concern into a traditional functional vocabulary. Without an exact product label or a diagnosed case, however, we cannot conclude that the shop treats depression, that screen use causes a specific pattern, or that a liver-care preparation addresses a biomedical hepatic disorder. 辨证论治 highlights what is missing between a general lifestyle narrative and an individual treatment decision: the actual assessment of the person and justification of the remedy.')
p('Preventive or complementary use is also more defensible than assuming replacement of biomedical care. A 2025 Ministry of Health speech reported that nearly 40% of TCM users identified in the 2022 National Population Health Survey combined TCM and Western medicine for the same condition (Ministry of Health, 2025). This establishes a wider context of combined use, not the behaviour of our interviewee’s customers. We did not ask consumers whether they sought natural remedies, feared side effects of biomedical medicines or used products alongside prescribed treatment. These remain possible motivations, rather than fieldwork findings.')
p('The staff’s emphasis on freshness, quality and sulphur-free materials indicates that trust is part of the retail explanation. Figure 3 records an American ginseng label and a sulphur-free Dang Shen claim; the photograph verifies the label’s presence, not the production method or safety of the material. Perceived naturalness similarly cannot establish absence of risk. HSA’s health-supplement claims guidance rejects implying that a product is safe simply because it is natural (Health Sciences Authority, 2026a). Its explanation of Chinese Proprietary Medicine regulation emphasises safety and quality controls and does not treat listing as proof of efficacy (Health Sciences Authority, 2026b). These distinctions matter to interpretation because convenience and reassuring labels can increase accessibility without resolving questions of individual suitability.')
h('4.5 Local processing and a multicultural retail space',2)
p('The sourcing discussion complicates the meaning of local TCM. The staff member described imported raw materials, particularly from China, alongside local processing, packing and some proprietary manufacture. The cabinet’s geographical labels also show that origin forms part of merchandising, although we did not verify those claims. The five locally linked examples cannot be converted into five verified locally grown products. Instead, they prompt a broader question: where in the chain from cultivation to consumption does Singapore contribute to a product’s form and meaning?')
p('One answer supported by the visit is retail selection and packaging. Visible Tong Keow branded bags collect recognisable ingredients into preparations for household use. Even when ingredients are imported, their arrangement, naming, portions and promotion can make them locally usable. The stronger statement that every photographed pack was processed or manufactured in Singapore remains unproven. Localisation should therefore be understood as several possible activities, with the evidence for each stated separately. Cultural change can accompany this process when an ingredient is encountered through a familiar meal, a convenience format or a wellness label rather than through specialist terminology.')
p('The staff member also described Malay customers buying dessert ingredients and Indian customers buying nuts, alongside a predominantly Chinese customer base. The product range makes such overlap plausible: foods can be purchased for culinary reasons without accepting a medical theory. We did not independently determine customers’ ethnicity, interview them about beliefs or measure transactions by group. The evidence suggests that the medicine hall can serve people beyond an exclusively Chinese clientele, but does not demonstrate universal adoption of TCM or an effect on racial harmony. Shared shopping space and shared therapeutic interpretation are different claims.')
p('An external example shows how businesses may make products accessible across dietary requirements. Eu Yan Sang’s Singapore store provides a halal-certified product category, including preparations using ingredients such as goji and red dates (Eu Yan Sang, n.d.). This is evidence of the company’s own market positioning and product listings; it does not establish halal status at Tong Keow. For our case, the more modest argument is that medicinal and culinary materials can circulate across cultural boundaries through everyday consumption. Understanding that circulation requires attention to product use, certification and consumer interpretation, rather than assuming that ethnic identity predicts a fixed set of purchases.')

h('5 Discussion of continuity through adaptation')
p('Taken together, the findings suggest that continuity involves both retained ideas and changed practical arrangements. Dang Shen, Huang Qi, nourishment, spleen support and liver-related language remain recognisable. Teas, supplements and branded soup packs alter how those ideas are selected, prepared and communicated. The report’s themes are consequently connected: everyday preventive care creates a place for soups; convenience changes the effort required to use them; local climate helps shape the retailer’s account of their appeal; and packaging and food use can broaden the routes through which consumers encounter medicinal materials.')
p('This understanding is consistent with the course’s historical treatment of TCM as a tradition shaped by selection and adaptation rather than an untouched inheritance (Unschuld, 2018). Yang’s (2022) Singapore history similarly situates Chinese medicine within changing social and institutional conditions. Tong Keow adds a small-scale view of this process at the retail counter. Its mixed range encourages contact through ordinary needs, while staff explanations connect those needs to traditional and contemporary categories. The case therefore supports an account of adaptation as an ongoing practice, rather than a simple division between traditional raw herbs and modern commercial products.')
p('辨证论治 prevents that argument from becoming a celebration of every retail simplification. A product may retain traditional terminology while the consumer’s access to diagnostic reasoning remains limited. At the same time, convenience does not necessarily eliminate individualisation, because a clinician could select a prepared product after assessment. Our fieldwork cannot determine which of these relationships predominates at this outlet. The strongest conclusion is that retail adaptation preserves visible elements of TCM while changing where knowledge and decision-making may reside—among the packer, staff member, household cook, consumer and, where present, practitioner.')

h('6 Fieldwork limitations')
p('This is a qualitative study of one outlet, one visit and one staff interview. We lack sales records, a verified 12-month ranking, a numerical bottom-three list and item-level manufacturing documentation. Customer age and ethnicity are largely staff-reported, and neither consumer beliefs nor treatment outcomes were investigated. A chain outlet’s stock selection and neighbourhood location may influence the observed range and reported clientele. We cannot generalise those patterns to all Tong Keow outlets, all medicine halls or all Singapore residents.')
p('The presentation also condenses the raw record. Its first herb entry groups two different materials, its local-products section mixes origin and processing claims, and its soup labels are more specific than the interview’s ingredient list. Tables 1, 3 and 4 retain the useful findings while exposing those limits. The unconfirmed physician status means that professional prescriptions and treated symptoms remain not established. External research contextualises climate, history, regulation and complementary use; it is not used to fill missing field-site answers. Follow-up would be most valuable if it confirmed the physician’s role, identified the exact soup and local-product labels, and obtained a defensible account of demand without disclosing individual patient information.')

h('7 Conclusion')
p('Tong Keow Healthcare offers a useful case of how TCM becomes part of contemporary everyday life in Singapore. The visit documented common herbs, eight product categories, locally linked examples, soup preparations and lower-demand categories, while also revealing the limits of retail evidence. Food use and convenience help explain how traditional ideas remain available to consumers with different routines. The staff’s emphasis on lighter replenishment, lifestyle-related wellness concerns and a varied clientele illustrates local interpretation, while leaving important claims about production, sales and individual treatment unverified.')
p('The central insight is that adaptation can sustain engagement with TCM while altering the depth and setting of that engagement. **辨证论治 supplies the critical distinction between a recognisable retail association and a treatment justified by an individual’s pattern.** It allows us to discuss localisation without diagnosing all Singapore residents from their climate, equating fatigue with Qi deficiency or treating branded products as clinical prescriptions. This single case suggests that modern TCM is maintained through changing forms of access and use, with continuity depending not only on retaining ingredients but also on how their meanings and applications are understood.')

d.add_page_break()
h('References')
refs=[
 ('Eu Yan Sang. (n.d.). ', 'Shop halal products.', ' Retrieved October 3, 2026, from https://www.euyansang.com.sg/en/halal-2/'),
 ('Health Sciences Authority. (2026a, May 4). ', 'Health supplement claims.', ' https://www.hsa.gov.sg/health-supplements/claims/'),
 ('Health Sciences Authority. (2026b, April 6). ', 'How Chinese Proprietary Medicines are regulated by HSA.', ' https://www.hsa.gov.sg/announcements/how-chinese-proprietary-medicines-are-regulated-by-hsa/'),
 ('Lim, M. K., Sadarangani, P., Chan, H. L., & Heng, J. Y. (2005). Complementary and alternative medicine use in multiracial Singapore. ', 'Complementary Therapies in Medicine, 13', '(1), 16–24. https://doi.org/10.1016/j.ctim.2004.11.002'),
 ('Meteorological Service Singapore. (n.d.). ', 'Climate of Singapore.', ' https://www.weather.gov.sg/climate-climate-of-singapore'),
 ('Ministry of Health. (2025, July 6). ', 'Speech by Mr Ong Ye Kung, Minister for Health, at the forum on the use of evidence-based Traditional Chinese Medicine in Western medicine practice.', ' https://www.moh.gov.sg/newsroom/speech-by-mr-ong-ye-kung--minister-for-health--at-the-forum-on-the-use-of-evidence-based-traditional-chinese-medicine-in-western-medicine-practice/'),
 ('Ministry of Health. (2026, February 10). ', 'About.', ' https://hpp.moh.gov.sg/tcm-practitioners/about/'),
 ('Ministry of Manpower. (2026, February 3). ', 'Written answer to PQ on moderating working hours.', ' https://www.mom.gov.sg/newsroom/parliament-questions-and-replies/2026/0203-written-answer-to-pq-on-moderating-working-hours'),
 ('Unschuld, P. U. (2018). ', 'Traditional Chinese medicine: Heritage and adaptation', ' (B. Andrews, Trans.). Columbia University Press. https://cup.columbia.edu/book/traditional-chinese-medicine/9780231175012/'),
 ('Unschuld, P. U., & Tessenow, H. (2011). ', 'Huang Di nei jing su wen: An annotated translation of Huang Di’s Inner Classic—Basic Questions', ' (Vol. 1). University of California Press.'),
 ('World Health Organization. (2022). ', 'WHO international standard terminologies on traditional Chinese medicine.', ' https://www.who.int/publications/i/item/9789240042322'),
 ('Yang, Y. (2022). A brief history of Chinese medicine in Singapore. In V. Lo & M. Stanley-Baker (Eds.), ', 'Routledge handbook of Chinese medicine', ' (pp. 524–536). Routledge. https://doi.org/10.4324/9780203740262-42')
]
for first,title,last in refs:
 par=d.add_paragraph(); par.paragraph_format.left_indent=Inches(.3); par.paragraph_format.first_line_indent=Inches(-.3); par.paragraph_format.space_after=Pt(9)
 par.add_run(first); par.add_run(title).italic=True; par.add_run(last)
p('Source note. The staff interview, group presentation and photographs are our fieldwork records. Personal communications are cited in the text rather than the reference list. Course readings inform the analysis through the published works cited above. The report on a different TCM institution was used only as a structural reference.')

figs=[
 ('Figure 1','Soup promotion in the neighbourhood retail setting','photo_2026-09-13_10-49-49.jpg','The shop-front soup display uses a family cooking image and contains branded packs alongside other food and medicinal materials. This supports the discussion of domestic nourishment and everyday access in Sections 3.4 and 4.1; it does not demonstrate a sales ranking or the recipes in Table 4.'),
 ('Figure 2','Preselected dried soup ingredients in branded packs','photo_2026-09-13_10-50-00.jpg','Visible dried materials and soup-pack labels illustrate convenience through ingredient selection and packaging. The photographed products still require preparation. The display corroborates the soup category, without independently confirming all five presentation labels or local manufacturing status.'),
 ('Figure 3','Herb labels and retail quality claims','photo_2026-09-13_10-49-57.jpg','The cabinet separately labels American ginseng and displays a sulphur-free Dang Shen claim. Labels offer evidence of retail classification and quality positioning. They do not independently establish botanical authenticity, production method, safety or an audited supply chain.')
]
for idx,(num,title,file,note) in enumerate(figs):
 d.add_page_break()
 if idx==0: h('Appendix Fieldwork photographs')
 cap=p(num); cap.runs[0].bold=True; cap.paragraph_format.keep_with_next=True
 pp=p(title); pp.runs[0].italic=True; pp.paragraph_format.keep_with_next=True
 imagep=d.add_paragraph(); imagep.alignment=WD_ALIGN_PARAGRAPH.CENTER
 imagep.add_run().add_picture(str(ROOT/'photo'/file),width=Inches(5.2))
 p('Note. '+note+' Photograph by the group, Tong Keow Healthcare, 13 September 2026.','Caption')

d.core_properties.title='Traditional Chinese Medicine at Tong Keow Healthcare'
d.core_properties.subject='GEC1044 group fieldwork report first draft'
d.core_properties.author='TD3 Group 2'
d.save(OUT)
alltext='\n'.join(p.text for p in d.paragraphs)+'\n'+'\n'.join(c.text for t in d.tables for row in t.rows for c in row.cells)
(ROOT/'_review'/'draft_sources'/'draft_text.txt').write_text(alltext,encoding='utf-8')
print(json.dumps({'output':str(OUT),'words_approx':len(alltext.split()),'tables':len(d.tables),'images':len(d.inline_shapes),'verify_flags':alltext.count('[VERIFY]')},indent=2))
