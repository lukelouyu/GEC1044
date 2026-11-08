from pathlib import Path
import urllib.request,json
from concurrent.futures import ThreadPoolExecutor
A=Path(__file__).parent/'appendix_images'
urls={
 'cactus.jpg':'https://www.nparks.gov.sg/-/media/ffw/migrated/round2/flora/2281/6d25d19cf9504ecf99b101a9f99f79aa.jpg',
 'roselle.jpg':'https://www.nparks.gov.sg/-/media/ffw/migrated/round2/flora/2096/54820dbe55ac4dfd88db6e874998b703.jpg',
 'five-flower-tea.jpg':'https://www.wjl.com.sg/cdn/shop/files/wjl-lung-soothing-summer-tea-01.jpg?v=1756444203',
 'fig-reference.pdf':'https://www.cmro.gov.hk/files/gcmti/research/mmi/ech_search/041_RF_vs_HGE_tc.pdf',
}
def fetch(k):
 req=urllib.request.Request(urls[k],headers={'User-Agent':'Mozilla/5.0'})
 (A/k).write_bytes(urllib.request.urlopen(req,timeout=30).read())
 return k
with ThreadPoolExecutor(max_workers=4) as p:print(list(p.map(fetch,urls)))
(A/'download_sources.json').write_text(json.dumps(urls,indent=2),encoding='utf-8')
