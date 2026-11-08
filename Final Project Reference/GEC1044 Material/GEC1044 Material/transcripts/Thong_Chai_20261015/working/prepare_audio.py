import json
import subprocess
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy.signal import correlate

ROOT = Path(__file__).resolve().parent
SOURCES = {
    'obsidian': Path("C:/Users/lukel/OneDrive/Documents/Luke Obsidian/Luke's Vault/99 Attachments/Recording 20261015164725.m4a"),
    'backup': Path('C:/Users/lukel/Downloads/Singapore Thong Chai Medical Institution.m4a'),
}
report = {}
envelopes = {}
for name, src in SOURCES.items():
    meta = json.loads(subprocess.check_output(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', str(src)]))
    wav = ROOT / f'{name}.wav'
    if not wav.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-ar', '16000', '-ac', '1', str(wav)], check=True)
    sr, raw = wavfile.read(wav)
    x = raw.astype(np.float32) / 32768
    blocks = x[:len(x)//160*160].reshape(-1, 160)
    rms = np.sqrt(np.mean(blocks**2, axis=1))
    envelopes[name] = rms
    report[name] = {'source': str(src), 'duration': len(x)/sr, 'metadata': meta,
                    'pcm_rms_db': float(20*np.log10(np.sqrt(np.mean(x*x))+1e-12)),
                    'peak': float(np.max(np.abs(x))),
                    'samples_near_full_scale_fraction': float(np.mean(np.abs(x)>.999)),
                    'rms_10ms_quantiles': [float(v) for v in np.quantile(rms,[.05,.25,.5,.75,.95])]}
    print(name, json.dumps({k:v for k,v in report[name].items() if k!='metadata'}), flush=True)

# Cross-correlate short-time loudness to align two independently recorded microphones.
a, b = envelopes['obsidian'], envelopes['backup']
alignments=[]
for start in [0,600,1800,3000,4200]:
    end = min(start+120, len(b)/100)
    if end-start<20:
        continue
    anchor = np.log(b[int(start*100):int(end*100)]+1e-5)
    lo=max(0,int((start-90)*100)); hi=min(len(a),int((end+90)*100))
    search=np.log(a[lo:hi]+1e-5)
    anchor=anchor-anchor.mean()
    scores=correlate(search-search.mean(),anchor,mode='valid',method='fft')
    loc=int(np.argmax(scores))
    aligned=search[loc:loc+len(anchor)]
    lag=lo/100+loc/100-start
    coefficient=float(np.corrcoef(aligned,anchor)[0,1])
    alignments.append({'backup_start':start,'obsidian_minus_backup_seconds':lag,'envelope_correlation':coefficient})
report['alignment_samples']=alignments
(ROOT/'audio_comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('ALIGNMENT', json.dumps(alignments), flush=True)
