from pathlib import Path
import re, json

root=Path(__file__).parent
path=root/'GEC1044_Lectures_6-11_Study_Notes.md'
text=path.read_text(encoding='utf-8')
backup=root/'sources'/'Notes_before_research.md'
if not backup.exists(): backup.write_text(text,encoding='utf-8')

sources={
'R1':('Tu Youyou (2015), Nobel biographical account: extraction, isolation and drug development','https://www.nobelprize.org/prizes/medicine/2015/tu/biographical/','First-person scientific/historical account'),
'R2':('WHO, Traditional medicine: ICD-11 frequently asked questions','https://www.who.int/standards/classifications/frequently-asked-questions/traditional-medicine','Official classification guidance'),
'R3':('TCMPB (5 October 2026), Implementation of the Clinical Competency Assessment','https://www.tcmpb.gov.sg/publications-and-newsroom/announcements/implementation-of-the-clinical-competency-assessment--cca--for-the-tcmpb-qualifying-examinations-for-registration/','Official current professional-assessment announcement'),
'R4':('Wang ZC et al. (2020), Intra-Rater and Inter-Rater Reliability of Tongue Coating Diagnosis Using Smartphones. JMIR Mhealth Uhealth 8:e16018','https://mhealth.jmir.org/2020/7/e16018','Primary diagnostic-reliability study; DOI 10.2196/16018'),
'R5':('Vickers AJ et al. (2018), Acupuncture for Chronic Pain: Update of an Individual Patient Data Meta-Analysis. J Pain 19:455–474','https://keele-repository.worktribe.com/output/409834','Original pooled analysis of individual trial data; DOI 10.1016/j.jpain.2017.11.005'),
'R6':('Liu S et al. (2021), A neuroanatomical basis for electroacupuncture to drive the vagal–adrenal axis. Nature 598:641–645','https://pmc.ncbi.nlm.nih.gov/articles/PMC9178665/','Primary mechanistic animal experiment; DOI 10.1038/s41586-021-04001-4'),
'R7':('NCCIH, Acupuncture: Effectiveness and Safety','https://www.nccih.nih.gov/health/acupuncture-effectiveness-and-safety','NIH professional/public evidence summary'),
'R8':('NCCIH, Cupping','https://www.nccih.nih.gov/health/cupping','NIH evidence and safety summary'),
'R9':('Estruch R et al. (2018), Primary Prevention of Cardiovascular Disease with a Mediterranean Diet Supplemented with Extra-Virgin Olive Oil or Nuts. N Engl J Med 378:e34','https://www.nejm.org/doi/full/10.1056/NEJMoa1800389','Republished primary PREDIMED trial analysis; DOI 10.1056/NEJMoa1800389'),
'R10':('WHO, Healthy diet','https://www.who.int/news-room/fact-sheets/detail/healthy-diet','Official nutrition guidance'),
'R11':('Memorial Sloan Kettering Cancer Center, Oldenlandia diffusa','https://www.mskcc.org/cancer-care/integrative-medicine/herbs/oldenlandia-diffusa','Specialist cancer-centre clinical herb monograph'),
'R12':('Hong Kong Hospital Authority, Atlas of Poisonous Plants: Xanthium sibiricum (cocklebur)','https://www3.ha.org.hk/toxicplant/en/xanthium_sibiricum.html','Clinical toxicology reference'),
'R13':('Tou NX et al. (2024), Effectiveness of community-based Baduanjin exercise intervention for older adults with varying frailty status: a randomized controlled trial. Eur Rev Aging Phys Act 21:28','https://link.springer.com/article/10.1186/s11556-024-00363-6','Primary assessor-blind randomized trial in Singapore'),
'R14':('WHO (2020), Guidelines on Physical Activity and Sedentary Behaviour: recommendations','https://www.ncbi.nlm.nih.gov/books/NBK566046/','Official evidence-based activity guideline'),
'R15':('Wellcome Collection, Daoyin Tu image catalogue: Mawangdui Tomb 3','https://wellcomecollection.org/works/sybqrqu7','Museum/library historical object catalogue'),
'R16':('Zhong LL-D et al. (2022), Effects of Chinese medicine for COVID-19 rehabilitation: a multicenter observational study. Chinese Medicine 17:99','https://pubmed.ncbi.nlm.nih.gov/35996191/','Primary uncontrolled observational cohort; DOI 10.1186/s13020-022-00654-z'),
'R17':('Zhong LL-D et al. (2022), Correction to the COVID-19 rehabilitation study. Chinese Medicine 17:120','https://link.springer.com/article/10.1186/s13020-022-00674-9','Published correction to R16'),
'R18':('Hong Kong Government (21 October 2026), Operation and services of Chinese Medicine Hospital of Hong Kong','https://www.info.gov.hk/gia/general/202610/21/P2026102100478.htm','Official operational update'),
'R19':('Hong Kong Government (25 August 2026), Hospital service expansion and planned 24-hour inpatient launch','https://www.info.gov.hk/gia/general/202608/25/P2026082500323.htm','Official forward service plan'),
}

def cite(k,label=None):
    return f'[{k}: {label or sources[k][0]}]({sources[k][1]})'

research={
6:f'''### Additional research — integration, translation and current assessment

**Traditional knowledge can generate a testable lead.** Tu Youyou's own account describes moving from herbal extracts to a reproducible active fraction, isolation of artemisinin, chemical characterization and further drug-development work. It also emphasizes identifying the correct plant species and preparation. This adds a concrete research pathway to the lecture's Nobel example: **historical observation → candidate selection → controlled extraction → identification → testing → standardized medicine**. Evidence about the isolated product does not automatically transfer to any tea, dose or multi-herb mixture. {cite('R1','Tu Youyou’s scientific account')}

**Integration also needs compatible information.** WHO explains that ICD-11 traditional-medicine categories support standardized reporting and optional dual coding alongside conventional diagnoses. WHO explicitly separates classification from endorsement of a practice or intervention. Thus an institutional milestone and a clinical-effectiveness finding answer different questions. {cite('R2','WHO explanation of traditional-medicine coding')}

**Current update, checked 4 November 2026.** TCMPB's 5 October 2026 announcement confirms that modified STRE began in August 2025 and applied in 2026, with the first Clinical Competency Assessment scheduled for 2027. This verifies the slide's direction of change. The announcement also distinguishes central administration in 2027 from school administration with Board oversight from 2028. These details are external updates, not additional words recovered from the recording. {cite('R3','TCMPB October 2026 announcement')}

**Research question to retain:** Does a proposed integrated service improve an outcome patients value, compared with a clearly defined alternative, while monitoring harms? Co-location, professional recognition and a shared database can enable a service; their existence alone does not answer that clinical question. This is an interpretation connecting the lecture to research design.

''',
7:f'''### Additional research — reproducibility is different from diagnostic validity

**A directly relevant reliability study.** Wang and colleagues developed standardized tongue-coating definitions and a smartphone photography protocol using a quasi-Delphi process involving 18 clinicians. In the selected-image assessment, agreement between clinicians was moderate for coating colour/texture (Gwet AC2 0.49–0.55) and fair for tongue-body colour/features (0.34). Some same-observer comparisons were stronger, but reliability varied by feature. This supports Lecture 7's emphasis on training and standardization while showing why observers cannot be assumed to agree perfectly. {cite('R4','Wang et al., 2020, diagnostic-reliability study')}

Two different questions must be distinguished:

| Question | Meaning | What would need to be tested? |
|---|---|---|
| Reliability | Do repeated observers or measurements produce similar descriptions? | Agreement under standardized conditions |
| Validity/accuracy | Does the observation identify the intended clinical condition? | Comparison against an appropriate reference standard in a representative population |
| Clinical usefulness | Does using the observation improve decisions or outcomes? | Evaluation of the resulting care pathway |

The table is a methodological explanation. The tongue-image study tests reproducibility; it does **not** establish that a purple tongue diagnoses a particular disease or that an organ-area map predicts treatment benefit. A technology can standardize image capture without validating every interpretation applied to the image.

**Connection to the four methods:** combining history, inspection and other findings is sensible information gathering, but the combined method still needs its own evaluation. More observations do not automatically remove measurement error. This is an inference from the distinction above, not a result reported by the lecturer.

''',
8:f'''### Additional research — clinical effects, mechanisms and cupping evidence

**Clinical pain evidence.** Vickers and colleagues' 2018 individual-patient-data analysis pooled 39 randomized trials with 20,827 participants with chronic pain conditions. Acupuncture performed better than no-acupuncture controls and sham controls; the average difference was larger against no acupuncture (about 0.5 standard deviations) than against sham (about 0.2). The result concerns the studied pain conditions and treatment packages; it does not validate every condition or point indication listed in the lecture. {cite('R5','Vickers et al., 2018, original pooled trial analysis')}

**Why the comparator matters.** A no-acupuncture comparison estimates the effect of adding the whole treatment encounter, including attention and expectations. A sham comparison asks a narrower question, although sham procedures can themselves stimulate tissues. NCCIH discusses nervous-system, local-tissue and nonspecific effects and notes that the mechanism is not fully understood. These explanations complement, rather than experimentally prove, the lecture's qi/meridian account. {cite('R7','NCCIH mechanism and effectiveness summary')}

**A specific experimental mechanism.** Liu and colleagues investigated electroacupuncture in mice and identified a role for PROKR2-marked sensory neurons in recruiting a vagal–adrenal pathway under particular hindlimb stimulation conditions. This provides a testable neuroanatomical mechanism for a specific experimental intervention. It is **animal mechanistic evidence**, not a human treatment trial or a demonstration that all meridian claims are correct. {cite('R6','Liu et al., Nature, 2021')}

**Cupping needs a separate evidence assessment.** NCCIH describes possible pain relief but weak evidence and predominantly low-quality research; it does not establish broad benefits for other conditions. The agency also documents burns, infection, scarring and other adverse effects. Nothing in that assessment validates cup-mark colour as a measure of toxins or clot burden. The lecture's cupping-mark chart should therefore remain labelled as traditional interpretation. {cite('R8','NCCIH cupping assessment')}

**How to read an acupuncture claim:** identify the condition, intervention, comparison, outcome and follow-up. A finding about pain scores is not automatically a finding about disease cure, and a statistically detectable difference may be small. Those are research-reading principles, not additional results from any one trial.

''',
9:f'''### Additional research — diet evidence and the food–medicine boundary

**Diet can affect disease outcomes, but the tested pattern matters.** The republished PREDIMED analysis included 7,447 adults at high cardiovascular risk. Mediterranean-diet groups supplemented with extra-virgin olive oil or nuts had fewer major cardiovascular events than the comparison diet. The republication addressed allocation irregularities using revised analyses. This is evidence about a specified dietary intervention and population; it does **not** test the five-taste/organ correspondence table. {cite('R9','Estruch et al., NEJM, 2018')}

**A modern comparison with “harmony.”** WHO describes healthy diets through adequacy, balance, moderation and diversity. Its guidance emphasizes whole grains, vegetables, fruit and pulses; for people older than ten it specifies at least 400 g of fruit/vegetables daily, and for adults less than 5 g of salt daily. This makes an important distinction for the lecture: a traditional “salty” category is not a recommendation for high sodium intake. A range of colourful foods can support variety without establishing that each colour selectively nourishes one anatomical organ. {cite('R10','WHO healthy-diet guidance')}

**Oldenlandia: what the cancer evidence actually supports.** Memorial Sloan Kettering's specialist monograph distinguishes laboratory/animal anticancer findings from a lack of human evidence sufficient to confirm safe and effective use. It also notes product-quality and substitution concerns. The lecture example illustrates traditional use and a research hypothesis, not an established cancer treatment. {cite('R11','MSK clinical herb monograph')}

**Cocklebur: historical praise does not establish safety.** Hong Kong Hospital Authority identifies the whole plant, particularly the fruit, as poisonous. This directly qualifies the historical passage on Su Shi's slide describing edibility and lack of poisoning. Preserve the passage as a record of historical belief, not as contemporary food advice. {cite('R12','Hospital Authority clinical-toxicology atlas')}

**How to evaluate a medicinal-food claim:** specify botanical identity, plant part, preparation, amount, duration, patient population and outcomes. “Used traditionally,” “active in cells,” and “improves outcomes in patients” are different evidence levels. This is a methodological synthesis of the sources above. A formula role such as chief or assistant explains intended design; it does not replace testing of the final combination.

''',
10:f'''### Additional research — historical evidence and a modern Singapore trial

**A historical correction worth retaining.** Wellcome Collection's catalogue identifies the exercise chart with **Mawangdui Tomb 3**, sealed in 168 BCE. This is more precise than associating the chart generally with the Lady Dai tomb complex, as the slide does. The source supports the chart's archaeological provenance and historical exercise context, not the efficacy of a modern reconstructed regimen. {cite('R15','Wellcome catalogue record')}

**A local Baduanjin trial.** Tou and colleagues conducted an assessor-blind randomized study at three Singapore senior activity centres. The analysis included 56 older adults; supervised Baduanjin ran for 16 weeks, two to three one-hour sessions weekly, against a wait-list/usual-activity control with monthly health education. No statistically significant overall between-group differences were found at four months. Attendance averaged 81.3%, no major adverse events were reported, and a high-attendance exploratory analysis suggested an exhaustion benefit. The appropriate conclusion is feasibility and acceptability with uncertain effectiveness on the main outcomes—not proven reversal of frailty or life extension. {cite('R13','Tou et al., 2024, randomized trial')}

**Why the exploratory result is weaker:** selecting people by attendance after randomization may select for motivation or better health. It is useful for generating hypotheses, but it is not equivalent to the main randomized comparison. This is a research-design interpretation of the reported analysis.

**How the exercise idea connects to current guidance.** WHO recommends regular activity for older adults, including 150–300 minutes of moderate aerobic activity weekly (or an equivalent vigorous combination), strengthening at least twice weekly, and varied activity emphasizing functional balance and strength on at least three days. A Baduanjin session's contribution depends on its actual intensity and content. These guidelines support attention to movement and function; they do not establish immortality or a specific lifespan from the historical texts. {cite('R14','WHO activity recommendations')}

''',
11:f'''### Additional research — identifying the study and updating hospital status

**Published study matching the lecture's description.** Zhong and colleagues' 2022 paper is explicitly a **multicentre observational study**, with 150 discharged Hong Kong patients receiving three to six months of individualized treatment. Its combination of retrospective history and prospective observation closely matches the lecture. Reported improvements are associations over follow-up; without a randomized untreated comparison, natural recovery and other influences remain alternative explanations. The study measured six-minute walk performance and the Lung Function Questionnaire, among other outcomes; those are not the same as spirometry or direct evidence of repaired lung tissue. {cite('R16','Zhong et al., 2022, primary report')}

**Use the corrected publication.** An October 2022 correction changed numerical text and a figure, including a walk-test model coefficient and an LFQ-related statement. It did not convert the study into a randomized trial. This is a useful example of why checking the actual paper and its correction is preferable to relying on automatic captions. {cite('R17','Published correction')}

**Current hospital status, checked 4 November 2026.** The lecture speaks of a future hospital opening. An October 2026 government update confirms that phased services began on **11 December 2025**, initially emphasizing outpatient and day-patient services. {cite('R18','Hong Kong Government October 2026 update')}

The announced next phase is **24-hour inpatient services from 11 December 2026**, which is still in the future at this check date. The August 2026 plan describes staged expansion rather than immediate use of the full planned 400-bed capacity. Keep the recorded plan, the services already operating and the announced future phase separate in an exam or report. {cite('R19','Official August 2026 expansion plan')}

**Connection to integration:** the study's combination of TCM pattern records and functional/quality-of-life measurements illustrates how systems can share research outcomes. Agreement on what to measure makes collaboration more interpretable; causal effectiveness still depends on an appropriate study design.

'''
}

for num,block in research.items():
    marker=f'### Lecture {num} revision checks'
    assert text.count(marker)==1, marker
    text=text.replace(marker,block+marker)

old='The captions call the work “randomized” at one point but also describe observational components without clearly stating a comparator or randomization method. **The study design therefore cannot be established confidently from this caption track.** Do not cite it as a confirmed randomized trial based on these notes.'
new='The captions call the work “randomized” at one point, but the matching published report is explicitly observational. **External research resolves the caption ambiguity: treat the matching 150-person cohort as observational, not as a confirmed randomized trial.** See the additional-research section below for the primary paper and its correction.'
assert old in text
text=text.replace(old,new)
text=text.replace('Measures include symptom questionnaires, TCM patterns/constitution and objective lung function.', 'The lecture describes symptom, TCM-pattern/constitution and lung-function-related assessments. The matching paper clarifies that the latter include six-minute walk performance and the Lung Function Questionnaire; these should not be labelled automatically as spirometry.')
text=text.replace('**TCM diagnostic associations', '**TCM diagnostic associations')
text=text.replace('## Coverage and how to use these notes\n', '## Coverage and how to use these notes\n\n**Research-enriched edition, checked 4 November 2026.** Text recognition was run on all 56 saved slide screenshots in English and Simplified Chinese. The checked, condensed extraction is available in [Slide_Text_Extraction.md](Slide_Text_Extraction.md); it paraphrases slide text and flags image-only material. Sections headed **Additional research** are external additions, not claims about what the lecturer said. Sources include primary studies, WHO/NIH guidance, professional regulators and specialist clinical references; [Research_Sources.md](Research_Sources.md) lists their types and links.\n')
text+='\n## Research references\n\nResearch additions were checked on 4 November 2026. Links are placed beside the relevant claims above; this list provides the bibliographic details and evidence types. Institutional guidance and clinical summaries are distinguished from original studies. This is a focused source check, not a systematic review.\n\n'
for k,(title,url,kind) in sources.items():
    text+=f'- **{k}.** [{title}]({url}). **Type:** {kind}.\n'
path.write_text(text,encoding='utf-8')

catalog=['# Research source register','', 'Checked 4 November 2026. Focused additions to the lecture notes; not an exhaustive or systematic review. Primary studies are used for specific research results; official and specialist references are used for guidance, classification, toxicology and current institutional facts.','']
for k,(title,url,kind) in sources.items(): catalog += [f'## {k}', '', f'[{title}]({url})', '', f'Evidence type: {kind}.', '']
(root/'Research_Sources.md').write_text('\n'.join(catalog),encoding='utf-8')

# Condensed, checked extraction: this is edited study text, not a verbatim reproduction.
# English and Chinese OCR outputs remain working evidence and are not treated as authoritative.
facts={
'L6-01-title':'Dr Chua Hui Zi; PhD in TCM internal medicine, biomedical-sciences honours degree, registered Singapore TCM practitioner.',
'L6-02-journey':'Training path shown: NTU TCM/biomedical-sciences double degree, Singapore practice, then postgraduate TCM study.',
'L6-03-comparison':'The slide compares the TCM physician with a gardener and the Western-medicine physician with a mechanic.',
'L6-04-seasons':'Seasonal imagery: spring sprouting, summer maturation, ripening/transformation, autumn harvesting, winter storage/composting; yin–yang links these phases.',
'L6-05-biomedicine':'Western medicine is illustrated through the body-as-machine analogy.',
'L6-06-integrated-hospitals':'Examples: Dongfang Hospital at Beijing University of Chinese Medicine and Tianjin University of TCM’s First Affiliated Teaching Hospital. Most content is photographic.',
'L6-07-hospitals':'Photographs identify an emergency unit, radiographic-film printing facility and 治未病 preventive-treatment centre.',
'L6-08-training':'Teaching aids include an electronic pulse machine and tongue photographs.',
'L6-09-outpatients':'Outpatient specialties include cardiology, neurology, nephrology, endocrinology, rheumatology and immunology; acupuncture is highlighted.',
'L6-10-case-record':'Record components: main symptoms, present/past/personal/family history, tongue colour/coating, pulse, blood pressure, kidney profile, glucose and CT brain imaging. Handwritten patient data are not reconstructed.',
'L6-11-formulas':'The prescription example emphasizes multiple herbs/compounds in selected proportions and doses. Individual handwritten ingredients remain uncertain.',
'L6-12-inpatients':'Daily rounds by physician/interns; vital checks, lung listening and symptom inquiry; weekly senior rounds and specialized acupuncture services.',
'L6-13-singapore':'Five settings: charitable organizations, private independent clinics, chains/enterprises, TCM departments in private hospitals and acupuncture departments in public hospitals.',
'L6-14-education':'The slide contrasts Singapore degree/college routes with Chinese undergraduate and internship routes. It lists the NTU–BUCM arrangement and the newer local four-year degree. Treat detailed route lengths as recorded-slide information.',
'L6-15-registration':'Singapore STRE and its move toward clinical competency are compared with China’s examination covering TCM and Western knowledge/practical skills. External R3 updates the timeline.',
'L6-16-science':'Tu Youyou, the 2015 Nobel Prize and artemisinin from qinghao provide the scientific-contribution example.',
'L6-17-artemisinin':'Embedded news frame on artemisinin and modern research. A full account of the clip cannot be extracted from one image.',
'L6-18-nobel':'Embedded interview frame identifies Yao Naili. Most content requires the clip’s audio, not OCR.',
'L6-19-who':'Slide reports ICD-11 adoption in 2019 and implementation in 2022, and lists 150 traditional-medicine disorders and 196 pattern categories. These counts are the slide’s figures, not a newly checked inventory.',
'L6-20-who-covid':'A WHO report dated 31 March 2022 concerns an expert meeting evaluating TCM in COVID-19 treatment; the overview gives meeting dates of 28 February–2 March 2022.',
'L6-21-prevention':'A cited October 2022 Healthier SG speech connects prevention with early management of risk factors and disease.',
'L6-22-forum':'Forum photographs show a presentation about standardized outcomes/core outcome sets in TCM studies of chronic heart failure.',
'L9-01-title':'Food therapy and harmony with nature. The original slide carries GEH1070.',
'L9-02-ancient':'Two premises: 药食同源, the shared origin of food and medicine, and harmony with nature.',
'L9-03-homology':'The slide attributes a food/medicine distinction based on hunger versus illness to the Inner Canon. This is a recorded attribution, not a verified quotation.',
'L9-04-hippocrates':'Historical Western comparison: Hippocrates, natural explanations of disease, and a diet/medicine quotation attributed to him.',
'L9-05-galen':'Galen provides a comparison using hot/cold/wet/dry qualities and Greek elements.',
'L9-06-properties':'Food classification uses nature, taste and colour. Five tastes listed: sweet, sour, bitter, salty and spicy.',
'L9-07-constitution':'A hot/excess-yang presentation is matched with cooling-classified foods; a cold/excess-yin presentation with warming-classified foods. Examples and symptom lists appear in the main notes.',
'L9-08-nature':'Colour correspondences: white–Metal–Lung/Large Intestine; dark–Water–Kidney/Bladder; green–Wood–Liver/Gallbladder; red–Fire–Heart/Small Intestine; yellow–Earth–Spleen/Stomach.',
'L9-09-elements':'Taste correspondences: sweet–Earth, spicy–Metal, salty–Water, sour–Wood, bitter–Fire, with the associated organ pairs.',
'L9-10-taste-effects':'Traditional actions: sweet nourishes/moderates; sour restrains losses; bitter clears heat/dries dampness; salty softens accumulations; spicy disperses/moves. The printed phrase “nourish flood” is anomalous and is not silently turned into a verified claim.',
'L9-11-harmony':'Harmony Rules, by Gary Butt and Frena Bloomfield, adapts Chinese balance concepts into dietary plans for another cultural setting.',
'L9-12-oldenlandia':'白花蛇舌草/Oldenlandia is presented as cooling and diuretic, with traditional heat/toxin-related uses. Cancer mentions are source claims; R11 qualifies their evidence.',
'L9-13-su-shi':'A Su Shi/Su Shen Liangfang passage praises cocklebur’s accessibility and alleged health effects. R12 supplies the modern toxicity qualification.',
'L9-14-longevity':'药膳 yaoshan combines food and medicinal ingredients; the slide emphasizes palatability and current syndrome/pattern.',
'L9-15-tea':'Tea example: rose, jasmine and red dates in hot water. The proposed complexion effect is explained through qi/blood flow and skin nourishment.',
'L9-16-hong-hai':'Job’s tears, green beans and dried tangerine peel illustrate a heat–dampness recipe. Ingredient roles differ, and the slide cautions against its use in a weak Spleen/Stomach presentation.',
'L9-17-herbal-treatment':'君臣佐使: chief ingredient, supporting minister, assistant to reduce unwanted effects, and envoy/helper for the overall formulation.',
'L9-18-summary':'Concluding themes: food and medicine overlap; tastes have attributed effects; traditions vary over time/place and influenced Japanese and Korean writings.',
'L10-01-title':'Chinese ideas of health preservation and ageing; original slide code GEH1070.',
'L10-02-sheng':'养 means cultivate/preserve/nourish; 生 concerns life/health. Goals include health maintenance, prevention and longevity within a human–nature worldview.',
'L10-03-yangsheng':'Cultivation dimensions: 养身 body, 养心 mind, 养性 character, 养神 spirit. Another framework is 精 essence, 气 breath/qi and 神 spirit.',
'L10-04-mind':'The seven emotions on this slide are joy, anger, sorrow, fear, love, hate and desire. Excess, prolonged immersion or sudden shock is distinguished from ordinary emotion.',
'L10-05-ji-kang':'Ji Kang (220–265 CE) illustrates historical claims that cultivation and guiding qi can produce exceptional longevity. These are historical aspirations, not established lifespan effects.',
'L10-06-daoyin':'导引 combines guiding qi and stretching; the slide emphasizes awareness, controlled breathing and slow movement, and calls it a forerunner of qigong.',
'L10-07-daoyin-chart':'Mawangdui archaeology is used to establish a long history of health-cultivation exercises; the chart is associated with 168 BCE. R15 refines the provenance to Tomb 3.',
'L10-08-mawangdui':'A chart shows many exercise postures and links to a demonstration. The image supplies visual historical evidence, not complete movement instructions.',
'L10-09-ageing':'Ageing is framed through internal/external harmony and everyday attention to seasons, diet, rest, massage, exercise and disciplined living.',
'L10-10-laolao':'Cao Tingdong (1699–1785), Lao Lao Heng Yan/Lasting Advice on Growing Old; the slide says he wrote the elderly-healthcare work at 75.',
'L10-11-discourses':'遵生八笺, Eight Discourses on Respecting Life (1591): Ming health writing spans medical, Daoist, Confucian, elite and household contexts.',
'L10-12-hu-wenhuan':'胡文焕, 保生心鉴/Heart Mirror for Preserving Life: an illustrated seated exercise links posture, the ears, breathing/body actions and historical therapeutic claims.',
'L10-13-baosheng':'A second illustrated practice is associated historically with rheumatism-related swelling/pain. It combines hands, posture, attention and breathing.',
'L10-14-baduanjin':'八段锦: eight brocade/silken movements; the slide describes multiple historical origin attributions rather than a single verified creator.',
'L10-15-demonstration':'Eight labels: hold up heavens; draw bow; separate heaven/earth; gaze backward; clench fists/glare; hold feet; sway head/shake tail; bounce on toes. This preserves the slide’s order.',
'L10-16-summary':'The conclusion joins balance, careful eating, disciplined lifestyle and self-maintained exercise as the lecture’s health-preservation approach.',
}
images=sorted((root/'slides').glob('*.jpg'))
assert set(facts)=={p.stem for p in images}
parts=['# Checked slide-text extraction — Lectures 6, 9 and 10','',
'This is a condensed, edited extraction of the text-bearing content in all 56 saved screenshots. It paraphrases the slides into readable study text; it is not a verbatim transcript. English and Simplified Chinese OCR were cross-checked against the earlier visual inspection. Photographs, illegible handwriting and video-only content are identified rather than invented. External research belongs to the main notes, not to this extraction.','',
'[Open the research-enriched notes](GEC1044_Lectures_6-11_Study_Notes.md)','']
for lec in ['L6','L9','L10']:
    parts += [f'## Lecture {lec[1:]}','']
    for p in images:
        if p.stem.startswith(lec+'-'):
            parts += [f'### {p.stem}', '', f'[Source screenshot](slides/{p.name})', '', facts[p.stem], '']
(root/'Slide_Text_Extraction.md').write_text('\n'.join(parts),encoding='utf-8')
print('Research sources:',len(sources))
print('Checked slide extractions:',len(facts))
print('Combined note words:',len(text.split()))
