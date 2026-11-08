from pathlib import Path
from copy import deepcopy
import shutil, re, json, hashlib
from docx import Document
from docx.oxml.ns import qn

root = Path(__file__).resolve().parents[1]
f = root / 'GEC1044_Tong_Keow_First_Draft.docx'
backup = root / '_review/GEC1044_Tong_Keow_before_readability_revision.docx'
if not backup.exists(): shutil.copy2(f, backup)
d = Document(backup)
pp = d.paragraphs
original_images = len(d.inline_shapes)
original_main_words = sum(len(p.text.split()) for p in pp[:72])

def rewrite(p, value):
    size = p.runs[0].font.size if p.runs else None
    p.clear()
    for part in re.findall(r'[\u3400-\u9fff]+|[^\u3400-\u9fff]+', value):
        r = p.add_run(part)
        if size: r.font.size = size
        if re.search(r'[\u3400-\u9fff]', part):
            chosen_font = 'Microsoft YaHei' if part == '辨证论治' else 'SimSun'
            r.font.name = chosen_font
            r._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), chosen_font)

changes = {
1: 'Everyday care convenience and localisation',
6: 'The report brings the group’s fieldwork findings together around everyday care, convenience and localisation. Appendix A retains the detailed survey records and illustrated tables.',
8: 'At Tong Keow’s Hougang outlet, dried herbs and packaged soups sit alongside grains and other everyday foods. During our visit, a staff member described customers buying products for nourishment, throat comfort, fatigue and concerns about their daily routines. This combination of food shopping and health care is the starting point of our report. We explore how a neighbourhood medicine hall brings Traditional Chinese Medicine (TCM) into ordinary life.',
9: 'Our argument is that TCM continues through changes in how people encounter and use it. Familiar soup ingredients connect it to household meals. Preselected packs and prepared products make it easier to buy and prepare. Local branding, manufacturing and a mixed food range give it a place in Singapore’s retail setting. The following sections develop these themes using our observations, the staff interview and relevant literature. Appendix A contains the full survey findings.',
11: '2 Fieldwork and the neighbourhood medicine hall',
12: '2.1 How we conducted the fieldwork',
13: 'We visited Tong Keow on 13 September 2026, photographed the displays and conducted a semi-structured interview with one staff member. We used the interview transcripts, presentation script and photographs to prepare this report. Where the transcripts contain recognition errors, we paraphrase the clear statements. References to the staff member refer to this interview (Tong Keow staff member, personal communication, September 13, 2026).',
14: 'Throughout the report, “the staff member described” refers to the interview, while descriptions of displays refer to our photographs. Phrases such as “we read this as” introduce our analysis. Published sources provide historical, demographic and industry context. The staff’s descriptions of popular and lower-demand products are informal accounts; we did not collect sales records or interview customers.',
15: '2.2 Tong Keow and its mixed retail model',
16: 'The group presentation traces Tong Keow’s original Toa Payoh shop to 1968, consistent with a directory’s account of its fiftieth anniversary in 2018. The business records have later dates: Tong Keow Medicine and Provision Shop was registered on 29 March 1975, and Tong Keow Medical Hall Pte. Ltd. was incorporated on 1 January 2015. Both list 70 Lorong 4 Toa Payoh #01-333, Toa Payoh Vista, as their registered address. Their business classifications cover Chinese medicine shops and provision or convenience stores (codes 47723 and 47102). This helps explain the combination of medicinal and food products in the shop (Accounting and Corporate Regulatory Authority [ACRA], n.d.; Healthcare.com.sg, n.d.; Singapore Department of Statistics [DOS], n.d.).',
17: 'The tutor described Tong Keow as a chain, and the directory links its Toa Payoh and Hougang outlets. At Hougang, we photographed Tong Keow branding on soup packs alongside herbs, grains and other foods. We read this as a medicine hall organised around both medicinal and culinary shopping. The branding connects the branch to the wider business, although we did not investigate how the branches buy or assemble their stock.',
18: '2.3 Hougang and the customers described by staff',
19: 'The staff member described customers as mainly Chinese, middle-aged and older, including people in their forties and fifties. Hougang’s residential setting provides useful context. The planning area had 228,140 residents in June 2024. HDB separately reported 57,557 dwelling units and 165,450 residents in its Hougang flats as at 31 March 2024. These totals cover different housing populations (DOS, 2024; Housing & Development Board [HDB], 2024, pp. 11–12).',
20: 'Hougang Central, the smaller subzone around the outlet, had about 4,620 residents in June 2025. Using the official rounded age-band totals, around 1,070 were aged 65 or above, roughly 23% of the population (DOS, 2025). This places the shop within a neighbourhood with a substantial older population, alongside the middle-aged customers described by staff.',
21: 'Chua et al. (2025) provide another view of neighbourhood life. Their 647 Hougang respondents had an average age of 69 and had lived in the area for an average of 22 years. Seventeen per cent lived alone, compared with 15% of 552 respondents in Taman Jurong; that difference was not statistically significant. The long residence in this sample gives context to our reading of Tong Keow as part of an established neighbourhood, although the study did not examine shopping at the outlet.',
22: 'Hougang also has a history of Teochew settlement, recorded in the National Heritage Board’s account of Tou Mu Kung and its fishing, farming and rubber-growing community (National Heritage Board [NHB], n.d.). Together, this history and the residential setting help us understand the place of a Chinese medicine hall in local community life. The staff’s account remains our source for the shop’s current customer mix.',
24: '3.1 Herbs in household meals',
25: 'The staff member named Dang Shen, Huang Qi, Yu Zhu, Huai Shan, red dates and goji as common soup ingredients. The presentation also included ginseng/American ginseng and monk fruit among its eight common-herb entries. Table A1 gives their traditional profiles and separates the two kinds of ginseng. In the shop, prepared ingredient packs and a family cooking image on the soup display placed these materials in the familiar setting of a household meal (Figures 1–2).',
26: 'We read this overlap between herbs and food through the ideas of nourishing life, 养生, and medicine and food sharing a source, 药食同源. Soup offers a way to encounter TCM through cooking and everyday nourishment. Lim et al.’s (2005) survey of complementary and alternative medicine in multiracial Singapore also identified health maintenance as a significant reason for use. Yang’s (2022) history places Chinese medicine within Singapore’s changing community and institutional life. These readings help explain why the food side of the medicine hall matters to our fieldwork.',
27: '3.2 Soup packs and light nourishment',
28: 'Our presentation organised the soup findings into five labels: Qing Bu Liang 清补凉, Dang Shen–Huang Qi soup 党参北芪补气汤, Yu Zhu–Huai Shan soup 玉竹淮山润燥汤, goji–red date soup 枸杞红枣养生汤 and Five Finger Fig soup 五指毛桃健脾汤. Table A4 retains these labels and the ingredients available in our records. The interview named common ingredients, but we did not obtain complete recipes for all five soups.',
29: 'The staff account and presentation associated these soups with digestion, moistening and light nourishment, 清补. This is an everyday approach to replenishment, distinct from the stronger tonification described as 大补. In our reading, the soup packs bring this language into ordinary meals. Traditional references to the Spleen and Liver describe TCM functions and relationships, rather than exact equivalents of biomedical organs (World Health Organization [WHO], 2022).',
30: '3.3 Singapore weather and the appeal of lighter soups',
31: 'The staff member linked monk fruit’s popularity and lighter soups to Singapore’s environment. Meteorological Service Singapore describes high temperatures, abundant rainfall and high humidity throughout the year, with monsoon and inter-monsoon periods (Meteorological Service Singapore [MSS], n.d.). The presentation’s phrase “without four distinct seasons” describes this tropical setting in broad terms. The link between the weather and product demand comes from the staff member’s explanation.',
32: 'The Suwen reading connects seasonal habits with maintaining health (Unschuld & Tessenow, 2011, pp. 45–57). We read the staff’s explanation as a local use of this environmental reasoning: lighter soups and cooling drinks are discussed in relation to Singapore’s weather. The descriptions remain distinct—for example, Yu Zhu is associated with moistening dryness, rather than removing dampness.',
35: '4.1 Easier preparation and the staff account of younger buyers',
36: 'The staff member described younger customers as buying fewer raw herbs and preferring teas, supplements and simpler preparations. Table A2 retains the eight categories from our presentation, ranging from ginseng tonics and herbal teas to soup packs, mood-support products and medicated oils. This account gives us a view of changing purchases from behind the counter; customer interviews would be needed to explore the reasons for those choices.',
37: 'The packaged products show what convenience means in practice. In a dried soup pack, someone has already selected and portioned the ingredients, leaving the buyer to cook them. Staff can explain the pack’s intended use, while the household completes the preparation. Capsules offer another form, with less preparation at home. The photographed multi-buy promotion adds a familiar retail feature to the soup display. Convenience here concerns the work involved in choosing and preparing a product, as well as its packaging.',
39: 'Other businesses offer useful comparisons. Nanyang Polytechnic describes Heng Foh Tong’s redesign of herbal drinks for millennials (Nanyang Polytechnic [NYP], n.d.). Amacha markets TCM-inspired milk teas, and a founder interview reported more than 150,000 cups sold in eight months (Amacha, n.d.; Angelynn T., 2026). Teck Soon’s owner reported a 30% sales increase after moving herbs from drawers to storefront displays in 1982 (Chin, 2024). Eu Yan Sang also offers a halal product category (Eu Yan Sang, n.d.). These institutional, promotional and media accounts describe attempts to change how customers encounter herbal goods. They provide industry comparisons for our convenience theme, rather than a survey of young Singaporeans or Tong Keow’s customers.',
40: '4.3 Products for daily pressures and products needing more guidance',
41: 'The staff member associated late nights, long work hours, stress and prolonged phone use with liver-care or mood-support products. The supplied photograph shows Nature’s Green Mind Soothe Capsules as an example, although the interview did not name a brand. Its packaging uses the familiar TCM language of soothing Liver-related constraint, 疏肝解郁. We read this as a way of presenting a product through concerns about daily life. “Liver” in this description refers to the TCM vocabulary discussed earlier.',
42: 'The staff’s account of work pressure needs to be read alongside broader labour data. Average usual weekly working hours among employed residents fell from 44.2 a decade earlier to 41.4 in 2025 (Ministry of Manpower [MOM], 2026). The interview therefore concerns staff impressions of customers’ routines and stress, rather than a national increase in working hours.',
43: 'The lower-demand examples point to the importance of preparation and guidance. The presentation listed Ban Zhi Lian 半枝莲, specialist herbs used in combinations and strong tonic formulas 大补方 (Table A5). Staff linked their lower appeal to unfamiliarity and the effort of preparing them, while the presentation also discussed the suitability of stronger tonics in Singapore’s climate. Staff said that poorly selling items were stocked in smaller quantities. We read these findings as a practical distinction between products that fit easily into daily routines and those that require more explanation or preparation.',
44: '5 Localisation through products packaging and cultural contact',
45: '5.1 Imported materials and locally made products',
46: 'The staff member described raw materials as coming mainly from China, citing variety and cost, with limited local cultivation. Our presentation retained five locally linked examples: cactus 仙人掌, roselle 洛神花, patent medicines 中成药, Five Flower Tea 五花茶 and monk-fruit tea 罗汉果茶 (Table A3). Their links to Singapore differ. For the pictured Nature’s Green Mind Soothe Capsules, the Health Sciences Authority (HSA) lists Tong Jum Chew as manufacturer and Singapore as the manufacturing country (HSA, 2025b). This is a locally manufactured finished medicine; the origins of its ingredients were not recorded.',
47: 'Tong Keow branding and preselected soup materials also give imported herbs a local retail form. We read localisation here as the work of choosing ingredients, portioning them, naming their uses and presenting them for Singapore shoppers. Staff described local processing and packing, although we did not trace the soup packs’ supply chain. Cultivation, manufacture and packaging are separate parts of this process, which is why Table A3 records them separately.',
48: 'Local manufacture and assembly of finished Chinese Proprietary Medicines (CPM) sit within Singapore’s regulatory framework. HSA requires the relevant dealer licences and product listing, with manufacturing and assembly facilities subject to licensing and Good Manufacturing Practice requirements (HSA, 2026c, 2026d). This provides context for the locally made capsule example. Raw herbs, foods and soup packs need to be considered according to their own product categories.',
49: '5.2 Packaging and the language of trust',
50: 'Packaging has a practical role in making medicines understandable to buyers. HSA’s CPM guidelines require full labelling in English, with any additional language corresponding to it. Labels must include product and ingredient information, batch and expiry details, and the relevant manufacturer, importer or assembler information (HSA, 2025a, section 5). HSA also distinguishes product listing from an assessment of therapeutic efficacy (HSA, 2026b). These rules shape how finished medicines are presented in Singapore.',
51: 'Liu et al. (2026), studying Chinese herbal medicines sold in Malaysia, discuss how legal requirements shape translated names and therapeutic statements. Their study offers a regional comparison for the relationship between medical vocabulary and consumer communication. In our reading, packaging helps carry that vocabulary into a retail setting, where a buyer encounters a named product and a short description of its use. Singapore’s own requirements remain the relevant rules for Tong Keow.',
52: 'The staff member also emphasised fresh colour and sulphur-free materials. Our cabinet photograph includes a sulphur-free Dang Shen label and a separate American ginseng label (Figure 3). These are examples of the quality information presented to shoppers. We read them as part of how the shop invites trust in its products. HSA’s guidance on supplement claims cautions against treating “natural” as a guarantee of safety (HSA, 2026a).',
53: '5.3 Different shoppers in a shared space',
54: 'The staff member described Malay customers buying dessert ingredients and Indian customers buying nuts, alongside a largely Chinese clientele. We did not interview these customers, so their purchases enter the report through the staff account. The food and medicinal range gives people different reasons to visit the same shop.',
55: 'We read this shared space as a form of everyday cultural contact. A shopper can buy a dessert ingredient without using it as medicine, while another buys a product for nourishment. The medicine hall can therefore become familiar through overlapping shopping routines, even when customers understand its products differently. This develops the presentation’s account of cultural change through the ordinary uses of the shop.',
56: '6 Bringing the findings together',
57: '6.1 Household care and clinical practice',
58: 'Our visit centred on retail advice and household care. Clinical TCM also involves assessing an individual’s signs and symptoms before selecting treatment, a process known as 辨证论治, or pattern differentiation and treatment (WHO, 2022). For example, the ginseng and American ginseng profiles in Table A1 differ in their traditional properties. The staff’s pairing of fatigue with a tonic in Table A6 is best read as a retail explanation; we did not observe a clinical consultation.',
59: 'People may also use TCM alongside other forms of care. MOH reported that nearly 40% of TCM users in the 2022 National Population Health Survey combined TCM and Western medicine for the same condition (Ministry of Health [MOH], 2025). We did not ask Tong Keow’s customers about their treatment choices, but this wider context reminds us that a purchase at a medicine hall can be one part of a person’s health care.',
61: '6.2 How the shop brings TCM into everyday life',
62: 'Food use gives herbs a familiar purpose, preselected packs reduce the work of choosing ingredients, and packaging explains their intended uses. Local branding and manufacture connect some products to Singapore’s businesses and regulatory setting. Together, these changes help people encounter TCM through ordinary cooking, shopping and daily care.',
63: 'Tong Keow’s mixed medicine-and-food business gives these activities a shared location. Its branding links the Hougang branch to a wider business, while the established neighbourhood provides the setting for the clientele described by staff. We see the shop as offering traditional materials in forms suited to local shopping and household routines.',
64: 'This reading connects with Unschuld’s (2018) account of selection and adaptation and Yang’s (2022) history of Chinese medicine in Singapore. Our fieldwork adds the everyday retail setting to that discussion: herbs remain visible, but they are encountered through soup displays, packaged products and a shop that also sells food.',
65: '7 Limitations',
66: 'The report draws on one visit and one staff interview. We did not collect sales figures, interview customers or compare branches. Product demand and customer preferences come from staff descriptions. Neighbourhood data cover populations beyond the shop’s customers, and industry examples are institutional, promotional or journalistic accounts used for comparison.',
67: 'We did not obtain complete soup recipes, ingredient sourcing records or branch purchasing records. HSA’s listing identifies the pictured Nature’s Green capsules as Singapore-manufactured, but the interview did not name the preparation or its ingredient origins. Physician presence at the outlet was not clearly confirmed, and no consultation, prescription or patient outcome was recorded. MOH’s description of professional registration provides the wider context for clinical practice (MOH, 2026).',
68: 'The appendix identifies traditional reference profiles and external images separately from our field photographs. Customer interviews, sales records, sourcing records and further visits would help explore repeat purchases and how people understand these products.',
70: 'At Tong Keow, TCM enters daily life through familiar ingredients, soup packs and prepared products in a shop that also sells food. The staff account links this range to nourishment, convenience and customers’ routines. The Hougang setting and the business’s mixed retail model help us understand why these uses sit together in one neighbourhood medicine hall.',
71: 'We conclude that the continuity of TCM in this case depends partly on adapting how people encounter and use it. The ingredients remain part of the tradition, while their packaging, preparation and settings of use change. Tong Keow offers a concrete view of this process through the ordinary activities of shopping and cooking.',
74: 'Appendix A retains the detailed survey findings from the group presentation. The tables identify staff-reported uses, traditional reference profiles and the sources of the photographs.',
76: 'The presentation groups ginseng and American ginseng in one entry. Table A1 separates their profiles, giving nine rows for the eight reported entries. The field cabinet also labels American ginseng separately.',
78: 'Note. Herb photographs and traditional profiles are adapted from the Hong Kong Polytechnic University database (PolyU). Meridian names refer to TCM functional systems, and the applications describe traditional uses in their stated contexts.',
81: 'The eight categories follow presentation slide 4. The supplied photograph identifies Nature’s Green Mind Soothe Capsules as the illustrated example for liver care and mood support. Details of mixtures and finished products are included where available in the field records.',
83: 'Note. Uses follow the interview or presentation. The Nature’s Green box is a supplied product photograph; the other reference illustrations are identified in their rows. Complete product formulas were not recorded during the visit.',
86: 'Table A3 separates local cultivation, manufacture and packaging. Nature’s Green is the brand of the pictured Mind Soothe Capsules. HSA lists the capsules as a Singapore-manufactured Chinese Proprietary Medicine (HSA, 2025b); their ingredient origins were not recorded.',
88: 'Note. NParks supplies the reference plant photographs. The cactus species and stock origins were not identified in the interview. The Five Flower Tea image is an external product example, and the monk-fruit image shows a reference ingredient. HSA supplies the manufacturing information for the Nature’s Green capsules.',
90: 'The five labels follow slide 6. Staff named Dang Shen, Huang Qi, Yu Zhu, Huai Shan, red dates and goji as common soup ingredients. Table A4 records the named ingredients and the presentation’s descriptions of nourishment and everyday care.',
95: 'The lower-demand examples follow presentation slide 8: one named herb and two broader product categories. Their descriptions come from staff and the presentation, without a numerical sales ranking.',
97: 'Note. Ban Zhi Lian properties come from PolyU. The specialist-herb photograph shows the field cabinet, and the ginseng image illustrates a tonic material. Specific combination and tonic formulas were not recorded.',
99: 'A6 Staff descriptions of product uses',
100: 'Staff described the six product associations below, retained from slide 9. Physician presence at the outlet was unclear, and we recorded no clinical prescriptions or patient cases. Table A6 therefore presents the interview’s retail descriptions.',
101: 'Table A6 Product uses described by staff',
103: 'A7 Survey coverage and sources',
104: 'Table A7 Survey coverage and details not recorded',
160: 'Note. Branded soup packs and a family cooking image at the shop frontage. Photograph by the group, Tong Keow Healthcare, 13 September 2026.',
165: 'Note. Preselected dried ingredients in Tong Keow soup packs. Photograph by the group, Tong Keow Healthcare, 13 September 2026.',
170: 'Note. Cabinet labels for American ginseng and sulphur-free Dang Shen. Photograph by the group, Tong Keow Healthcare, 13 September 2026.',
}
for i, value in changes.items(): rewrite(pp[i], value)
# These short paragraphs repeat the clinical distinction retained in Section 6.1.
for i in (60, 33, 10):
    pp[i]._p.getparent().remove(pp[i]._p)

# Simplify table commentary without touching picture-bearing paragraphs or herb profiles.
cell_changes = {
 (1,1,4): 'Staff described use for fatigue and general nourishment.',
 (1,5,4): 'Staff described use for general wellness and immunity support.',
 (1,6,4): 'Staff linked this category to late nights and stress.',
 (1,7,4): 'Staff described use for cold symptoms.',
 (2,3,3): 'Nature’s Green is the brand of this finished Chinese Proprietary Medicine.',
 (3,1,2): 'Light nourishment and everyday care in the presentation.',
 (3,2,2): 'Qi support and nourishment in the presentation.',
 (3,3,2): 'Moistening and nourishment in the presentation.',
 (3,5,2): 'Spleen and digestive support in traditional terms.',
 (5,0,2): 'Details recorded',
 (5,1,2): 'Product category named; formula not recorded.',
 (5,2,2): 'Product category named; formula not recorded.',
 (5,3,2): 'Staff used fatigue and Qi-support language.',
 (5,4,2): 'Staff described immunity support.',
 (5,5,2): 'Staff linked products to daily routines and stress.',
 (5,6,2): 'Staff described external use for aches and injuries.',
 (6,0,3): 'Details not recorded',
 (6,6,1): 'No physician prescriptions recorded',
 (6,7,3): 'No physician-treated cases recorded.',
}
for (ti, ri, ci), value in cell_changes.items():
    cell = d.tables[ti].cell(ri,ci)
    assert not cell._tc.xpath('.//w:drawing')
    rewrite(cell.paragraphs[0],value)

# Keep the final bibliography entries together rather than stranding two on a page.
for p in d.paragraphs:
    if p.text.startswith('Unschuld, P. U. (2018).'):
        p.paragraph_format.page_break_before = True
    if p.style.name == 'Normal' and not p._p.xpath('.//w:drawing'):
        p.paragraph_format.keep_together = False

try:
    d.save(f)
except PermissionError:
    f = root / 'GEC1044_Tong_Keow_Readability_Revision.docx'
    d.save(f)
check = Document(f)
text = '\n'.join(p.text for p in check.paragraphs)
assert len(check.inline_shapes) == original_images == 36
assert text.count('辨证论治') == 1
assert 'This is our interpretation' not in text
assert not re.search(r'\bprove[sd]?\b', text[:text.index('References')],re.I)
def picture_hashes(doc):
    return [hashlib.sha256(s._inline.xml.encode()).hexdigest() for s in doc.inline_shapes]
assert picture_hashes(check) == picture_hashes(Document(backup))
main = text[:text.index('Appendix A Detailed')]
checks = {'main_words_before': original_main_words,
          'main_words_after':len(main.split()), 'keyword_instances':1,
          'inline_images':36, 'all_picture_xml_preserved':True,
          'body_paragraphs_revised': len(changes), 'repeated_clinical_paragraphs_removed':3,
          'saved_file':str(f)}
(root/'_review/readability_revision_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
print(json.dumps(checks,indent=2))
