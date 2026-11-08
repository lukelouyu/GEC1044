from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph
from pathlib import Path
root=Path.cwd()
d=Document(root/'GEC1044_Tong_Keow_Clean_Read.docx')
anchor=next(p for p in d.paragraphs if p.text.startswith('4.3'))
def para():
 e=OxmlElement('w:p');anchor._p.addprevious(e);return Paragraph(e,anchor._parent)
def caption(t):
 p=para();p.style=d.styles['Caption'];p.paragraph_format.space_after=Pt(8)
 p.paragraph_format.keep_together=True; p.paragraph_format.keep_with_next=False
 r=p.add_run(t);r.font.size=Pt(10)
 return p
p=para();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.keep_with_next=True
paths=[r'C:\Users\lukel\AppData\Local\Temp\codex-clipboard-ba6fb0dc-3108-4248-af09-aef5c6327136.png',r'C:\Users\lukel\AppData\Local\Temp\codex-clipboard-33fc1aa7-17fd-4d32-b6ba-b397a85f99fc.png',r'C:\Users\lukel\AppData\Local\Temp\codex-clipboard-2c08b1ca-4c9e-4811-ac37-0455473157f8.png']
p.add_run().add_picture(paths[0],height=Inches(2.35));p.add_run('   ');p.add_run().add_picture(paths[1],height=Inches(2.35))
caption('Figure 4.2a. Heng Foh Tong herbal-drink vending machine. Bottled drinks and self-service purchasing illustrate how herbal products can be presented in a convenient retail format, linking the industry example to Tong Keow\u2019s emphasis on easier preparation and use.')
caption('Figure 4.2b. Amacha branded takeaway drinks. The shop setting and takeaway cups illustrate a contemporary beverage format for the TCM-inspired teas discussed above, showing how traditional ingredients can be marketed through familiar consumer routines.')
p=para();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.keep_with_next=True
p.add_run().add_picture(paths[2],width=Inches(3.8))
caption('Figure 4.2c. Herbal retailing with a traditional balance scale and visible ingredient jars. The photograph illustrates the weighing and display of raw herbs, providing a visual comparison with bottled and takeaway drinks. Making ingredients visible can help customers see what is available, as discussed in the Teck Soon example.')
for s,desc in zip(list(d.inline_shapes)[-3:],['Heng Foh Tong herbal-drink vending machine','Amacha takeaway drinks in front of its shop','Herbal retailer weighing raw herbs with a balance scale']):
 s._inline.docPr.set('descr',desc)
out=root/'GEC1044_Tong_Keow_With_Section_4_2_Pictures.docx';d.save(out)
print(out)


