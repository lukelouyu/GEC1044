from zipfile import ZipFile
from lxml import etree
z=ZipFile('GEC1044_Tong_Keow_First_Draft.docx')
n={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
styles=etree.fromstring(z.read('word/styles.xml'))
for style in styles.findall('w:style',n):
 if style.get('{'+n['w']+'}styleId') in ('Title','Heading1','Normal'):
  print(etree.tostring(style,pretty_print=True).decode())
print(z.read('word/settings.xml').decode())
