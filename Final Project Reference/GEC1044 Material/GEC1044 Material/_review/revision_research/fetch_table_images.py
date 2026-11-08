from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request, re, json
from urllib.parse import urljoin
R=Path(__file__).parent
A=R/'table_images'; A.mkdir(exist_ok=True)
urls={k:'https://herbaltcm.sn.polyu.edu.hk/herbal/'+k for k in ['barbated-skullcup-herb','chrysanthemum-flower','glossy-ganoderma','japanese-honeysuckle-flower']}
urls['red-flower-oil']='https://feifah.com/zh/products/red-flower-ointment-50ml'
def fetch(k):
    url=urls[k]; t=urllib.request.urlopen(url,timeout=30).read().decode('utf-8')
    (A/(k+'.html')).write_text(t,encoding='utf-8')
    if 'polyu' in url:
        ims=re.findall(r'<img[^>]+src="([^"]+/417p278/[^"]+)"',t)
        imurl=ims[0]
    else:
        imurl=re.search(r'<meta[^>]*property="og:image"[^>]*content="([^"]+)"',t)[1]
        imurl=imurl.replace('&amp;','&')
    f=A/(k+'.jpg'); f.write_bytes(urllib.request.urlopen(imurl,timeout=30).read())
    return k, {'page':url,'image':imurl,'local':str(f)}
with ThreadPoolExecutor(max_workers=5) as p: result=dict(p.map(fetch,urls))
(A/'sources.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(result)
