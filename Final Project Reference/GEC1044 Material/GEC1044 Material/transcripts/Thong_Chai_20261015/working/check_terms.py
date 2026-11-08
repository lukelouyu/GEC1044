import os
import sys
import time
import wave
import json
from dataclasses import asdict
from pathlib import Path

root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'python_packages'))
import numpy as np
from faster_whisper import WhisperModel

start=840
end=880
with wave.open(str(root/'backup.wav'),'rb') as wav:
    wav.setpos(start*16000)
    audio=np.frombuffer(wav.readframes((end-start)*16000),dtype='<i2').astype(np.float32)/32768
model=WhisperModel(str(root/'model_large_v3_turbo'),device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
print('LOADED',flush=True)
began=time.time()
segments,info=model.transcribe(audio,language='en',beam_size=5,temperature=0,
    initial_prompt='TCM teaching session. Tongue diagnosis. Pulse diagnosis. Cun, guan, chi. Qi and blood. Yin and yang. Spleen, kidney, liver, heart, lung. Floating pulse, deep pulse, wiry pulse, slippery pulse. Radial artery. Styloid process of the radius.',
    condition_on_previous_text=True)
records=[]
for s in segments:
    r=asdict(s)
    r['start']+=start;r['end']+=start
    records.append(r)
    print(r['start'],r['end'],r['text'],flush=True)
(root/'terminology_check.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print('SECONDS',round(time.time()-began),flush=True)
