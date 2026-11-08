from pathlib import Path
import re, json, hashlib

root = Path(__file__).parent
source_dir = Path("C:/Users/lukel/OneDrive/Documents/Luke Obsidian/Luke's Vault/01 Modules/GEC1044/Course Notes/Lectures/Clean Notes")
names = [
'1.1 What is Medicine.md','1.2 Begining.md',
'2.1 Natural Philosophy and Chinese Medicine.md','2.2 Organs & Meridians in Classic Chinese Medical Texts.md',
'3.1 Chinese Medicine from Medieval to Late Imperial Period — Han to Tang.md',
'3.2 Chinese Medicine from Medieval to Late Imperial Period — Song Jin Yuan.md',
'4. Becoming Traditional Chinese Medicine.md','5. A Brief Introduction to Chinese Medicine in Singapore.md',
*[f'Reading for Week {i}.md' for i in range(1,6)]]
manifest=[]
for i,name in enumerate(names,1):
    p=source_dir/name
    content=p.read_text(encoding='utf-8-sig')
    manifest.append({'id':f'S{i}','file':name,'path':p.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'words':len(content.split()),'headings':len(re.findall(r'^\s*#+ ',content,re.M))})
(root/'sources'/'Course_notes_source_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

early = '''## Lecture 1 — What is medicine? Beginnings of Chinese medicine

**Course sources:** supplied notes S1–S2 and Week 1 reading summary S9; [source index](Course_Source_Index.md#lecture-1-and-week-1). These are summaries of your Markdown files, not a newly checked video transcript. Reading arguments are attributed through those summaries; the original assigned chapters were not supplied.

### 1. The central problem: one biological species, many medical systems

The opening question is why biologically similar people develop different systems for interpreting illness. The course treats medicine as a combination of **observations, explanatory models, practices and institutions**. Patients trust interpretations of bodily experience as well as treatments. Cultural and political history helps explain why one medical account becomes authoritative.

The notes distinguish **healing**, the broad effort to relieve suffering, from **medicine**, a systematic attempt to explain normal and abnormal bodily states, predict their development and intervene. This is the lecture's analytical distinction, not a universal rule excluding all ritual or practical healing from medical history.

The model **living person = body + X** captures historical attempts to explain what makes physical matter alive. X can refer to soul, spirit, psyche or other concepts. The model describes historical reasoning; it does not establish an independently measured life substance or make these terms equivalent.

### 2. Observation requires interpretation

A physician connects signs to a model of bodily processes. The supplied notes use a *Shiji* physician story to illustrate recognizing disease before obvious symptoms appear. The point is expert interpretation and prognosis, rather than proof that the story records a verified diagnostic achievement.

**Observation → theoretical interpretation → diagnosis → prognosis → intervention.** A symptom such as fever and a disease process are different levels of description. Both historical traditions and modern medicine use concepts that go beyond what can be directly seen.

In the supplied account of **Foucault's medical gaze**, hospitals, clinical teaching and pathological anatomy reorganized observation and professional authority. A clinician selects medically relevant features from a person's experience. This explains the relationship between knowledge and institutions; it does not imply that clinical findings are arbitrary or that all clinicians disregard patients' lives.

### 3. Early healing: environment, ancestors and ritual

| Theme | Explanation in the supplied lecture notes | Historical lesson |
|---|---|---|
| Survival and hygiene | Drainage, shelter, ventilation and avoiding harmful environments | Health protection preceded formal medical theory |
| Shang healing | Oracle-bone divination investigated illness and possible ancestral displeasure; the king had ritual authority | Social and ancestral relations informed causation |
| Zhou developments | Heaven, ancestors and other spirits coexisted in explanations of misfortune | New frameworks supplemented older ones |
| Warring States healing | Demons, exorcism and aggressive therapies were described using attack/defence language | Warfare supplied metaphors for bodily disorder |
| Naturalistic accounts | Qi, blood, shen, organs, emotions and environmental influences became linked | Supernatural concepts could be reinterpreted within bodily processes |

Banpo's ditch and Hemudu's raised housing are examples used in the notes to discuss environmental adaptation. Do not infer a complete ancient disease theory or a single purpose for an archaeological structure from these examples alone.

**Research correction:** S2 and the Studocu PDF imply that prehistoric trepanation was absent from China. Lv and colleagues describe a Neolithic Fujia skull interpreted as evidence of trepanation with survival. The blanket absence claim is therefore not retained. The finding does not by itself establish the operator's purpose, so “expelling spirits” should not be assumed for every case. [R30: Lv et al., *World Neurosurgery*, 2013](https://pubmed.ncbi.nlm.nih.gov/23022649/)

### 4. From external spirits to internal resources

**Zang** are described through longer-term storage of vital resources; **fu** receive, transform and transmit. **Shen** becomes associated with consciousness and mental activity, especially through the Heart system. **Qi and blood** support bodily processes in this framework.

An internal deficiency can be compared with a breach in a city's defences. External influences become pathogenic in relation to bodily vulnerability. **Zheng qi** refers to the body's proper or healthy capacities; **xie qi** to pathogenic or disordering influences. The vocabulary retains political, military and moral associations even when used in naturalistic explanations.

The notes identify emotional excess as a possible internal cause within traditional theory. The conventional medical list includes joy, anger, worry, pensiveness, grief, fear and fright. This differs from the list in Lecture 10's cultivation context. These are historical medical frameworks, not evidence that people are morally responsible for becoming ill.

### 5. Week 1 reading — patterns, yin–yang and society

**Kaptchuk, as summarized in S9:** a patient's signs gain meaning through their configuration. The same biomedical disease can correspond to different TCM patterns, while one pattern can occur in people with different diseases. The stomach-disorder example illustrates the reasoning process rather than supplying a self-diagnosis checklist. The landscape-painting analogy emphasizes relationships among parts; the “web” image describes interacting processes without requiring one controlling thread.

The summary identifies five yin–yang relationships: **co-presence, mutual dependence, mutual restraint, transformation, and inclusion of the opposite within each aspect**. Yin and yang are relative categories, not two isolated substances or a requirement that every healthy variable stay at a fixed 50/50 value.

**Sivin, as summarized in S9:** scientific ideas, employment, patronage, political institutions and intellectual practices develop together. The **cosmos–state–body** relationship cannot be reduced to an apolitical theory later borrowed by government. The China/Greece comparison concerns different settings for argument and intellectual authority; it is not a ranking of civilizations or a claim that every thinker behaved identically.

**Read Week 1 beside Week 4:** Kaptchuk's disease/pattern contrast is a useful teaching model. Unschuld's later critique warns against turning it into an absolute opposition between causal Western medicine and non-causal Chinese medicine. Both traditions have internal diversity.

### Studocu cross-check — PDF pp. 2–3

Added or retained: culture and trust; theory beyond observation; the living-person problem; symptoms versus disease; environmental adaptation; ancestral and demonic healing; qi/shen, storage systems and emotions. The quotation attributed to Chen Yinke is not reproduced without a traceable source. A single exact date for the “birth of medicine” is not treated as settled fact. The linear sequence is a revision aid: ritual, practical and naturalistic healing continued to coexist.

### Lecture 1 revision checks

- Explain why observation alone does not determine a medical theory.
- Explain how trust and institutions contribute to authority.
- Compare ancestral punishment, demonic invasion and naturalistic disorder as explanatory models.
- Explain how body–state metaphors connect Lecture 1 to Lectures 2 and 12.

## Lecture 2 — Natural philosophy, organs and meridians

**Course sources:** S3–S4 and Week 2 reading summary S10; [source index](Course_Source_Index.md#lecture-2-and-week-2).

### 1. Natural order and systematic correspondence

The notes place the growth of natural philosophy amid political upheaval and debate in the late Zhou/Warring States world. Yin–yang, qi and the Five Phases offered ways to explain recurring processes shared by nature, society and the body. These developments coexisted with ancestral and spirit explanations.

**Systematic correspondence** organizes different domains through common relationships: seasons, directions, tastes, bodily systems and climatic qualities. **Microcosm** means a smaller system understood through patterns also attributed to a larger one. A body could therefore be interpreted simultaneously through cosmic cycles and political organization.

### 2. Yin–yang, the Yijing and the Five Phases

Yin and yang originally evoke shade and sunlight and develop into relative aspects such as inward/outward, cold/hot and still/active. Their meaning depends on the relationship being described.

The supplied notes present a cosmological teaching sequence from undifferentiated unity through two forms, four images and eight trigrams. **Broken lines represent yin; unbroken lines represent yang.** Three binary lines give eight trigrams, and two trigrams combine into one of 64 hexagrams. This summarizes a received interpretive scheme; it should not be read as proof that every stage, including the Wuji/Taiji formulation, appeared together in the earliest *Yijing*.

“Phases” or “agents” emphasizes processes rather than five fixed chemical ingredients:

| Phase | Seasonal image | Direction | Climatic association | Taste | Zang / paired fu | Tissue association in the supplied table |
|---|---|---|---|---|---|---|
| Wood | Spring growth | East | Wind | Sour | Liver / Gallbladder | Sinews |
| Fire | Summer expansion | South | Heat | Bitter | Heart / Small Intestine | Blood |
| Earth | Late-summer ripening | Centre | Dampness | Sweet | Spleen / Stomach | Flesh |
| Metal | Autumn gathering | West | Dryness | Pungent | Lung / Large Intestine | Skin and hair |
| Water | Winter storage | North | Cold | Salty | Kidney / Bladder | Bone marrow |

**Generating cycle:** Wood → Fire → Earth → Metal → Water → Wood. **Restraining cycle:** Wood → Earth → Water → Fire → Metal → Wood. Normal restraint maintains order within the theory; excessive restraint or reversal is a different concept. “Destruction” is not a suitable replacement for all restraint.

### 3. Zang-fu and the bureaucratic body

The *Huangdi Neijing* is a composite textual tradition conventionally discussed through **Suwen, Basic Questions**, and **Lingshu, Spiritual Pivot**, with the latter strongly associated with acupuncture. These are not simply writings personally composed by a historical Yellow Emperor.

The five zang and interior/abdomen are classified as yin relative to the fu and exterior/back classified as yang. Zang-fu name functional systems whose meanings extend beyond anatomical organs.

| Bureaucratic comparison | Systems and functions in the course account |
|---|---|
| Ruler | Heart-mind: shen, consciousness and coordination |
| Senior adviser and general | Lung: order/moderation; Liver: planning |
| Decision-making and envoy | Gallbladder: judgement; Danzhong/Pericardium: joy |
| Grain provision | Spleen and Stomach: food and flavours |
| Receiving and transmitting | Small and Large Intestines: processing and transformation |
| Skilled work and waterways | Kidneys: capacity/expertise; Sanjiao: fluid pathways; Bladder: storage |

**Xin, 心**, spans heart and mind. **Sanjiao, 三焦**, is discussed as a functional organization of upper, middle and lower regions rather than a single identifiable anatomical organ. The supplied table groups respiration/distribution above, digestion/transformation centrally and fluid/waste processes below; these are broad functional regions, not a modern anatomical atlas.

### 4. Six yin and six yang principal channels

The channel name combines **hand/foot + yin/yang division + associated system**:

| Yin channel | Paired yang channel |
|---|---|
| Hand Taiyin Lung | Hand Yangming Large Intestine |
| Foot Taiyin Spleen | Foot Yangming Stomach |
| Hand Shaoyin Heart | Hand Taiyang Small Intestine |
| Foot Shaoyin Kidney | Foot Taiyang Bladder |
| Hand Jueyin Pericardium | Hand Shaoyang Sanjiao |
| Foot Jueyin Liver | Foot Shaoyang Gallbladder |

The Pericardium adds a sixth yin-system channel to the five-zang scheme. The notes distinguish sovereign and ministerial Fire in explaining the expanded correspondences. Avoid treating “weak/strong Fire” as a simple measurement of intensity, or all uses of “six phases,” “six qi” and “six channels” as interchangeable.

Channels link bodily regions in the traditional model, so a selected acupuncture point need not lie directly over the anatomical organ named by its channel. This explains the model of treatment in Lecture 8; it does not independently establish a physical conduit or clinical efficacy.

### 5. Week 2 reading — Daoism, medicine and canonicity

**Stanley-Baker, as summarized in S10:** Daoist traditions and medicine shared techniques and concepts, while also contesting one another. The phrase “medicine and Daoism share a source” should not erase these changing boundaries. **Ming, 命**, connects life, allotted lifespan, destiny and command; political collapse, epidemics and bodily disorder could therefore be understood together.

Healing, prevention, longevity and transcendence could share practices while pursuing different goals. Examples include **daoyin** (guided movement), **fangzhongshu** (bedchamber cultivation), **fushi** (ingesting substances), **bigu** (grain avoidance) and **fuzhou** (talismans/incantations). These circulated beyond exclusively Daoist communities and are described historically, not recommended here. The Celestial Masters and Great Peace movements combined communal organization, moral accounts of illness and healing. An **illness theodicy** explains why suffering may strike people who seem innocent; it differs from identifying an infectious organism.

**Boyanton, as summarized in S10:** the question is how the *Neijing* became canonical. Short textual units, apprenticeship and divergent collections preceded later compilations. Editors such as Huangfu Mi and Wang Bing reordered inherited material; Song state editing and printing then increased particular editions' authority and circulation. Canon formation preserves selected texts and can marginalize alternatives. Its process is **transmission → compilation → editing → publication → citation and authority**, not simply age → automatic supremacy.

Exact composition dates remain contested and layered. A bibliographic reference, surviving passage, later compilation and printed edition are different events; the PDF's broad chronology and the reading's dating argument should not be fused into one exact authorship date.

### Studocu cross-check — PDF pp. 3–8

Added the diagram-based tissue, body-region and bureaucracy correspondences to the lecture summary. Included generation/restraint cycles, the distinction between Suwen/Lingshu, and functional Sanjiao. The PDF's claim that Five Phases simply originated from the Five Virtues doctrine is not used as a proven single origin. Table correspondences are labelled traditional associations throughout.

### Lecture 2 revision checks

- Define systematic correspondence and explain one row of the phase table.
- Explain why normal restraint is not automatically pathology.
- Decode “Hand Taiyin Lung” and distinguish a channel name from anatomy.
- Explain why canonicity and the boundaries of Daoism/medicine are historical questions.

## Lecture 3 — From Han to Tang, Song and Jin–Yuan; reading extension to Ming–Qing

**Course sources:** S5–S6 and Week 3 reading summary S11, with S10 for related textual history; [source index](Course_Source_Index.md#lecture-3-and-week-3). Ming–Qing and Warm Disease details below come from the reading summary, extending the lecture-note headings.

### 1. Early manuscripts reveal plurality

Mawangdui manuscripts show recipes, ritual techniques, prognostic interests and bodily cultivation alongside early vessel concepts. Their importance is that the fully integrated system familiar from later teaching cannot be assumed for every earlier source.

**Research correction:** do not write that Mawangdui contains no yin–yang or vessel theory. The excavated corpus includes texts conventionally titled *Cauterization Canon of the Eleven Yin and Yang Vessels*. A specialist historical study lists these alongside daoyin, cultivation and recipe texts. The defensible contrast is between diverse early configurations and later systematization, not total absence of relevant ideas. [R31: Li Yunxin, 2022, historical study and manuscript list](https://jas.hkbu.edu.hk/content/dam/jas-assets/publications/bulletin-of-the-jao-tsung-i-academy-of-sinology/issue-9/i9--04.pdf)

### 2. Formula medicine and classical theory

The supplied notes contrast partly distinct early traditions: canonical acupuncture theory associated with the *Neijing*, and collections of **fang, 方**, or prescriptions, including *Prescriptions for Fifty-Two Ailments*. This is a comparison of textual emphases and status, not an absolute rule that all elites rejected drugs.

The tradition attributed to **Zhang Ji/Zhang Zhongjing** links clinical presentations, illness progression and the patient's condition to named formulae. The later transmitted **Shanghan Lun** became particularly influential through Song and subsequent editing and interpretation. A useful distinction is **formula collection** versus **reasoned matching of presentation and formula**; neither ancient title should be treated as a modern clinical trial.

### 3. Religious exchange and Han–Tang synthesis

| Figure or development | Main contribution in the supplied account |
|---|---|
| Religious Daoism | Longevity/transcendence encouraged cultivation and investigation of substances |
| Ge Hong | *Zhouhou Beiji Fang*: accessible emergency and practical formula knowledge |
| Tao Hongjing | Editing and organization of materia medica |
| Buddhist exchange | Four-element/humoral models, healing deities, meditation and breathing practices |
| Sui–Tang institutions | Expanded state medical administration and training |
| Sun Simiao | Formula medicine and cultivation, incorporating several intellectual and religious influences |
| Wang Bing | Reorganized and commented on the Suwen; the notes date his edition to 762 |

Buddhist earth/water/fire/wind and Indian wind/bile/phlegm models are distinct from Chinese Five Phases. Practices were translated and adapted rather than transferred unchanged. Late Tang political persecution affected Buddhist institutions; this should not be converted into a claim that all Buddhist medical influence disappeared.

### 4. The Song transformation: books, scholars and government

The Song's significance lies in expanded institutions and circulation of knowledge. **Woodblock printing** made editions more reproducible and widely available. The **Bureau for Editing Medical Texts**, associated in the notes with 1057–1069, compared versions and published selected works, including the *Suwen*, *Shanghan Lun*, formula collections and materia medica. Selection and state publication helped create a shared canon.

The **ruyi, 儒医**, or scholar-physician ideal connected medical authority with classical learning, ethical responsibility and cultivated judgement. The growth of examination-based elites matters here, but access remained socially unequal; “democratization” means wider circulation, not universal literacy or equal participation.

Official formularies, dispensaries, subsidized medicines, training and epidemic responses expanded government involvement. These improved access and standardization while creating a tension: a formula attached mechanically to a disease label could overlook the patient's actual presentation. State medical institutions predated the Song; the argument concerns expansion and reorganization, not the first government interest in health.

### 5. Pattern differentiation and the four Jin–Yuan masters

Distinguish **symptom**, an individual manifestation; **bing, 病**, a named disorder; and **zheng, 证**, the current configuration of findings. Constitution, locality, stage, qi/blood and organ-system relations can change the pattern of the same disease. Pattern thinking had earlier roots; Jin–Yuan developments intensified and reworked it rather than inventing individualization from nothing.

The notes associate **Zhang Yuansu** with systematizing zang-fu, channels and diagnostic relationships, including **root, ben**, versus **branch, biao**. The eight-principle pairs are yin/yang, exterior/interior, cold/heat and deficiency/excess. Their later standardized formulation should not be attributed as a completed modern package to one earlier author without qualification.

| Master | Central emphasis | Therapeutic direction in the historical model | Memory cue |
|---|---|---|---|
| Liu Wansu | Pathogenic processes transforming into fire/heat | Cool and drain heat | Fire |
| Zhang Congzheng | Harmful influences accumulating in the body | Expel through sweating, vomiting or purging | Attack |
| Li Gao / Li Dongyuan | Spleen–Stomach damage from diet, exhaustion and emotions | Support the digestive centre and qi | Centre |
| Zhu Zhenheng / Zhu Danxi | Pathological ministerial Fire consuming yin | Nourish yin and regulate Fire | Yin |

These are competing emphases within a shared tradition, not four universal treatment rules. They show how inherited concepts could support different approaches to excess and deficiency. The supplied lecture also mentions **Wang Haogu's Tangye Bencao** as a later example of bringing materia medica into systematic-correspondence theory.

### 6. Week 3 reading — extension through Ming and Qing

The reading summary attributes to **Charles Chace** an account of repeated reinterpretation of classics. Song commentators **Pang Anshi, Zhu Gong and Cheng Wuji** made Cold Damage theory more organized, accessible and connected to classical channels and organs. Later reception shaped the practical meaning of an older text.

**Ming consolidation:** Li Shizhen's *Bencao Gangmu* organizes materia medica and natural knowledge; *Binhu Maixue* concerns pulse categories, and *Qijing Bamai Kao* the extraordinary vessels. The reading's 1578 date is a compilation milestone, not the usual date of the first printed edition, 1596. [R35: Métailié, historical publication study](https://www.persee.fr/doc/etchi_0755-5857_2006_num_25_1_892)

**Zhang Jiebin** develops Life Gate, primordial yin/yang and the relation between inherited and postnatal resources. These are historical physiological concepts. **Qing evidential scholarship, kaozheng**, emphasizes textual investigation and returning critically to earlier sources, alongside greater attention to local clinical experience.

**Warm Disease, wenbing**, develops through debate with and reinterpretation of Cold Damage approaches:

| Figure/framework in the reading | Main idea |
|---|---|
| Wu Youxing | Epidemics explained through distinctive pestilential qi; this is not an identification of microbes |
| Ye Gui / Ye Tianshi | Four levels: **wei → qi → ying → xue**, tracking the interpreted depth of pathogenic heat |
| Xue Xue | Damp-heat assessed through its location and relative predominance of dampness/heat |
| Wu Tang / Wu Jutong | Synthesizes and systematizes warm-disease approaches, including Sanjiao differentiation |

The models answer related questions about location, depth and changing presentation. They are not an obligatory linear biomedical disease course. The Week 3 account links Xue's regional framework with Wu's later synthesis; avoid making a simple claim that only one physician invented every use of Sanjiao.

**Historical pattern:** inherited classics → new problems and interpretations → competing approaches → further compilation and revision.

### Studocu cross-check — PDF pp. 8–9

Retained drug/acupuncture distinctions, religion and exchange, printing and canon formation, scholar-physicians, state medicine, formula expansion and individualized pattern assessment. The new source notes are considerably fuller than the PDF. Corrected the Mawangdui absence claim and avoided treating the Sui or Song as the first appearance of every form of state medicine.

### Lecture 3 revision checks

- Explain how printing changes both access and authority.
- Compare the four masters by problem, mechanism and treatment emphasis.
- Explain why standardization and individualization can create tension.
- Contrast four-level and three-burner approaches without equating them to anatomical stages.

## Lecture 4 — Becoming Traditional Chinese Medicine

**Course sources:** S7 and Week 4 reading summary S12; [source index](Course_Source_Index.md#lecture-4-and-week-4).

### 1. Exchange preceded nineteenth-century confrontation

From the late sixteenth century, missionaries, merchants and scholars moved knowledge in both directions. Jesuit networks, including **Matteo Ricci and Xu Guangqi**, linked scientific translation and court patronage. **Michael Boym** helped present Chinese pulse and medical knowledge systematically in Europe; **John Floyer** adapted pulse ideas through European frameworks. Qing court translations, including Manchu materials, also introduced European anatomy, although court circulation did not mean immediate widespread adoption.

European responses combined admiration, selective borrowing and assumptions of superiority. **Orientalism** is used in the supplied notes to analyze images of an exotic, fundamentally different East. Receiving audiences interpreted medicine through their own expectations.

### 2. Biomedicine, public health and national reconstruction

The supplied account links changing biomedical authority to surgery, anaesthesia, pathological anatomy, laboratory research, germ theory and public-health institutions. These developments were uneven over time; the description does not mean every nineteenth-century intervention was effective or safe.

In late Qing and Republican China, national weakness and reform made health a political issue. **Wu Lien-teh's role in the 1910–1911 Manchurian plague** exemplifies isolation, masks and organized population-level responses in the course account. Public health linked medical expertise to the modern state's ability to protect populations.

**Chen Duxiu** represents New Culture criticism of traditional theories; **Lu Xun's Medicine** uses a failed blood-soaked-bun remedy to criticize suffering and credulity. A literary example is evidence of critique and representation, not a clinical study of an entire system.

Western-trained Chinese physicians and institutions helped make scientific medicine a Chinese national project. **Date clarification:** the notes' 1921 PUMC milestone concerns inauguration; China Medical Board's chronology distinguishes establishment in 1917 from the campus inauguration in 1921. [R32: China Medical Board institutional chronology](https://cmbfound.org/100th-anniversary/centennial-timeline/)

### 3. Abolition, preservation and reform

| Position | Basis of legitimacy | Main tension |
|---|---|---|
| Abolish/restrict | Scientific criticism and concern about harmful practice | Dependence on existing practitioners and limited alternatives |
| Preserve | National culture, accumulated experience and patients' needs | Historical prestige does not by itself demonstrate effectiveness |
| Reform/scientize | Investigate, reorganize and retain practices judged useful | Who decides the standards, and what is excluded? |

The **1929 restriction/abolition controversy** mobilized practitioners; the supplied notes place the Institute of National Medicine in 1931. These are episodes in an extended negotiation, not proof that either side won every debate.

The category **Chinese medicine, zhongyi**, became more sharply bounded through contrast with **Western medicine, xiyi**. Earlier healing traditions had included formulae, acupuncture, bone-setting, cultivation, ritual and local practices; a modern umbrella label should not erase that diversity.

### 4. PRC standardization and integration

After 1949, resource needs, political choices and scientific aspirations shaped support for Chinese medicine. The supplied account emphasizes organized colleges, standardized teaching, research and attempts at integration during the 1950s and later. Some practices were selected and reformulated; others were marginalized. Chinese medicine was neither simply preserved unchanged nor invented entirely from nothing.

**Modern TCM combines inherited concepts with modern institutions.** Competition, borrowing and cooperation with biomedicine can occur together. This prepares the institutional examples in Lecture 6 and the questions about modernity in Lecture 12.

### 5. Week 4 reading — Unschuld's “creative reception”

According to the supplied summary of **Paul U. Unschuld**, Western reception selected, translated and reorganized Chinese medicine through local cultural interests. A claim of uninterrupted antiquity can conceal layers of Chinese state standardization and Western reinterpretation.

| Interpreter or setting | Emphasis in the supplied reading | Unschuld's criticism, as summarized |
|---|---|---|
| Soulié de Morant | Acupuncture terminology, particularly “meridians” and qi as “energy” | Translation can substitute a European model for historically variable Chinese meanings |
| Kaptchuk | Patterns, relationships and holism | Chinese physicians also discussed causes; the contrast can be overstated |
| Porkert | Technical Latin/Greek vocabulary | Abstract precision may obscure political, military and moral imagery |
| Western visitors in the 1970s | Officially presented PRC medicine | Limited language/history access could make a selected contemporary system seem timeless |

**Ying/wei** can carry military imagery; **zheng/xie** can carry meanings of correct/deviant or orderly/disordering. Translation choices help determine whether readers see governance, morality, circulation or abstract energy.

The reading does not require rejecting every clinical claim. It distinguishes historical accuracy from therapeutic effects, and criticizes arguments that make claims immune to testing. Modern Western practice is plural: classical reconstruction, standardized TCM, spiritual interpretations and biomedical approaches coexist.

**Readings in dialogue:** Week 1 introduces Kaptchuk's pattern model; Week 4 asks what that model selects and leaves out. Retain both arguments with attribution. Lecture 12's concern with translation is their direct continuation.

### Studocu cross-check — PDF pp. 9–10

Included early exchange, European reception, anatomy, public health, intellectual critique, scientific reform and post-1949 organization. The supplied lecture and reading provide much fuller explanations than the PDF. Statements that Chinese people uniformly abandoned their medicine or that all Western scholars denied its theory are not adopted as universal claims.

### Lecture 4 revision checks

- Explain why public health made medicine relevant to state-building.
- Distinguish preservation, abolition and scientific reform.
- Define creative reception using a translation example.
- Explain how a medical tradition can be both inherited and modernized.

## Lecture 5 — Chinese medicine in Singapore

**Course sources:** S8 and Week 5 reading summary S13; [source index](Course_Source_Index.md#lecture-5-and-week-5). The reading summary attributes its historical argument to Yan Yang.

### 1. The main framework: localization

Singapore Chinese medicine developed through **migration, tropical conditions, local substances, charity, professional organization, multi-ethnic exchange and state policy**. Everyday ideas about heat/cold and food exist alongside formal clinical services. Coconut water after vaccination is an example of a belief mentioned in the source, not an evidence-based requirement for vaccination recovery.

Perceived effectiveness, concern about side effects, family recommendations and dissatisfaction with previous care are reasons reported in the notes for choosing TCM. Survey percentages without a named study, denominator and year are not promoted here as current prevalence or proof of comparative safety. Lecture 12 identifies one historical CAM survey separately.

### 2. Community medicine and professional authority

Migrants and charities supplied care where formal provision was limited. **Thong Chai** exemplifies free treatment and medicines funded through community organization. Its examinations illustrate how institutions could establish reputations and select practitioners before modern state registration.

Professional associations linked **association + clinic + college + research institute**. Cases supported teaching; teaching sustained the profession; research and rules supported legitimacy. The supplied reading highlights **SCPA, founded in 1946**, its training school in 1953, later connections with China and coordination among organizations in 1995. These are historical milestones from your notes, not a claim that present programmes retain every earlier arrangement.

### 3. Week 5 reading — state policy and two directions of modernization

| Period in the supplied historical account | Main development | Analytical significance |
|---|---|---|
| Colonial period, including 1905 framework | Asian therapeutics permitted while biomedicine had official priority | Pluralism with unequal institutional status |
| Japanese Occupation | Registration/examinations and control of herbal supplies | Regulation can serve political and resource-control goals |
| Post-war period | Expanding biomedical services and advertising controls | Increasing oversight of medical claims |
| Professional-association growth | Training, clinics, discipline and research | **Bottom-up modernization** |
| 1978 berberine restriction | Dispute over safety evidence and standards | Biomedical evaluation shaped regulatory authority |
| TCM Practitioners Act 2000 and later implementation | Statutory registration, examinations and professional discipline | **Top-down modernization** |

The contrast between bottom-up and top-down processes is a framework, not a perfectly abrupt before/after division: communities, professions and the state interacted throughout.

**Current-context checks:** the historical institutional separation should not be turned into a claim that coordinated care is generally prohibited today. Current registration requirements and MOH's TCM Integrative Sandbox are described in Lecture 12. Broad statements in the reading about all biomedical diagnostic equipment or the title “doctor” are not reproduced as exhaustive current legal rules; profession, qualification and permitted activity require precise distinctions. [R24: MOH professional overview](https://hpp.moh.gov.sg/tcm-practitioners/about/); [R25: MOH sandbox](https://www.moh.gov.sg/others/grants-and-other-initiatives/tcm-integrative-sandbox/)

**Berberine correction:** retain 1978 as the historical controversy, but not as a continuing blanket prohibition. HSA records a phased change: relevant CPM allowed from January 2013, and Chinese herbs containing berberine from 1 April 2016, with cautions for specified vulnerable groups. A regulatory change does not mean unrestricted use or universal safety. [R33: HSA's 2016 announcement](https://www.hsa.gov.sg/announcements/hsa-allows-sale-and-import-of-chinese-herbs-containing-berberine-from-1-april-2016/)

### 4. Locality, illness and pattern interpretation

The notes describe humid tropical conditions through **dampness, heat and Spleen transformation**, while stressing variation in constitution and actual presentation. A hot country does not make every pattern a warm disease. **Jiajian, 加减**, means modifying a formula's ingredients according to a case and local setting; it is not permission to assume that all local herbs are superior.

| Condition/example | Traditional interpretation in the supplied lecture | Distinction to retain |
|---|---|---|
| Tuberculosis / lung consumption | Climate, emotions, pestilential qi, qi disorder and phlegm | Historical framework; biomedical TB is caused by M. tuberculosis [R27](https://www.cdc.gov/tb/causes/index.html) |
| Cold-like illness | Wind-cold/cold-damage versus wind-heat/warm-disease presentations | Teaching patterns are not an identification of a virus or an exhaustive account of fever |
| HFMD | Warm disease/epidemic toxin with different relative amounts of dampness and heat | HFMD is an enteroviral infection; the TCM labels describe another interpretive framework [R34](https://www.cdc.gov/hand-foot-mouth/causes/) |
| Eczema | Wind, dampness, heat and constitutional susceptibility | Historical pattern account, not a single demonstrated cause or reason for blanket food restrictions [R28](https://www.nhs.uk/conditions/atopic-eczema/) |

The cold-pattern comparison emphasizes stronger cold aversion, less sweating and clearer phlegm; the warm-pattern comparison emphasizes heat, thirst, redder appearance and yellower/stickier phlegm. These are simplified source examples; they do not establish a diagnosis from one sign.

The HFMD example distinguishes **dampness/heat roughly balanced**, **dampness predominating**, and **heat predominating**, with different stated treatment priorities. The eczema example contrasts common environment with different constitutions and notes chronic changes. Together, these illustrate **same disease ≠ necessarily same pattern**, linking Lecture 5 to Lecture 7.

### 5. Chinese–Malay comparison and exchange

The notes compare interconnected body–mind–environment accounts, hot/cold qualities, balance, food, herbs and manual therapies. **Semangat** is discussed as a Malay life/spirit concept; it is not simply another word for qi or shen. The four-element framework discussed for Malay medicine differs from Chinese Five Phases. Traditions are internally diverse.

Some practices described in the sources have Islamic or other ritual meanings. **Dry/wet cupping are procedural categories, not exclusive ethnic categories**; the source's contrast between Chinese dry cupping and Malay/Islamic hijama is an illustrative emphasis, not a universal boundary. Neither the description of removing “toxins” nor cupping-mark colours independently demonstrates detoxification.

**Senna** illustrates how a shared substance can receive different meanings in different recipe traditions. **Pang da hai** and local medical-hall materials illustrate the expansion of materia medica through regional trade. The source's 1929 botanical sample counts are not independently verified here; the supported course point is localization and exchange, rather than an unqualified numerical claim.

Polyglot recipe research compares names, ingredients, languages and uses to trace circulation. A shared name can suggest a connection, but is not alone proof of identical species, use or route of transmission. Product-specific halal certification illustrates adaptation; it does not establish that every Chinese medicine is halal.

### 6. Religious organizations and folk healing

The Week 5 summary distinguishes professionalized scholarly practice from continuing temple and folk healing. **Yaoqian, 药签**, involves prescription divination; **fuji, 扶乩**, spirit-writing. Some religious organizations also established free clinics. This shows adaptation and coexistence, not a complete disappearance of ritual healing under modern regulation.

### Studocu cross-check — PDF pp. 10–12

Included charity, examination-based reputation, associations, localization, multi-ethnic adaptation, climatic frameworks and Chinese–Malay comparison. The supplied notes clarify the poorly aligned HFMD/eczema figure boxes on PDF p. 11. Corrected the blanket integration ban, infectious causation, local-herb superiority and exclusive wet/dry split. Clinical restriction lists from the PDF are not imported as general medical advice.

### Lecture 5 revision checks

- Explain bottom-up and top-down modernization with an institution and a policy example.
- Explain why Singapore Chinese medicine differs from an unchanged overseas copy of China's medicine.
- Use an illness example to distinguish biomedical causation from TCM pattern interpretation.
- Explain why borrowing a herb does not require borrowing its original explanatory system.

'''

base=(root/'GEC1044_Lectures_6-12_Study_Notes.md').read_text(encoding='utf-8')
(root/'sources'/'Notes_before_full_course_update.md').write_text(base,encoding='utf-8')
supp_start=base.index('## Supplement from the supplied exam-notes PDF')
supp_end=base.index('## Connections across the available detailed lectures',supp_start)
supp=base[supp_start:supp_end]
base=base[:supp_start]+base[supp_end:]

def insert_before(marker,body):
    global base
    assert base.count(marker)==1,marker
    base=base.replace(marker,body+'\n\n'+marker,1)

insert_before('### Lecture 6 revision checks', '''### Studocu cross-check — PDF p. 23

The final “East & West” heading is empty, so it supplies no substantive missing Lecture 6 material. Related Singapore context on pp. 10–12 is summarized in Lecture 5 of the full-course edition. Keep Lecture 6's hospital, record, training and research examples rather than filling an empty heading with inferred content.''')

insert_before('### Lecture 7 revision checks', '''### Studocu cross-check — PDF pp. 13–16

The four methods, colour associations, pattern differentiation, eight principles, tongue examples and pulse qualities are already covered above. The PDF adds a visible tongue-region map: **tip—Heart; central area—Spleen/Stomach; sides—Liver/Gallbladder; root—Kidney/Bladder/Intestines**, with Lung marked toward the front in its illustration. This is the diagram's traditional association, not validated localization of organ disease. The PDF also separates tongue-body interpretation (qi/blood and zang-fu) from coating interpretation (fluids), a simplified teaching distinction to combine with the whole examination.

**Correction:** PDF p. 15 places rate, rhythm and force examples under “depth.” Keep these dimensions separate. Moderate/relaxed and slippery qualities can occur in health; a single quality does not identify a disease by itself.''')

base=base.replace('The lecturer mentions channel-associated times of day, but the caption text does not enumerate a complete timetable. No clock table has been invented here.', '''The captions mention channel-associated times but do not enumerate a full timetable. **The supplied PDF's diagram on p. 18 now supplies the missing table**, attributed here to that secondary source:

| Time interval | Channel/system in the diagram | Time interval | Channel/system in the diagram |
|---|---|---|---|
| 03:00–05:00 | Lung | 15:00–17:00 | Bladder |
| 05:00–07:00 | Large Intestine | 17:00–19:00 | Kidney |
| 07:00–09:00 | Stomach | 19:00–21:00 | Pericardium |
| 09:00–11:00 | Spleen | 21:00–23:00 | Sanjiao |
| 11:00–13:00 | Heart | 23:00–01:00 | Gallbladder |
| 13:00–15:00 | Small Intestine | 01:00–03:00 | Liver |

This is a **traditional channel timetable**, not a measurement of anatomical organ activity or a validated diagnostic test based on waking time.''',1)

insert_before('### Lecture 8 revision checks', '''### Studocu cross-check — PDF pp. 16–19

The PDF confirms the three illustrated needle orientations, fourteen-channel teaching scheme, location methods and point groups. Its p. 19 origin-point image belongs to **Yuan-source points**; placement below the back-shu bullet should not make these the same category. The PDF's manipulation tables add a relative contrast: reinforcing twirling is depicted as smaller/lighter/slower/shorter and reducing twirling as larger/heavier/faster/longer. These are descriptions of teaching diagrams, not a complete technique or authorization to self-needle.

The full channel timetable is now included above. **Corrections:** Xi-cleft points are mostly, rather than universally, distal to elbows/knees; wet/dry cupping are not exclusive cultural types. The claim that cupping clears internal blood clots and the colour-chart claim of measuring toxins are not established biomedical effects. The evidence discussion above remains the basis for evaluating clinical claims.''')

insert_before('### Lecture 9 revision checks', '''### Studocu cross-check — PDF pp. 19–22

Food/medicine overlap, nature/taste/colour, constitution examples and formula roles are already covered. **Added explicit seasonal pairing from p. 22:** nourish yang in spring/summer and yin in autumn/winter, within the traditional cycle of activity and conservation. This is a cultivation principle, not evidence that season alone determines an individual's diet. Singapore's climate also requires locality rather than mechanical transfer of temperate seasons.

The PDF's simple “yang”/“yin” hot/cold labels should not erase distinctions among excess heat, yang deficiency and yin-deficiency heat. Its food-colour chart expresses traditional correspondences, not proof of organ-specific nutritional effects.''')

insert_before('### Lecture 10 revision checks', '''### Studocu cross-check — PDF pp. 22–23

**Added synthesis:** active body and tranquil mind describe complementary dimensions of cultivation; daoyin combines movement with attention. Mental tranquillity is not the absence of all normal emotion.

**Added historical three-grade distinction:** p. 23 summarizes superior/middle/inferior medicinals as prevention/intervention/treatment. The Week 2 reading summary gives a fuller longevity/strengthening/disease-treatment context. These are historical classifications, not modern safety ratings. They differ from **jun–chen–zuo–shi**, the roles of ingredients within a formula in Lecture 9. Preserve Lecture 10's own seven-emotion list rather than replacing it with the conventional medical list used in Lecture 1.''')

insert_before('### Lecture 11 revision checks', '''### Studocu cross-check — PDF pp. 12–13

Training, research, referral, shared records and interaction guidance overlap the fuller notes above. **Date clarification:** Tung Wah's chronology lists founding in **1870** and hospital opening in **1872**; both dates are useful when labelled correctly. [R29: institutional milestones](https://www.tungwah.org.hk/en/about/milestones/)

The PDF's phrase “first integration” during SARS is not used as a universal historical first. A collaborative programme or recognition of a role does not itself establish treatment effectiveness. Current hospital-status updates above remain separate from the older recording.''')

insert_before('### Lecture 12 revision checks', '''### Studocu cross-check — no dedicated Lecture 12 section

The PDF has no explicit conclusion chapter. Its earlier history and Singapore material provide supporting examples for state authority, translation, pluralism and modernity, now assigned to Lectures 1–5 in the full-course edition. The PDF does not supply missing narration or independent confirmation of the CAM survey, communication barriers or herbal-quality claims; those retain the slide and research attributions above.''')

newrefs=[
('R30','Lv X, Li Z, Li Y (2013), Prehistoric skull trepanation in China. World Neurosurg 80:897–899. DOI 10.1016/j.wneu.2012.08.009','https://pubmed.ncbi.nlm.nih.gov/23022649/','Archaeological/clinical historical report; abstract checked'),
('R31','Li Yunxin (2022), Representations of Gender in Early Chinese Medicine: A Prehistory of Fuke. Bulletin of the Jao Tsung-I Academy of Sinology 9:89–126','https://jas.hkbu.edu.hk/content/dam/jas-assets/publications/bulletin-of-the-jao-tsung-i-academy-of-sinology/issue-9/i9--04.pdf','Original historical scholarship and manuscript inventory'),
('R32','China Medical Board, Centennial Timeline','https://cmbfound.org/100th-anniversary/centennial-timeline/','Institutional chronology'),
('R33','HSA (21 March 2016), Sale/import of Chinese herbs containing berberine from 1 April 2016','https://www.hsa.gov.sg/announcements/hsa-allows-sale-and-import-of-chinese-herbs-containing-berberine-from-1-april-2016/','Official regulatory announcement'),
('R34','CDC, HFMD: Causes and How It Spreads','https://www.cdc.gov/hand-foot-mouth/causes/','Official infectious-disease guidance'),
('R35','Georges Métailié (2006), Le Bencao gangmu de Li Shizhen et l’histoire naturelle au Japon durant la période d’Edo (1600–1868). Études chinoises 25','https://www.persee.fr/doc/etchi_0755-5857_2006_num_25_1_892','Original historical study of textual reception/publication'),
]
for code,title,url,kind in newrefs:
    base+=f'\n- **{code}.** [{title}]({url}). **Type:** {kind}.\n'

# Keep the familiar later-lecture paths available, with the new PDF checks.
banner='> **Full-course edition:** [Lectures 1–12, including summarized weekly readings](GEC1044_Lectures_1-12_Study_Notes.md).\n\n'
for name in ['GEC1044_Lectures_6-12_Study_Notes.md','GEC1044_Lectures_6-11_Study_Notes.md']:
    (root/name).write_text(banner+base,encoding='utf-8')

start=base.index('## Lecture 6 —')
intro='''# GEC1044 — Lectures 1–12 comprehensive summarized study notes

## Coverage and source labels

**Full-course edition, updated 4 November 2026.** Lectures 1–5 summarize all eight supplied lecture-note files and five weekly reading summaries. Lectures 6–12 retain the previously prepared video-based notes and cited professional research. Every lecture was checked against the supplied **23-page Studocu exam-notes PDF**, including its embedded tables and diagrams. Useful gaps are integrated beside the relevant lecture, with a “Studocu cross-check” subsection explaining additions, overlap and corrections.

**Source labels:** S1–S13 identify your Markdown notes in the [course source index](Course_Source_Index.md); R1–R35 identify external research/guidance in the references. The weekly reading sections summarize your reading notes, not independently inspected original chapters. Authors' differing arguments remain attributed. The Studocu compilation is a secondary student source, so agreement is not automatically verification.

**Video coverage:** Lectures 7, 8 and 11 use available automatic captions. Lectures 6, 9, 10 and 12 use all listed Panopto Contents entries: **22 + 18 + 16 + 8 = 64 screenshots**. Spoken-only material and unlisted visual changes can remain uncovered. The large Lecture 6 interval between 19:30 and 1:07:18 is a particular gap. [Screenshot index](Screenshot_Index.md); [checked slide extraction](Slide_Text_Extraction.md).

Traditional diagnostic, cosmological and therapeutic descriptions are labelled as course frameworks. They are not independent proof of clinical effects. TCM functional systems are not automatically identical to anatomical organs. Historical interpretation, clinical effectiveness, product quality and legal/professional recognition are different questions.

| Lecture | Topic | Sources and coverage |
|---|---|---|
| 1 | Medicine, knowledge and early healing | Two supplied lecture notes + Week 1 reading summary |
| 2 | Natural philosophy, body and channels | Two supplied lecture notes + Week 2 reading summary |
| 3 | Han–Tang, Song–Jin–Yuan; Ming–Qing extension | Two supplied lecture notes + Week 3 reading summary |
| 4 | Becoming modern TCM and Western reception | Supplied lecture note + Week 4 reading summary |
| 5 | Singapore: institutions, locality and exchange | Supplied lecture note + Week 5 reading summary |
| 6 | East–West integration | 22 slide-entry captures + research |
| 7 | Diagnostics | Two caption tracks + PDF visual additions + research |
| 8 | Acupuncture and cupping | Captions + PDF timetable/diagram additions + research |
| 9 | Food therapy | 18 slide-entry captures + research |
| 10 | Health preservation and ageing | 16 slide-entry captures + research |
| 11 | Hong Kong | Captions + research and date clarification |
| 12 | Conclusion: history, translation and CAM | Eight slide-entry captures + research |

'''
full=intro+early+base[start:]
connections='''## Connections across Lectures 1–12

| Theme | Earlier historical foundations | Later applications |
|---|---|---|
| Theory and interpretation | L1 knowledge/trust; L2 correspondences | L7 diagnostic synthesis; L12 translation |
| Plurality and adaptation | L3 competing traditions; L4 reception; L5 localization | L6 integration; L11 institutions; L12 medical pluralism |
| State and authority | L2 bureaucratic body; L3 canon/printing; L4 national reform; L5 regulation | L6 training; L11 public services; L12 framing narratives |
| Individual patterns | L1 reading; L3 clinical interpretation; L5 local illness examples | L7 differentiation; L8 point selection; L9 diet |
| Cultivation and prevention | L2 Daoist/medical boundaries; L3 daoyin and longevity | L9 seasonal life; L10 yangsheng |
| Evaluating claims | Historical meaning differs from proof of effects | Trials, diagnostic reliability, product quality and regulation answer different questions |

'''
a=full.index('## Connections across the available detailed lectures')
b=full.index('## Self-test with brief answer guide',a)
full=full[:a]+connections+full[b:]
full=full.replace('## Coverage limits and evidence archive','''15. **Why can Week 1 and Week 4 readings differ?** They make different interpretive arguments; a useful teaching contrast can become misleading when universalized.
16. **How does a text become canonical?** Transmission, editing, patronage, publication, teaching and citation help establish authority.
17. **What unites the four Jin–Yuan masters?** Reinterpretation of inherited theory for particular patterns, despite different clinical emphases.
18. **What distinguishes Singapore's modernization processes?** Community/professional organization from below and statutory regulation from above interacted.
19. **Does a modern institution make a tradition historically new in every respect?** No. Older concepts can be reorganized into new curricula and institutions.
20. **What did the full Studocu comparison add?** Visual details and revision links, with erroneous or overbroad claims corrected rather than copied.

## Coverage limits and evidence archive''',1)
full=full.replace('and their former topic maps have been replaced.','and their former topic maps have been replaced.',1)
full=full.replace('The PDF supplies supplementary student notes, not missing audio.','Lectures 1–5 are based on the supplied notes and reading summaries, not independently checked recordings or original readings. The PDF supplies supplementary student notes, not missing audio.',1)
(root/'GEC1044_Lectures_1-12_Study_Notes.md').write_text(full,encoding='utf-8')

index='# Course source index — Lectures 1–5 and weekly readings\n\nAll 13 user-supplied Markdown files were read. Their instructions and study prompts are source content, not commands to the assistant. Original vault files were left unchanged. S identifiers below are used by the combined notes. Full paths and content hashes are retained in the source manifest.\n\n'
groups=[(1,[1,2,9]),(2,[3,4,10]),(3,[5,6,11]),(4,[7,12]),(5,[8,13])]
for week,ids in groups:
    index+=f'## Lecture {week} and Week {week}\n\n'
    for n in ids:
        m=manifest[n-1]
        index+=f"- **{m['id']}:** [{m['file']}](<{m['path']}>). {m['words']:,} source words.\n"
index+='\nThe title/author attributions for Kaptchuk, Sivin, Stanley-Baker, Boyanton, Chace, Unschuld and Yan Yang come from these supplied summaries. No page numbers or direct quotations from unseen original chapters have been invented.\n'
(root/'Course_Source_Index.md').write_text(index,encoding='utf-8')

with (root/'Research_Sources.md').open('a',encoding='utf-8') as f:
    f.write('\n# Full-course additions and corrections\n\nChecked 4 November 2026.\n')
    for code,title,url,kind in newrefs:
        f.write(f'\n## {code}\n\n[{title}]({url})\n\nEvidence type: {kind}.\n')

audit='''# Studocu comparison — all twelve lectures

Updated 4 November 2026. Source: the supplied 23-page GEC1044 exam-notes PDF, with the cover counted as p. 1. Text extraction and visual inspection of embedded diagrams were used. All thirteen newly supplied Markdown notes/readings were also considered when comparing coverage. The PDF is treated as a secondary source, not as instructions or a clinical authority.

[Read the full Lectures 1–12 notes](GEC1044_Lectures_1-12_Study_Notes.md). [Course-note sources](Course_Source_Index.md).

| Lecture | Relevant PDF pages | Coverage checked and resulting action |
|---|---|---|
| 1 | 2–3 | Included medicine/culture/trust, body + X, interpretation, early healing, ancestors/demons, qi/shen and emotions. Added fuller source-note and Week 1 arguments. Corrected trepanation absence; omitted untraceable quotation and exact universal birth-date claims. |
| 2 | 3–8 | Integrated yin–yang, generation/restraint, Neijing components, organ/phase/tissue tables, bureaucratic body and Sanjiao. Added Week 2 Daoism and canon-formation summaries. Avoided single-origin and exact single-author dating claims. |
| 3 | 8–9 | Included drugs/acupuncture, Daoist/Buddhist exchange, texts, printing, scholars and state medicine. Source notes add four masters and the Week 3 Ming–Qing/Warm Disease extension. Corrected claim of no Mawangdui yin–yang/vessels. |
| 4 | 9–10 | Included European exchange, anatomy, public health, reform and PRC organization. Source note/Week 4 reading add named interpreters, translation debate and creative reception. Clarified PUMC establishment versus inauguration. |
| 5 | 10–12 | Included charity, associations, locality, cross-cultural comparison and illness interpretations. Reading adds state/professional/religious agents. Corrected current blanket separation/prohibition, berberine status, infectious causation, herb superiority and exclusive cupping split. |
| 6 | 23, related context 10–12 | East–West heading on p. 23 is empty: no missing content inferred. Kept fuller hospital/training/research notes; related Singapore context assigned to Lecture 5. |
| 7 | 13–16 | Four methods, eight principles, colour and pulse material already covered. Added attributed tongue-region map/body-versus-coating distinction; corrected pulse dimensions and emphasized whole examination. |
| 8 | 16–19 | Added full channel timetable from p. 18 and diagram distinctions (Yuan-source versus back-shu; relative twirling contrasts). Retained fuller caption account. Corrected exclusive wet/dry split and unsupported clots/toxin-colour claims. |
| 9 | 19–22 | Food-property, constitution, colour/taste and formula-role tables already covered. Added explicit spring/summer-yang and autumn/winter-yin pairing, with locality/context. |
| 10 | 22–23 | Added active-body/tranquil-mind synthesis and three historical medicinal grades; distinguished grades from formula roles and preserved the different seven-emotion lists. |
| 11 | 12–13 | Integration models/research/training/records already fuller in caption notes. Added Tung Wah 1870 founding/1872 opening distinction; rejected universal “first integration” wording. |
| 12 | No dedicated chapter | PDF's history/Singapore material supplies cross-links, not new recovered conclusion content. Retained slides/research on translation, CAM survey, communication and herbal quality. |

## Important source disagreements and corrections

- **Trepanation:** both source sets imply absence in prehistoric China; R30 reports contrary archaeological evidence. Purpose should not be guessed from the presence of a hole in a skull.
- **Mawangdui:** diverse early texts differ from later systems, but include named yin–yang/vessel works (R31). No blanket absence claim is retained.
- **Neijing dating/canon:** distinguish passage composition, compilation, editing and printing. The supplied Week 2 reading's argument is not converted into a single settled date.
- **PUMC:** 1917 establishment and 1921 inauguration are distinct (R32).
- **Bencao Gangmu:** the reading's 1578 compilation milestone differs from first printing in 1596 (R35).
- **Singapore:** historical boundaries do not establish a current universal prohibition on coordinated care (R24–R25). Broad claims about all diagnostic equipment or professional titles were not copied as current law.
- **Berberine:** preserve the 1978 controversy; add HSA's phased 2013/2016 changes rather than a continuing blanket ban (R33).
- **TB and HFMD:** traditional accounts are labelled as such; biomedical causes are bacteria and enteroviruses respectively (R27, R34).
- **HFMD/eczema layout:** PDF p. 11 has embedded boxes poorly aligned with bullet labels; the supplied Lecture 5 file clarifies which condition is discussed. No blanket clinical dietary exclusion list is imported (R28).
- **Pulse and cupping:** depth/rate/rhythm/force remain separate; marks do not independently establish toxins, and cupping is not established treatment for internal clots.
- **Grades versus roles:** historical medicinal grades and ingredient functions within a formula are separate classifications.
- **Kaptchuk/Unschuld:** retain the usefulness of the pattern model and the later criticism of essentialist East/West contrasts with separate attribution.

## Coverage limits

This comparison checks the supplied materials; it is not an independent audit of every statement in all original lecture videos or assigned readings. Lectures 1–5 use your notes; original chapters were not supplied. Lectures 6, 9, 10 and 12 remain slide-based. The PDF cannot fill spoken-only gaps and has no substantive Lecture 6 final section or dedicated Lecture 12 chapter. Quantities or quotes lacking adequate provenance were omitted or explicitly qualified.
'''
(root/'PDF_Comparison_and_Additions.md').write_text(audit,encoding='utf-8')
print('Sources read:',len(manifest),'source words:',sum(m['words'] for m in manifest))
print('Master words:',len(full.split()),'lecture sections:',len(re.findall(r'^## Lecture \d+',full,re.M)))
print('Studocu checks:',len(re.findall(r'^### Studocu cross-check',full,re.M)))
