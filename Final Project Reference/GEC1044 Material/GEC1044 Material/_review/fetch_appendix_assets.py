from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,re,json

A=Path(__file__).parent/'appendix_images'
A.mkdir(exist_ok=True)
urls={
 'roselle':'https://www.nparks.gov.sg/florafaunaweb/flora/2/0/2096',
 'cactus':'https://www.nparks.gov.sg/florafaunaweb/flora/2/2/2281',
 'fig':'https://www.cmro.gov.hk/html/b5/useful_information/public_health/publication/Interesting_Chinese_Herbs.html',
 'tea':'https://www.wjl.com.sg/products/wing-joo-loong-lung-soothing-summer-tea',
}
def fetch(k):
 try:
  req=urllib.request.Request(urls[k],headers={'User-Agent':'Mozilla/5.0'})
  raw=urllib.request.urlopen(req,timeout=30).read()
  (A/(k+'.html')).write_bytes(raw)
  tx=raw.decode('utf-8')
  return k,re.findall(r'<img[^>]+>',tx)[:40]
 except Exception as e:return k,str(e)
with ThreadPoolExecutor(max_workers=4) as pool:
 for result in pool.map(fetch,urls):print(result)
