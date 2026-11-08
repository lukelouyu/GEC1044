from pathlib import Path
import json
import time
import torch
import whisper

torch.set_num_threads(4)
root=Path(__file__).resolve().parent
model=whisper.load_model('tiny')
source=whisper.load_audio(str(root/'obsidian.wav'))
out={}
began=time.time()
for label,start,end in [('opening',0,50),('ending',4390,4442)]:
    r=model.transcribe(source[start*16000:end*16000],language='en',fp16=False,verbose=False,temperature=0,beam_size=1,best_of=1)
    out[label]=r
    print(label,json.dumps(r['text'],ensure_ascii=True),flush=True)
(root/'boundary_check_tiny.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('SECONDS',round(time.time()-began),flush=True)
