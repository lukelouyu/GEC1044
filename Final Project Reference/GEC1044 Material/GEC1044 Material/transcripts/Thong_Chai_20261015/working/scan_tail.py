import json
import time
import wave
from pathlib import Path
import numpy as np
import torch
import whisper

torch.set_num_threads(4)
root=Path(__file__).resolve().parent
model=whisper.load_model('tiny')
records=[]
began=time.time()
with wave.open(str(root/'obsidian.wav'),'rb') as wav:
    duration=wav.getnframes()/16000
    for start in range(1800,int(duration),300):
        wav.setpos(start*16000)
        audio=np.frombuffer(wav.readframes(300*16000),dtype='<i2').astype(np.float32)/32768
        result=model.transcribe(audio,language='en',fp16=False,temperature=0,beam_size=1,best_of=1,
            condition_on_previous_text=False,no_speech_threshold=.5,logprob_threshold=-.7,verbose=None)
        for s in result['segments']:
            s['start']+=start;s['end']+=start
            records.append(s)
        (root/'tail_scan_tiny.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
        print('SCANNED_THROUGH',min(start+300,duration),'SECONDS',round(time.time()-began),flush=True)
