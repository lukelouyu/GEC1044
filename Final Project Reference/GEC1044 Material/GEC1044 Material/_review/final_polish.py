from pathlib import Path
import hashlib, json
from docx import Document

root = Path(__file__).resolve().parents[1]
source = root / 'GEC1044_Tong_Keow_Argument_Revision_v2.docx'
output = root / 'GEC1044_Tong_Keow_Final_Polish.docx'
doc = Document(source)
old = 'Together, these accounts suggest that understanding and preparation matter to a product’s place on the shelf.'
new = 'We interpret these accounts as linking a product’s place on the shelf to the explanation and preparation it requires. This helps explain the appeal of prepared packs, which make selection and portioning part of the shop’s service.'
matches = [p for p in doc.paragraphs if old in p.text]
assert len(matches) == 1
p = matches[0]
runs = [r for r in p.runs if old in r.text]
assert len(runs) == 1
runs[0].text = runs[0].text.replace(old, new)
doc.save(output)

original = Document(source)
check = Document(output)
assert len(original.paragraphs) == len(check.paragraphs)
changed = [i for i,(a,b) in enumerate(zip(original.paragraphs,check.paragraphs)) if a.text != b.text]
assert len(changed) == 1
assert [t._tbl.xml for t in check.tables] == [t._tbl.xml for t in original.tables]
pics = lambda d: [hashlib.sha256(s._inline.xml.encode()).hexdigest() for s in d.inline_shapes]
assert pics(check) == pics(original)
text = '\n'.join(p.text for p in check.paragraphs)
for wrong in ['辩论论治', 'known as 证论治', 'publications accounts', 'buys can']:
    assert wrong not in text
for correct in ['辨证论治', 'public-relations accounts', 'buyers can']:
    assert correct in text
result = {'output': str(output), 'changed_paragraphs': changed,
          'pictures_preserved': len(check.inline_shapes), 'tables_unchanged': True,
          'three_reported_typos_already_correct_in_source': True}
(root / '_review/final_polish_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))
