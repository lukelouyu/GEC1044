from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
WORK=Path(__file__).resolve().parent
old=(ROOT/'working/draft-v1/report_v1.md').read_text(encoding='utf-8')
notes=dict(re.findall(r'^\[\^(\d+)\]: (.+)$',old,re.M))
body=re.split(r'^\[\^1\]:',old,flags=re.M)[0]

def section(start,end,new):
    global body
    a=body.index(start); b=body.index(end,a)
    body=body[:a]+new.strip()+'\n\n'+body[b:]

body=body.replace('Student ID  [Add student ID]\n\n','')
body=body.replace('The activities discussed included brisk walking or gentle jogging in a park, and swimming at a suitable low or moderate intensity.','The activities discussed included park walking and swimming at an appropriate intensity. I use those options here; jogging needs a separate check because it is commonly classed as vigorous activity.')

section('### 3.1','### 3.2', '''### 3.1 A Chinese medicine perspective

The recipe needs a more specific basis than the idea that tired students need nourishing food. Lecture 7 distinguishes a symptom from a pattern, or zheng: the same complaint can occur in different combinations of signs. The four diagnostic methods establish that combination before a treatment principle is chosen.[^4] Here I use possible patterns to explain the recipe's design, rather than diagnose my earlier movement difficulties.

Fatigue together with poor appetite suggests investigating Spleen qi deficiency. Within Chinese medicine, the Spleen and Stomach receive and transform food; reduced nourishment gives a traditional explanation for linking eating poorly with low energy.[^5] Inquiry would therefore cover meal regularity, stool consistency and whether tiredness persists after rest. The practitioner would also examine the tongue and pulse. Sleep disturbance alone would not establish this digestive pattern.

If poor appetite and fatigue accompany easily interrupted sleep, palpitations and a pale complexion, the question becomes whether Heart and Spleen deficiency gives a better account. A Chinese University of Hong Kong booklet describes this combination with loose stools and a pale tongue with a thin white coating. I use its description of the pattern, which appears in a booklet for young cancer survivors, without applying that population's treatment plan to students.[^26] The Heart's association with shen, or mental and emotional activity, explains why this line of reasoning includes sleep as well as digestion.

The corresponding food therapy principle is to support the Spleen and nourishment while including ingredients traditionally used to calm shen. Yam and rice establish the digestive focus; lotus seeds connect that focus with calming shen; dates add a small nourishing component. This chain makes the ingredient choice answer the proposed pattern. The Department of Health also lists rice, yam and dates in dietary guidance for qi deficiency constitution, a broader category than a current clinical pattern.[^27]

Alternative signs change the direction. Hong Kong University's discussion links Liver fire insomnia with irritability and phlegm heat with gastric bloating, a heavy head and a bitter taste.[^6] Such a presentation needs a different assessment and principle, rather than simply more tonic ingredients. Lecture 9 makes the same point through a cooling heat-dampness soup described as unsuitable for a weak Spleen and Stomach. The present congee is therefore a focused nourishing option within the traditional framework, not a general insomnia remedy.[^15]''')

body=body.replace('Hooley, Nock and Butcher organise abnormal psychology through a biological, psychological and social approach.','Pearson\'s introduction to Hooley, Nock and Butcher\'s Abnormal Psychology describes a biological, psychological and social approach.')

anchor='The proposed batch makes two portions. All quantities below are planned kitchen weights. Fresh yam and dried ingredients are listed separately because their weights and preparation differ.'
body=body.replace(anchor,anchor+'''

The 20 g lotus seeds give 10 g of dried seeds per intended portion. This makes them a supporting ingredient alongside 100 g fresh yam, rather than the main bulk of the meal. Their traditional digestive and calming functions explain their inclusion; the exact weight is a kitchen design choice for this first version. The 15 g dates give 7.5 g per portion, half the Department of Health example's batch quantity. This keeps dates subordinate to yam and reduces the amount of dried fruit while retaining some sweetness. These food weights do not establish a therapeutic dose or a measured effect on sleep.''')

section('### 4.3','## 5', '''### 4.3 Suitability and the choices behind the combination

Lecture 9's chief, minister, assistant and envoy scheme helped me rank the ingredients. Yam anchors the main aim and lotus seeds support it while adding the traditional shen connection. Dates contribute a smaller nourishing component, and rice makes the combination a meal. A simple household recipe does not need an extra herb to fill every formula role.[^17]

This restraint follows the course's account of the Zhang Zhongjing tradition: the patient's presentation guides formula selection.[^18] Adding ginseng or several more tonics would need a further reason. The proposed combination already addresses its chosen direction, and more ingredients would add cost and preparation without resolving a new finding.

The intended benefit is a tolerable, nourishing meal whose selection is explained through Chinese food therapy. Traditional functions such as calming shen supply that rationale; they are not clinical results from testing this congee. It is intended as food and does not replace individual assessment or treatment for persistent sleep problems, fatigue or appetite loss. Personal allergies, prescribed diets and ongoing medication should be discussed with the treating clinician before using it regularly.''')

section('## 5','## 6', '''## 5 Home preparation and practical evaluation

For this recipe, use a saucepan with a lid, a kitchen scale and a measuring jug. Weigh the edible portions listed above. Rinse the lotus seeds and follow the packet's soaking instructions, checking that the green embryos have been removed. Wash the rice. Peel the yam with gloves if its sap irritates the skin, then cut it into small pieces. Wash and pit the dates.

Place the rice, lotus seeds and 1,000 ml water in the saucepan. Bring to the boil, then reduce the heat to a gentle simmer. Add the yam and dates and cook until the rice breaks down and the lotus seeds are tender. Stir occasionally and add water if needed. Allow about 45 to 60 minutes of cooking, in addition to ingredient preparation and any soaking. Tenderness is the final check. Divide into two portions and serve warm.

A one-pot method reduces equipment and washing up, but an hour of cooking still requires planning. This is more realistic for a planned evening or weekend meal than for a rushed morning. Preparing two portions together can spread that work across two meals, or allow two people to share the batch. If saving a portion, cool it quickly, ideally within one hour, refrigerate, and use within 24 hours; reheat only once until steaming hot throughout, following Food Standards Agency advice for cooked rice.[^28]

This version has not yet been cooked. The practical evaluation needs to establish whether the stated water quantity, cooking time and two-portion yield work. A useful record will compare the planned and actual weights, active preparation time, simmering time, cost per portion and final texture. Photographs taken during weighing, ingredient preparation, simmering and serving will document that process. Taste and ease of eating will determine whether the design is worth repeating.''')

section('## 6','## 7', '''## 6 Acupuncture and individualized care

Lecture 8 explains acupuncture through regulating qi, blood and yin and yang, with point selection and technique guided by the person's presentation.[^19] Its relevance here is the shared principle of individualized care: neither an acupuncture point nor a food ingredient should be selected from a symptom label alone.

My Thong Chai photograph records a teaching slide about needling sensations and precautions (Figure 3). Explaining what to expect gives a patient a clearer basis for asking questions and reporting discomfort. Psychologically, this makes communication and participation part of the care experience.

[[PHOTO acupuncture]]

Figure 3  Patient sensations and precautions discussed in the Thong Chai acupuncture session. Photograph by the author.[^20]

My earlier loss of mobility makes that attention to the individual meaningful to me. It motivates the project without establishing the congee's effects. The link with food therapy is a way of reasoning about care, not evidence that the two interventions produce the same outcome.''')

section('## 7','## 8', '''## 7 Exercise and everyday food therapy

My doctor advised exercise while avoiding strenuous activity and gym training. Park walking and suitable swimming provide practical options within that advice. Although gentle jogging was also discussed, I leave it out of the present routine until its intensity has been clarified with my doctor. The CDC classifies jogging as vigorous and distinguishes recreational swimming from continuous lap swimming, so the activity's name alone does not establish a suitable intensity.[^23]

Lecture 10 places movement, food, rest and emotional cultivation within yangsheng, or nourishing life.[^24] For this project, that means planning the congee as part of regular meals, allowing preparation to fit my available energy, and choosing movement that leaves room for the rest of the day. Psychology helps explain the value of achievable tasks: preparing a meal or completing a suitable walk gives a concrete opportunity to participate and notice progress.

I also prefer warm water as a comfortable way to drink regularly. NHS guidance supports adjusting fluid intake to circumstances such as hot weather and activity.[^25] Warm water belongs to the routine as hydration; it is not a treatment claim for psychological or movement problems.''')

section('## 8','## 9', '''## 8 Reflection and conclusion

The recipe's strongest feature is the connection between the concerns, the proposed pattern and the ingredient roles. A possible Spleen deficiency direction explains the emphasis on yam and rice. The Heart-Spleen question explains why lotus seeds and a small quantity of dates belong in the combination. Comparing this direction with heat-related sleep disturbance shows why the same recipe should not be recommended simply because someone sleeps badly.

The main practical trade-off is time. Familiar ingredients and one saucepan make the recipe straightforward, but soaking and simmering may still be demanding for a fatigued student. Planned preparation and two portions address that problem in the design; the cooking record must show whether they work in practice. A successful first trial would produce tender seeds and yam, an acceptable texture and sweetness, and a portion that is easy to eat at a reasonable cost. These are concrete food outcomes. Changes in a clinical condition require a different kind of evaluation.

Regaining mobility made ordinary daily activities matter more to me. GEC1044 helps me turn that concern into a food choice with a clear rationale. Psychology adds questions about habits, coping and participation. Together, they make this a focused project about preparing a suitable meal within everyday care.''')

notes['7']='Pearson, “Abnormal Psychology, Global Edition,” 18th ed., “Title overview,” paragraph describing the biopsychosocial approach, accessed November 6, 2026, https://www.pearson.com/en-nz/subject-catalog/p/abnormal-psychology-global-edition/P200000003860?view=educator. The textbook is Jill M. Hooley, Matthew K. Nock, and James N. Butcher, Abnormal Psychology, 18th global ed. (Harlow, England: Pearson, 2021).'
notes['15']='GEC1044, Lecture 9, 7:03, 38:51 and 44:57.'
notes['18']='GEC1044, Lecture 3, section on formula medicine and the tradition attributed to Zhang Ji or Zhang Zhongjing.'
notes['26']='Chinese University of Hong Kong, School of Chinese Medicine et al., 中醫藥與青少年和青年癌症康復者小冊子, series 1, 睡眠困難, 9, accessed November 6, 2026, https://scm.cuhk.edu.hk/images/2024/7-6/_01-Booklet__.pdf. Used here for its description of the Heart-Spleen deficiency pattern.'
notes['27']='Hong Kong Department of Health, Chinese Medicine Regulatory Office, “中醫體質分類與養生,” “氣虛體質,” accessed November 6, 2026, https://www.cmro.gov.hk/html/b5/useful_information/public_health/exhibit_boards/Body_Constitution_and_Relevant_Health_Maintenance.html.'
notes['28']='Food Standards Agency, “Home Food Fact Checker,” section on rice, accessed November 6, 2026, https://www.gov.uk/government/publications/home-food-fact-checker/home-food-fact-checker.'
section('## 2','## 3', '''## 2 My experience and everyday care

Losing mobility affected my independence: going out and starting ordinary activities became difficult. Being able to walk again restored a practical part of daily life. My doctor advised exercise while avoiding strenuous activity and gym training. I carry forward park walking and suitable swimming here; the jogging mentioned in our discussion needs clarification about intensity.

That experience made manageable care important to me. A student may value regular meals but struggle with appetite, preparation or an irregular schedule. I chose a familiar one-pot meal with that difficulty in mind.

My photograph of a pulse diagnosis slide at Thong Chai connects this concern with Lecture 7's emphasis on combining observations and history (Figure 1).[^2] A single symptom starts an inquiry; the whole presentation guides the response.

[[PHOTO pulse]]

Figure 1  Pulse positions explained during the Thong Chai teaching session. Photograph by the author.[^3]''')
section('### 3.2','## 4', '''### 3.2 A psychological perspective

Pearson's introduction to Hooley, Nock and Butcher's Abnormal Psychology describes a biological, psychological and social approach.[^7] This helps me consider feelings alongside physical ability and access to activities and people. My movement difficulties changed all three aspects of daily life.

The PL1101E textbook explains how appraisal shapes a stress response and how rumination can interfere with problem solving.[^8] These ideas help frame a possible student cycle: worry disrupts rest, fatigue makes work feel harder, and unfinished work creates further worry. They do not establish a psychological cause for my earlier physical symptoms.

Behavioural approaches suggest starting with achievable activities that offer enjoyment or a sense of progress.[^9] Preparing a meal gives this idea a practical form. Chinese medical concepts explain the recipe selection; psychology helps examine whether preparation fits a person's energy and supports participation in daily routines.''')
section('### 4.2','### 4.3', '''### 4.2 Why these ingredients belong together

Chinese yam, or shan yao, anchors the digestive aim. The Polytechnic University describes dried yam rhizome as sweet and neutral, associated with the Spleen, Lung and Kidney, and traditionally used to support the Spleen and Stomach. This recipe uses fresh yam, following the Department of Health's congee preparation.[^11] Soft cooked yam also makes the meal more substantial than a herbal drink.

Lotus seed, or lian zi, connects digestive support with calming shen. Its sweet, astringent and neutral description and affinities to the Spleen, Kidney and Heart explain its supporting role.[^12] I specify dried shelled seeds with the green embryo removed, distinguishing the ingredient from lotus plumule.

Red dates, or da zao, contribute sweetness and traditional nourishment. Their listed functions include supplementing middle qi and nourishing blood and calming shen; they are sweet and warm, associated with the Spleen and Stomach.[^13] The smaller quantity keeps this supporting role clear. No extra sugar is included.

Rice supplies the starch that thickens the congee and gives it a familiar meal base. Lecture 9 also includes rice among sweet foods associated with nourishment.[^14] Its kitchen function therefore supports the same overall choice.

[[TABLE properties]]

My Thong Chai photograph shows the framework applied here (Figure 2): nature, flavour, meridian affinity and function are separate questions about each ingredient.[^15]

[[PHOTO properties]]

Figure 2  A teaching slide on the properties of herbs at Thong Chai. Photograph by the author.[^16]''')
# Number true footnotes by first occurrence, including repeated references as new notes.
newnotes=[]
def ref(match):
    newnotes.append(notes[match.group(1)])
    return '[^'+str(len(newnotes))+']'
body=re.sub(r'\[\^(\d+)\]',ref,body)
newtext=body.rstrip()+'\n\n'+'\n'.join(f'[^{i}]: {t}' for i,t in enumerate(newnotes,1))+'\n'
(WORK/'report_v2.md').write_text(newtext,encoding='utf-8')

builder=(ROOT/'working/draft-v1/build_report.py').read_text(encoding='utf-8')
builder=builder.replace("'Final_Report_V1.docx'","'Final_Report_V2.docx'").replace("'report_v1.md'","'report_v2.md'")
builder=builder.replace("['Final Project','Student Name  Lou Yu','Student ID  [Add student ID]']","['Final Project','Student Name  Lou Yu']")
builder=builder.replace("==25","==len(notes)")
start=builder.index('BIBLIOGRAPHY = ['); end=builder.index('\nITALICS = [',start)
namespace={}
exec(builder[start:end],namespace)
bib=namespace['BIBLIOGRAPHY']
bib=[t for t in bib if not t.startswith(('Chinese University of Hong Kong, School of Chinese Medicine.','MacPherson,','Hooley,','National University of Singapore. GEC1044 Chinese Medicine:'))]
bib += [
 'Chinese University of Hong Kong, School of Chinese Medicine et al. 中醫藥與青少年和青年癌症康復者小冊子. Series 1, 睡眠困難. Accessed November 6, 2026. https://scm.cuhk.edu.hk/images/2024/7-6/_01-Booklet__.pdf.',
 'Food Standards Agency. “Home Food Fact Checker.” Section on rice. Accessed November 6, 2026. https://www.gov.uk/government/publications/home-food-fact-checker/home-food-fact-checker.',
 'Hong Kong Department of Health, Chinese Medicine Regulatory Office. “中醫體質分類與養生.” Accessed November 6, 2026. https://www.cmro.gov.hk/html/b5/useful_information/public_health/exhibit_boards/Body_Constitution_and_Relevant_Health_Maintenance.html.',
]
titles={2:'Natural Philosophy Organs and Meridians',3:'Formula Medicine and Classical Theory',7:'The Art and Science of TCM Diagnostics',8:'Acupuncture Theory and Practice',9:'Food Therapy Living in Harmony with Nature',10:'Chinese Ideas of Health Preservation and Ageing'}
for i,title in titles.items():
    bib.append(f'National University of Singapore. GEC1044. Lecture {i}, “{title}.” Course teaching materials, AY2026/27 Semester 1.' if i!=3 else 'National University of Singapore. GEC1044. Lecture 3. Section on formula medicine and classical theory. Course teaching notes, AY2026/27 Semester 1.')
bib=[t.replace('Title overview.','“Title overview,” paragraph on the biopsychosocial approach.') for t in bib]
bib.sort(key=str.casefold)
builder=builder[:start]+'BIBLIOGRAPHY = '+repr(bib)+'\n'+builder[end:]
builder=builder.replace("'Cooking and tasting record','Clinical chronology'","'Cooking and tasting record'")
builder=builder.replace("p.paragraph_format.space_after=Pt(8)\n                p.paragraph_format.line_spacing=1.0", "p.paragraph_format.space_after=Pt(4)\n                p.paragraph_format.line_spacing=1.0")
(WORK/'build_report.py').write_text(builder,encoding='utf-8')
print('Prepared V2 source with',len(newnotes),'footnotes')
