from pathlib import Path
import urllib.request, re, html, json, zipfile
from pypdf import PdfReader
from lxml import etree
R=Path(__file__).parent
u='https://www.singstat.gov.sg/find-data/explore-data-themes/population/geographic-distribution/latest-news-data'
t=urllib.request.urlopen(u).read().decode()
links=[html.unescape(x) for x in re.findall(r'href="([^"]+)"',t) if '2025' in x or '2024' in x]
(R/'singstat_links.txt').write_text('\n'.join(links),encoding='utf-8')
print('\n'.join(links))
pdf=PdfReader(r'C:\Users\lukel\Downloads\Traditional Chinese Medicine in Singapore Fieldwork Findings (1).pdf')
(R/'group_presentation.txt').write_text('\n\n'.join(f'PAGE {i+1}\n'+(p.extract_text() or '') for i,p in enumerate(pdf.pages)),encoding='utf-8')
print('PRESENTATION PAGES',len(pdf.pages))
with zipfile.ZipFile(r'C:\Users\lukel\Downloads\Group 43 Assignment Slides-1 (1).pptx') as z:
    slides=sorted([n for n in z.namelist() if re.match(r'ppt/slides/slide\d+.xml$',n)],key=lambda n:int(re.search(r'slide(\d+)',n)[1]))
    texts=['SLIDE '+str(i+1)+'\n'+'\n'.join(etree.fromstring(z.read(n)).xpath('//a:t/text()',namespaces={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'})) for i,n in enumerate(slides)]
    (R/'group43_slides.txt').write_text('\n\n'.join(texts),encoding='utf-8')
    print('OTHER PPT',texts[0][:250])
