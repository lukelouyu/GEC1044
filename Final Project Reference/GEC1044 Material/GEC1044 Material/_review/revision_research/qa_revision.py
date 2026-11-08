from pathlib import Path
import json, re
from docx import Document
from pypdf import PdfReader
import pypdfium2 as pdfium
R=Path(__file__).resolve().parents[2]
D=Document(R/'GEC1044_Tong_Keow_First_Draft.docx')
text='\n'.join([p.text for p in D.paragraphs]+[c.text for t in D.tables for r in t.rows for c in r.cells])
checks={
'presentation_eight_categories':all(s in text for s in ['Ginseng tonics','Monk-fruit products','Flower and herbal teas','Soup packs','Lingzhi supplements','Liver care and mood support','Yin Qiao-type remedies','Medicated oils']),
'presentation_five_soups':all(s in text for s in ['清补凉','党参北芪补气汤','玉竹淮山润燥汤','枸杞红枣养生汤','五指毛桃健脾汤']),
'lower_demand_preserved':all(s in text for s in ['半枝莲','Specialist herbs','Strong tonic formulas']),
'five_column_illustrated_tables': len(D.tables[0].columns)==5 and len(D.tables[1].columns)==5 and len(D.tables[4].columns)==5,
'eight_category_rows':len(D.tables[1].rows)==9,
'three_lower_demand_rows':len(D.tables[4].rows)==4,
'pictures_in_all_requested_rows':all(len(c._tc.xpath('.//a:blip'))>0 for i in [1,4] for row in D.tables[i].rows[1:] for c in row.cells[:1]),
'corrected_demographic_figures':all(s in text for s in ['228,140','57,557','165,450','4,620','1,070','23%']),
'clinical_evidence_not_fabricated':'not established' in text and 'Huoxiang Zhengqi' in text,
'evidence_labels':'This is our interpretation' in text and 'staff member' in text,
'revision_note':'Revision note' in text,
}
print(json.dumps(checks,indent=2)); assert all(checks.values())
(R/'_review/revision_research/quality_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
pdf=R/'_review/draft_render/draft.pdf'
out=R/'_review/thematic_render';out.mkdir(exist_ok=True)
pr=PdfReader(pdf); pd=pdfium.PdfDocument(pdf)
for i in range(len(pd)):
    pd[i].render(scale=1.5).to_pil().save(out/f'page-{i+1:02}.png')
    t=pr.pages[i].extract_text() or ''
    print(f'PAGE {i+1}: {len(t)} chars; '+t[:90].replace('\n',' | ')+' ... '+t[-80:].replace('\n',' | '))
print('Rendered',len(pd),'pages')
