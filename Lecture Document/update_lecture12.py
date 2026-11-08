from pathlib import Path
import re

root = Path(__file__).parent
old = root / 'GEC1044_Lectures_6-11_Study_Notes.md'
text = old.read_text(encoding='utf-8')
(root / 'sources' / 'Notes_before_Lecture12_and_PDF.md').write_text(text, encoding='utf-8')

lecture12 = '''## Lecture 12 — Conclusion: history, translation and complementary medicine

[Recording](https://mediaweb.ap.panopto.com/Panopto/Pages/Viewer.aspx?id=e111022f-72b7-41b5-b2d3-b22000af5738)

**Source: all eight Panopto Contents entries, captured and visually checked.** Six contain substantive teaching; the other two are the title and ending. No caption track was available. The following explanations develop the visible slide arguments; they do not reconstruct unrecorded speech. External sources are identified separately.

### 1. Four questions that frame the course — 2:12

The conclusion asks how Chinese medicine should be understood through four connected issues:

| Issue on the slide | What to explain in an exam | Connections to previous lectures |
|---|---|---|
| Medicine and the state | Who authorizes practitioners, organizes training, funds care and decides which knowledge counts? | Singapore services in Lecture 6; Hong Kong professionalization in Lecture 11 |
| Combining Chinese medicine and biomedicine | Which aspects can cooperate clinically, and where do concepts, evidence and responsibilities differ? | Combined hospital records, cross-referrals, joint case management |
| China's modernity | How did changing institutions and ideas of science reshape Chinese medicine? | Modern training, research, regulation and hospital organization |
| The division between modern and premodern | Does a simple before/after distinction conceal continuities and changes within both traditions? | Historical practices alongside contemporary instruments and trials |

**Interpretive point:** Chinese medicine is a changing body of knowledge and practice shaped by institutions, translation, patients and politics. Studying it requires more than deciding whether it is ancient or modern. Likewise, integration can mean coordination of care without agreement on every theoretical concept.

### 2. Comparative history of science — 10:45

The slide challenges a historical habit of describing European knowledge as objective science while treating East Asian knowledge primarily as magic, mysticism or religion. It proposes comparing actual developments in fields such as astronomy, mathematics and the study of substances across regions.

Three distinctions make this argument precise:

1. **Historical understanding:** ask what a concept meant to its users and what problems it addressed.
2. **Historical comparison:** compare institutions, practices and standards of explanation in their own settings, including their exchanges.
3. **Clinical evaluation:** test whether a particular intervention produces meaningful benefits and acceptable harms today.

These are related but different questions. Criticizing Eurocentrism does not establish the effectiveness of a therapy. Conversely, failure of one modern clinical claim does not make a tradition historically unimportant.

**Additional historical research.** Joseph Needham's collaborative project made Chinese contributions visible within world histories of science. Nathan Sivin's introduction to the medicine volume also questions histories that treat every earlier discovery as a step toward a predetermined biomedical endpoint. This supports reading the course as a history of changing knowledge and care, not simply a list of ancient anticipations of modern discoveries. The correct bibliographic identification is *Science and Civilisation in China*, Volume 6, Part VI, *Medicine* (2000), by Needham with Lu Gwei-djen, edited and introduced by Sivin. [R20: Cambridge title pages](https://assets.cambridge.org/97805216/32621/sample/9780521632621ws.pdf); [R21: Sivin's introduction](https://assets.cambridge.org/97805216/32621/excerpt/9780521632621_excerpt.pdf)

### 3. Translation changes what we think we are comparing — 13:06

The slide identifies a mismatch between modern Chinese biomedical vocabulary and the terminology of historical Chinese medicine. A modern Chinese term for a microbe or hormone can refer to an internationally defined biomedical entity; that does not mean an older medical term had the same reference.

| Term or problem | Useful approach | Mistake to avoid |
|---|---|---|
| Qi, 气 | Preserve the term and explain its function in the particular passage | Treating it as automatically identical to energy measured in joules, oxygen or a hormone |
| Wanwu, 万物 | Explain the broad cosmological reference to the multiplicity of phenomena | Assuming its categories reproduce modern biological taxonomy |
| Zang-fu organ systems | Explain the traditional functions and relations | Substituting anatomical organs without qualification |
| Historical religion and philosophy | Examine how these shaped healing and cultivation | Removing them from the account merely because the modern course calls the subject medicine |

The slide raises a problem of translation, rather than proving that translation is impossible. A careful comparison states both the resemblance and the remaining difference. For example, a traditional description of digestive transformation may concern some experiences also studied by gastroenterology, while using a different explanatory structure.

The slide's comment about the absence of an authoritative comprehensive account should be read as the lecturer's assessment in context. It is not presented here as a verified claim that no authoritative reference exists in 2026.

### 4. CAM in multicultural Singapore — 28:24

CAM means complementary and alternative medicine. The slide presents high use in Singapore and distinguishes Chinese, Malay/Jamu and Indian/Ayurvedic traditions. This illustrates **medical pluralism**: people may draw on several systems within one society, and sometimes within the same episode of care.

**Additional research: identify the figures before memorizing them.** Lim, Sadarangani, Chan and Heng's 2005 survey used interviewer-administered questionnaires in one housing estate whose characteristics resembled Singapore's. It reported 76% using CAM over the preceding 12 months (95% CI 73.9–77.9%), with use reported by 84% of Chinese respondents and 69% of both Malay and Indian respondents. Its modality figures were TCM 88%, Jamu 8% and Ayurveda 3%. They describe the reported CAM-use mix, not percentages of all Singapore residents. The abstract alone does not resolve all modality denominator and multiple-use details. These are historical survey findings, not a current national census. The study also reported that 74% did not discuss CAM use with Western-trained doctors. [R22: Lim et al., 2005, primary survey](https://pubmed.ncbi.nlm.nih.gov/15907674/)

**Additional research: terminology.** NCCIH distinguishes complementary care, used alongside conventional care, from alternative care, used in its place. Integrative care adds deliberate coordination across approaches. Thus, taking two treatments at once does not by itself demonstrate well-integrated care. [R23: NCCIH definitions](https://www.nccih.nih.gov/health/complementary-alternative-or-integrative-health-whats-in-a-name)

### 5. Why communication can be difficult — 31:36

The slide asks why orthodox-medicine practitioners may be reluctant to communicate with CAM practitioners. It proposes limited CAM education, distrust, uncertainty about evidence or legal standing, philosophical differences, competition and concern about referral liability.

These are **possible barriers posed for discussion**, not measured prevalence estimates or a claim that every practitioner holds these views. In particular, the slide's mention of legal recognition does not mean that Singapore TCM practitioners lack legal recognition.

The earlier lectures supply practical ways to address these barriers: a common medication history, clear referral criteria, shared records, professional communication and explicit responsibility for monitoring and follow-up. This is a synthesis of Lectures 6, 11 and 12, rather than another recovered slide.

**Additional regulatory check, current to 4 November 2026.** MOH states that Singapore TCM practitioners must be registered and hold a valid practising certificate; registration and the licensing status of a clinic are separate questions. MOH's Integrative Sandbox supports evaluated collaboration with conventional care in public healthcare institutions. The existence of such a programme shows that integration is being developed under defined conditions; it does not validate every combination of treatments. [R24: MOH registration overview](https://hpp.moh.gov.sg/tcm-practitioners/about/); [R25: MOH TCM Integrative Sandbox](https://www.moh.gov.sg/others/grants-and-other-initiatives/tcm-integrative-sandbox/)

### 6. Why herbal products raise quality and safety questions — 34:12

The final substantive slide organizes distrust of Chinese herbal medicine around variability, uncertainty about constituents, and risks in production and supply.

| Stage or issue | What can vary or go wrong | Why this matters for evaluating evidence |
|---|---|---|
| Cultivation | Climate, soil and growing conditions | A plant name alone may not describe identical chemical material |
| Harvest and processing | Harvest timing, preparation and storage | Products described by the same traditional name may differ |
| Extraction and manufacture | Solvent, extraction process and formulation | Evidence for one preparation may not transfer to another |
| Identification | Wrong species or wrong plant part | The intended medicine and the supplied material may differ |
| Contamination | Unwanted metals, pesticide residues or microbes | Harm may arise from unwanted material rather than the intended constituent |
| Adulteration | Deliberate addition of undeclared substances | Apparent rapid benefit may have another explanation |
| Intrinsic constituents | Active and potentially toxic chemicals | A natural origin does not establish harmlessness |

**Terminology correction:** the slide lists cadmium, lead, mercury and arsenic together. Arsenic is a metalloid; pesticide residues are a separate contaminant category. Do not equate these categories or infer that every herbal product contains them.

**Additional professional research.** HSA requires dealers and listed Chinese Proprietary Medicines to meet relevant safety and quality requirements, including limits on toxic metals and microbial contamination and restrictions on undeclared synthetic drugs. Finished CPM products are a particular regulatory category; the rules should not be generalized indiscriminately to every raw herb or food. Listing and quality controls should not be read as clinical proof for every claimed indication. [R26: HSA safety and regulatory explanation](https://www.hsa.gov.sg/announcements/safety-precautions-when-buying-chinese-medicinal-pills-and-capsules/)

**Study synthesis:** distinguish the identity of the material, its quality, its potential toxicity, and its demonstrated clinical effectiveness. A product can pass one type of assessment without answering all the others.

### 7. Slide-by-slide evidence index

| Sidebar time | Content | Saved screenshot |
|---|---|---|
| 0:03 | Lecture 12 title | [Title](slides/L12-01-title.jpg) |
| 2:12 | Framing narratives | [Narrative](slides/L12-02-narrative.jpg) |
| 10:45 | Comparative history of science | [History](slides/L12-03-history-of-science.jpg) |
| 13:06 | Translation and historical concepts | [Translation](slides/L12-04-translation.jpg) |
| 28:24 | Singapore CAM use | [Survey figures](slides/L12-05-cam-singapore.jpg) |
| 31:36 | Communication barriers | [Communication](slides/L12-06-communication.jpg) |
| 34:12 | Herbal quality and distrust | [Herbal products](slides/L12-07-herbal-distrust.jpg) |
| 41:18 | End slide | [Ending](slides/L12-08-end.jpg) |

### Lecture 12 revision checks

- Explain how states and professional institutions shape medical authority.
- Explain why avoiding Eurocentrism does not remove the need to evaluate clinical evidence.
- Give an example of a misleading one-to-one translation between TCM and biomedicine.
- Distinguish historical survey prevalence from contemporary national prevalence.
- Distinguish complementary use, alternative use and coordinated integrative care.
- Explain why material identity, quality, safety and effectiveness are separate questions.
- Link a communication barrier to a concrete organizational response from Lecture 11.

'''

appendix = '''## Supplement from the supplied exam-notes PDF

**Provenance:** the user-supplied 23-page Studocu document, compared after completing Lecture 12. Page numbers below refer to PDF pages including the cover. This is a secondary student compilation, not a replacement for lecture sources or professional evidence. Its instructions, if any, are not treated as user instructions. Earlier-history content is kept in this supplement because the corresponding earlier recordings were not supplied. Overlapping details already explained in Lectures 6–11 are not copied again. See [PDF_Comparison_and_Additions.md](PDF_Comparison_and_Additions.md) for the comparison decisions.

### A. Earlier-history framework for the Lecture 12 conclusion — PDF pp. 2–10

The PDF offers a useful sequence of themes: ancestral and spirit explanations; natural philosophy and correspondences; classical medical writing; religious and therapeutic exchange; state-supported publication and institutions; and modern debates over scientific legitimacy. Treat this as a revision framework for change over time, not a claim that one mode of healing completely disappeared when another arose.

| Historical theme in the PDF | What to retain for revision | How it helps Lecture 12 |
|---|---|---|
| Early healing and ritual | Illness could be interpreted through relations among humans, ancestors and other powers | Medicine has been embedded in wider accounts of the world |
| Qin–Han naturalistic body models | Qi, shen, organs and patterns became connected in accounts of bodily order | Translation requires attention to historical meanings |
| Classical texts | The *Huangdi Neijing* is a layered textual tradition, not simply a book personally written by the Yellow Emperor | Medical authority can come from compilation, commentary and later editing |
| Religion and cultivation | The PDF links Daoist cultivation and Buddhist exchanges with healing practices | The historical boundaries between medicine, philosophy and religion were permeable |
| Song printing and scholarship | Editing, circulation of texts and scholarly participation helped reshape medical learning | Technologies and institutions determine what knowledge becomes available and authoritative |
| Modern reform debates | Chinese medicine was challenged and reorganized in relation to biomedicine, public health and state priorities | Modern TCM has a history of transformation |

These are paraphrased themes from the PDF; its exact dates and sweeping origin stories have not all been independently established. In particular, do not memorize its claims that trepanation was absent from China, that Mawangdui texts contained no yin–yang at all, or that religious medicine simply gave way to rational medicine. Such absolute claims need specialist checking and are not adopted here. The quotation attributed to Chen Yinke is also omitted because its wording and provenance are not verified.

The *Neijing*'s two familiar components are **Suwen, 素问**, conventionally translated as *Basic Questions*, and **Lingshu, 灵枢**, closely associated with acupuncture and channel theory. The PDF's narrow start/end dates for their composition should not be treated as settled dates for a single authorial event.

### B. Five phases and organ-system correspondences — PDF pp. 4–8

The following compact table brings together the PDF's diagrams. These are traditional explanatory associations, not experimentally established connections between tastes, directions and anatomical organs.

| Phase | Season | Direction | Climatic quality | Taste | Zang system | Paired fu system |
|---|---|---|---|---|---|---|
| Wood | Spring | East | Wind | Sour | Liver | Gallbladder |
| Fire | Summer | South | Heat | Bitter | Heart | Small Intestine |
| Earth | Late/long summer | Centre | Dampness | Sweet | Spleen | Stomach |
| Metal | Autumn | West | Dryness | Pungent | Lung | Large Intestine |
| Water | Winter | North | Cold | Salty | Kidney | Bladder |

**Generation, 生:** Wood → Fire → Earth → Metal → Water → Wood. **Restraint, 克:** Wood → Earth → Water → Fire → Metal → Wood. Normal restraint is part of the model of regulation, not automatically disease or destruction. Excessive restraint and reversal of restraint are distinct pathological ideas; the PDF's word “destruction” should not replace every instance of control.

**Yin–yang classification (PDF p. 7):** the interior, abdomen and five zang are classified as yin relative to the exterior, back and fu classified as yang. These classifications depend on the comparison being made; they are not claims that a body part possesses only yin or only yang in every context.

**The bureaucratic analogy (PDF pp. 6–7):** the Heart is likened to the ruler, the Lung to a senior official, the Liver to a general and the Gallbladder to decision-making. This is a model of coordinated bodily functions using political language. It is particularly useful for explaining Lecture 12's medicine–state theme: the language of political order can help organize descriptions of bodily order. It does not mean the anatomical heart issues conscious administrative commands.

**Sanjiao, 三焦:** the PDF emphasizes a named functional system rather than a single anatomical organ. The Pericardium and Sanjiao complete the six yin/six yang principal-channel pairing used in Lecture 8; they are commonly associated with Fire. Do not force every traditional functional category into a discrete structure on an anatomical chart.

### C. Singapore and medical pluralism — PDF pp. 10–12

The PDF adds themes of charity care, community associations, localization of formulas and exchange between Chinese and Malay traditions. These extend Lecture 12's account of a multicultural therapeutic landscape. Its comparative themes include herbs, food, bodily balance, hot/cold distinctions, manipulation and religious meanings.

Similarity does not establish a common theory or identical treatment. The PDF describes Malay traditional medicine using an earth/water/air/fire scheme; do not substitute that scheme for Chinese **wuxing**, or assume every Malay practice shares one standardized doctrine. Claims that local plants are always better than imported herbs are not supported by the comparison and are not adopted.

**Corrections to preserve:** the PDF's statement that integration is prohibited by law is too broad as a description of contemporary Singapore. Current MOH material explicitly describes evaluated integrative care. Likewise, a historical absence of practitioner regulation should not be read as today's position; current registration requirements are described in Lecture 12. [R25: MOH sandbox](https://www.moh.gov.sg/others/grants-and-other-initiatives/tcm-integrative-sandbox/); [R24: registration](https://hpp.moh.gov.sg/tcm-practitioners/about/)

The PDF gives a traditional account of tuberculosis in terms of climate, emotions and qi. **Biomedical correction:** TB is caused by *Mycobacterium tuberculosis* and spreads through airborne transmission from infectious pulmonary/throat disease. The historical framework belongs in an account of medical interpretation; it is not a substitute for infectious causation. [R27: CDC, TB causes and transmission](https://www.cdc.gov/tb/causes/index.html)

On PDF p. 11 the embedded HFMD and eczema boxes are positioned awkwardly relative to their bullet labels. Do not attach the fever/blister/mouth-ulcer box to eczema or the itchy/dry-skin box to HFMD. Their treatment and food-avoidance lists are not imported as clinical recommendations. In particular, broad eczema food exclusions should not be generalized; professional guidance advises against changing diet without medical advice. [R28: NHS atopic eczema guidance](https://www.nhs.uk/conditions/atopic-eczema/)

### D. Diagnostic and acupuncture diagram checks — PDF pp. 13–19

Most of this material is already covered in Lectures 7–8, including the four methods, eight principles, needle manipulation, point groups and fourteen-channel teaching scheme. The comparison adds these clarifications:

- **Pulse dimensions:** superficial/deep describes depth; rapid describes rate; intermittent describes rhythm; excess/weak describes force. They should not all be listed under “depth,” as on PDF p. 15. No single pulse description diagnoses an anatomical heart disorder by itself.
- **Tongue and facial maps:** the PDF's diagrams show traditional correspondences. They do not independently validate diagnosis or make a photograph sufficient for clinical assessment. Read them with Lecture 7's discussion of synthesis and research on observer agreement.
- **Channel count:** fourteen is the main channel-and-point teaching scheme of twelve principal channels plus Ren and Du, not a claim that the wider tradition recognizes no other vessels.
- **Cupping categories:** wet and dry describe methods, not exclusive ethnic ownership. PDF p. 19 itself lists both, so the earlier “Malay wet versus Chinese dry” distinction is too absolute.
- **Cupping marks:** a colour chart is not a validated measurement of toxins, organ illness or internal clots. The PDF's claim about clearing blood clots is not accepted as a biomedical effect. Lecture 8 already separates traditional explanations from clinical evidence.

### E. Food therapy and preservation of health — PDF pp. 20–23

**Seasonal principle (p. 22):** the PDF explicitly pairs spring/summer with nourishing yang and autumn/winter with nourishing yin. Within this traditional model, daily cultivation follows cycles of growth, outward activity, gathering and conservation. This extends Lecture 9's seasonal theme, but does not show that a season alone determines the correct diet for every person. In equatorial Singapore, do not mechanically transfer a temperate four-season calendar into a clinical prescription.

**Body and mind (pp. 22–23):** the preservation-of-health section combines bodily activity with mental tranquillity. Daoyin is described as both guided movement and attention training. This helps explain Lecture 10's integration of physical and mental cultivation; tranquillity should not be interpreted as avoiding all normal emotion.

**Two emotion lists should remain separate:** the PDF's earlier discussion uses the familiar medical grouping of joy, anger, worry/pensiveness, grief, fear and fright, whereas its preservation-of-health section uses joy, anger, sorrow, fear, love, hate and desire. Lecture 10 visibly uses the latter list. Lists of seven emotions vary by context; do not silently make them identical.

**Three grades versus four formula roles:** PDF p. 23 distinguishes superior, middle and inferior herbal grades, summarized there as prevention, intervention and treatment. Retain this as a historical classification described by the student source, with those simplified labels attributed to it. It is not a contemporary safety rating, evidence hierarchy or rule for self-prescribing. This is different from **jun–chen–zuo–shi**, the four functional roles within a formula discussed in Lecture 9 and on PDF p. 22. A grade classifies a medicinal substance in a historical scheme; a formula role describes its relationship to the other ingredients in a particular prescription.

The PDF's food-property, colour and taste charts largely duplicate Lecture 9. Its “yang” and “yin” constitution labels are simplified hot/cold examples, not interchangeable definitions of yang deficiency and yin deficiency. Retain the fuller distinctions already in Lecture 7.

### F. Hong Kong date clarification — PDF pp. 12–13

The PDF's 1872 date and the common 1870 date refer to different milestones: Tung Wah's own chronology lists its founding in **1870** and hospital opening in **1872**. Preserve both with their meanings. The PDF's remaining training, referral, research and records material mostly overlaps Lecture 11. Its “first integration” claim about SARS is too broad to use as a universal historical first. [R29: Tung Wah institutional chronology](https://www.tungwah.org.hk/en/about/milestones/)

'''

text = text.replace('# GEC1044 — Lectures 6–11 study notes', '# GEC1044 — Lectures 6–12 study notes', 1)
text = text.replace('**Research-enriched edition, checked 4 November 2026.**', '**Research-enriched edition with Lecture 12 and PDF comparison, checked 4 November 2026.**', 1)
text = text.replace('All six lectures now have explanatory study notes.', 'Lecture 12 adds eight visually checked sidebar captures, bringing the archive to 64 images. All seven lectures now have explanatory study notes. The supplied 23-page exam-notes PDF was subsequently compared, and selected additions and corrections are identified in the supplement below.', 1)
text = text.replace('| 11 | TCM outside China: History and Development in Hong Kong | Detailed caption-based notes; uncertain caption details flagged |', '| 11 | TCM outside China: History and Development in Hong Kong | Detailed caption-based notes; uncertain caption details flagged |\n| 12 | Conclusion: history, translation and CAM | Notes from all eight sidebar entries; spoken-only detail remains limited |', 1)
text = text.replace('## Connections across the available detailed lectures', lecture12 + appendix + '## Connections across the available detailed lectures', 1)
text = text.replace('## Coverage limits and evidence archive', '''11. **What does Lecture 12 add to the clinical lectures?** A framework for examining state authority, modernity, translation, pluralism and trust.
12. **Does the 76% CAM figure measure current national prevalence?** No. It is a 12-month estimate reported in a 2005 housing-estate survey.
13. **Is standardization equivalent to proven effectiveness?** No. Identity, consistency, safety and clinical outcomes require different evidence.
14. **What is the difference between a historical herb grade and a formula role?** One categorizes a substance in a historical scheme; the other describes its function within a prescription.

## Coverage limits and evidence archive''',1)
text = text.replace('All sidebar-listed entries for Lectures 6, 9 and 10 were captured and analyzed', 'All sidebar-listed entries for Lectures 6, 9, 10 and 12 were captured and analyzed',1)
text = text.replace('## Research references', 'Lecture 12 has no accessible captions; the eight sidebar frames cover listed slides rather than all spoken material. The PDF supplies supplementary student notes, not missing audio. Its contents have been paraphrased and assessed, with page references and exclusions documented in the comparison file.\n\n## Research references',1)

refs = [
('R20','Needham, with Lu Gwei-djen; edited by Nathan Sivin (2000), Science and Civilisation in China, Vol. 6, Part VI: Medicine, title pages','https://assets.cambridge.org/97805216/32621/sample/9780521632621ws.pdf','Publisher bibliographic source'),
('R21','Nathan Sivin (2000), editor’s introduction to the medicine volume','https://assets.cambridge.org/97805216/32621/excerpt/9780521632621_excerpt.pdf','Specialist historical scholarship, publisher excerpt'),
('R22','Lim MK, Sadarangani P, Chan HL, Heng JY (2005), Complementary and alternative medicine use in multiracial Singapore. Complement Ther Med 13:16–24. DOI 10.1016/j.ctim.2004.11.002','https://pubmed.ncbi.nlm.nih.gov/15907674/','Primary cross-sectional survey; abstract checked'),
('R23','NCCIH, Complementary, Alternative, or Integrative Health: What’s In a Name?','https://www.nccih.nih.gov/health/complementary-alternative-or-integrative-health-whats-in-a-name','Official terminology guidance'),
('R24','MOH Health Professionals Portal, TCM registration and regulation overview','https://hpp.moh.gov.sg/tcm-practitioners/about/','Official professional-regulation overview'),
('R25','MOH, Traditional Chinese Medicine Integrative Sandbox, updated 3 November 2026','https://www.moh.gov.sg/others/grants-and-other-initiatives/tcm-integrative-sandbox/','Official current programme description'),
('R26','HSA, Safety precautions when buying Chinese medicinal pills and capsules','https://www.hsa.gov.sg/announcements/safety-precautions-when-buying-chinese-medicinal-pills-and-capsules/','Official product-quality and safety explanation'),
('R27','CDC, Tuberculosis: Causes and How It Spreads','https://www.cdc.gov/tb/causes/index.html','Official infectious-disease guidance'),
('R28','NHS, Atopic eczema','https://www.nhs.uk/conditions/atopic-eczema/','Official clinical/public guidance'),
('R29','Tung Wah Group of Hospitals, Historical Milestones','https://www.tungwah.org.hk/en/about/milestones/','Institutional primary historical chronology'),
]
for code,title,url,kind in refs:
    text += f'\n- **{code}.** [{title}]({url}). **Type:** {kind}.\n'
old.write_text(text,encoding='utf-8')
(root/'GEC1044_Lectures_6-12_Study_Notes.md').write_text(text,encoding='utf-8')
with (root/'Research_Sources.md').open('a',encoding='utf-8') as f:
    f.write('\n# Lecture 12 and PDF comparison: additional sources\n\nChecked 4 November 2026.\n')
    for code,title,url,kind in refs:
        f.write(f'\n## {code}\n\n[{title}]({url})\n\nEvidence type: {kind}.\n')

slides = [
('0:03','L12-01-title','Title: Lecture 12, Conclusion.'),
('2:12','L12-02-narrative','Four framing issues: state and medicine; combining Chinese medicine and biomedicine; Chinese modernity; division between modern and premodern.'),
('10:45','L12-03-history-of-science','Compare histories of science across regions; question stereotypes of East Asia as exclusively mystical or religious; consider Needham and alternatives to Eurocentric history.'),
('13:06','L12-04-translation','Translation problems: modern Chinese biomedical vocabulary is not equivalent to historical concepts; qi and wanwu require contextual interpretation; medicine intersects with religion and philosophy.'),
('28:24','L12-05-cam-singapore','CAM survey figures displayed: 76% overall; Chinese 84%, Malay 69%, Indian 69%; modality figures TCM 88%, Jamu 8%, Ayurveda 3%. Slide does not show year, sample or precise denominators. Research context is in the main notes.'),
('31:36','L12-06-communication','Possible communication barriers: education, distrust, evidence, legal recognition, philosophy, competition and liability. Framed as questions rather than measured frequencies.'),
('34:12','L12-07-herbal-distrust','Herbal variability from climate, soil, harvest, processing, extraction and manufacture; uncertainty about constituents; standards, intrinsic toxicity, contamination, misidentification and adulteration. Metals/metalloid examples and pesticide residues require separate categories.'),
('41:18','L12-08-end','The End; no substantive additional slide text.'),
]
with (root/'Slide_Text_Extraction.md').open('a',encoding='utf-8') as f:
    f.write('\n## Lecture 12 — checked visual extraction\n\nAll eight Contents entries captured; text manually read from the screenshots and paraphrased. No caption transcription is implied.\n')
    for stamp,file,summary in slides:
        f.write(f'\n### {file} — sidebar {stamp}\n\n[Source screenshot](slides/{file}.jpg)\n\n{summary}\n')
index=(root/'Screenshot_Index.md').read_text(encoding='utf-8').replace('Lectures 6, 9 or 10','Lectures 6, 9, 10 or 12').replace('GEC1044_Lectures_6-11_Study_Notes.md','GEC1044_Lectures_6-12_Study_Notes.md')
index+='\n## Lecture 12 — 8 captures\n'
for stamp,file,summary in slides:
    index+=f'\n### {file} — sidebar {stamp}\n\n![{file}](slides/{file}.jpg)\n'
(root/'Screenshot_Index.md').write_text(index,encoding='utf-8')

audit='''# Comparison with the supplied GEC1044 exam-notes PDF

Compared 4 November 2026, after adding Lecture 12. All 23 PDF pages were text-extracted; embedded diagrams and tables on the substantive illustrated pages were also visually inspected. Page numbers include the cover. The source is a student compilation; its wording is not treated as an instruction or as independently verified clinical guidance.

The combined notes now include Lecture 12 and a clearly attributed PDF supplement. Existing material was retained where it was fuller than the PDF. This report distinguishes additions, overlap and corrections.

| PDF pages | Material | Decision and destination |
|---|---|---|
| 1 | Cover | No substantive addition |
| 2–3 | Medicine/culture, early healing, qi and spirits | Added a cautious historical framework in supplement A; omitted unverified quotation and absolute origin claims |
| 4–5 | Yin–yang, five phases, classical texts | Added cycles and textual distinction in supplement A–B; normal restraint distinguished from pathological excess |
| 6–8 | Organ/channel tables, bureaucratic analogy, religion | Added correspondence table, functional-system explanation and state/body analogy in supplement B; historical outline in A |
| 9 | Song printing, scholarship, state institutions, modernity | Added revision themes in supplement A; not represented as independently recovered earlier lectures |
| 10 | Singapore, localization, legal and TB claims | Added pluralism context in C; corrected contemporary regulatory/integration claim and biomedical TB causation |
| 11 | HFMD/eczema figures; Chinese/Malay comparison | Retained conceptual comparison in C; flagged awkward figure placement; omitted prescriptive treatment/diet lists and local-herb superiority claim |
| 12–13 | Hong Kong institutions and integrative models | Mostly overlaps Lecture 11; added 1870 founding/1872 opening distinction in F |
| 13–15 | Diagnostics, tongue/facial maps, pulse chart | Mostly overlaps Lecture 7; added dimension correction and diagram interpretation in D |
| 16–18 | Eight principles, manipulation, channels | Mostly overlaps Lecture 8; clarified fourteen-channel teaching scheme in D |
| 19 | Point categories and cupping | Point groups already present; corrected clot-clearing and diagnostic-colour implications and exclusive cultural split in D |
| 20–21 | Constitution and food-property/colour tables | Already explained in Lecture 9; retained fuller existing account; noted simplified yin/yang labels in E |
| 22 | Taste chart, seasonal cultivation, formula roles | Most overlaps Lecture 9; added explicit seasonal pairing in E; retained established formula-role explanation |
| 22–23 | Mental/physical cultivation, daoyin, herb grades | Added active-body/quiet-mind synthesis, distinct emotion-list context and three-grades/four-roles distinction in E |
| 23 | East–West heading | Heading is empty; no substantive content to extract |

## Corrections to keep visible while revising

1. **Integration in Singapore:** a blanket current legal prohibition is not a sound summary. MOH's Integrative Sandbox explicitly evaluates coordinated care. See R24–R25 in the notes.
2. **Registration:** historical absence of licensing is distinct from today's mandatory practitioner registration and practising certificate. See R24.
3. **TB:** a traditional explanatory vocabulary is not infectious causation. CDC identifies M. tuberculosis and airborne spread. See R27.
4. **Tung Wah:** founding in 1870 and opening in 1872 are different milestones, both in the institution's chronology. See R29.
5. **Pulse:** rate, rhythm, force and depth are separate dimensions. Rapid and intermittent are not depths.
6. **Wet/dry cupping:** methods are not exclusive to one ethnic tradition. The PDF itself later lists both.
7. **Cupping marks and clots:** the colour chart does not establish toxin measurement or clot treatment. Read with the existing Lecture 8 evidence discussion.
8. **HFMD/eczema:** embedded boxes on p. 11 are poorly aligned with labels. Do not turn extraction order into a diagnosis or import blanket dietary restrictions. See R28.
9. **Herbal grades:** historical superior/middle/inferior categories are not modern safety or efficacy rankings, and differ from roles within a formula.
10. **Historical absolutes:** trepanation, Mawangdui, exact Neijing composition dates and claims of a universal first integration require more specialist verification. They were not silently accepted.

## Lecture 12 evidence added separately

Eight screenshots cover all Contents entries. Added explanations address historical narratives, comparative science, translation, CAM use, professional communication and herbal-product quality. External additions identify the 2005 survey behind the slide figures, clarify terminology and current regulation, and distinguish product controls from effectiveness. The lecture remains slide-based; missing narration has not been replaced with invented speech.

[Open the updated combined notes](GEC1044_Lectures_6-12_Study_Notes.md)
'''
(root/'PDF_Comparison_and_Additions.md').write_text(audit,encoding='utf-8')
print('Updated notes:',len(text.split()),'words; lecture sections:',len(re.findall(r'^## Lecture \d+',text,re.M)))
print('Screenshots:',len(list((root/'slides').glob('*.jpg'))))
