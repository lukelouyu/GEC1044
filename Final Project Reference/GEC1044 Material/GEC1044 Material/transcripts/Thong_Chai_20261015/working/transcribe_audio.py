import argparse
import json
import os
from pathlib import Path
import sys
import time
import wave
from dataclasses import asdict

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'python_packages'))
os.environ['HF_HOME'] = str(ROOT / 'hf_cache')
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
os.environ['HF_HUB_DISABLE_XET'] = '1'
from faster_whisper import WhisperModel, BatchedInferencePipeline
from faster_whisper.utils import download_model
import numpy as np

def stamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'

parser=argparse.ArgumentParser()
parser.add_argument('--download', action='store_true')
parser.add_argument('--standard', action='store_true')
parser.add_argument('--sample', action='store_true')
parser.add_argument('--names', nargs='+', default=['backup','obsidian'])
parser.add_argument('--tag',default='')
parser.add_argument('--resume',action='store_true')
parser.add_argument('--batch-size',type=int,default=2)
parser.add_argument('--threads',type=int,default=8)
parser.add_argument('--context',action='store_true')
args=parser.parse_args()
model_path=ROOT/'model_large_v3_turbo'
if not (model_path/'model.bin').exists() and (ROOT/'model_standard'/'model.bin').exists():
    model_path=ROOT/'model_standard'
if args.download:
    # A standard HTTP retry uses its own directory if an earlier transfer holds a lock.
    if '--standard' in sys.argv:
        model_path=ROOT/'model_standard'
    print(download_model('turbo',output_dir=str(model_path)),flush=True)
    sys.exit(0)

started=time.time()
model=WhisperModel(str(model_path),device='cpu',compute_type='int8',cpu_threads=args.threads,num_workers=1,local_files_only=True)
pipeline=BatchedInferencePipeline(model=model)
print('MODEL_READY',round(time.time()-started,1),flush=True)
for name in args.names:
    source_name=name.replace('_independent','')
    source=ROOT/(f'{source_name}_sample.wav' if args.sample else f'{source_name}.wav')
    target=ROOT/((f'{name}_sample' if args.sample else name)+args.tag)
    complete=target.with_suffix('.complete.json')
    if complete.exists():
        print('SKIP_COMPLETE',name,flush=True)
        continue
    began=time.time()
    records=[]
    if args.resume and target.with_suffix('.jsonl').exists():
        for line in target.with_suffix('.jsonl').read_text(encoding='utf-8').splitlines():
            if line.strip(): records.append(json.loads(line))
    offset=records[-1]['end'] if records else 0
    old_count=len(records)
    with wave.open(str(source),'rb') as audio_file:
        assert audio_file.getnchannels()==1 and audio_file.getframerate()==16000 and audio_file.getsampwidth()==2
        full_duration=audio_file.getnframes()/16000
        audio_file.setpos(round(offset*16000))
        audio=np.frombuffer(audio_file.readframes(audio_file.getnframes()),dtype='<i2').astype(np.float32)/32768.0
    prompt=('A traditional Chinese medicine teaching session at Singapore Thong Chai Medical Institution. TCM. Tongue body and tongue coating. Pulse diagnosis, radial artery, styloid process of the radius, cun guan chi. Qi, blood, yin, yang, spleen, kidney, liver, heart, lung. Floating pulse, deep pulse, wiry pulse, slippery pulse. Chinese herbs. Acupuncture, acupressure, cupping. Chin Swee Road, Ang Mo Kio, Bukit Batok, Sengkang, Bedok.' if args.context else None)
    segments, info=pipeline.transcribe(audio,batch_size=args.batch_size,language='en',task='transcribe',beam_size=5,
        condition_on_previous_text=False,temperature=0,vad_filter=True,
        initial_prompt=prompt,
        vad_parameters={'min_silence_duration_ms':500},word_timestamps=False)
    print('START',name,'duration',full_duration,'resumed_from',offset,'remaining_speech_duration',info.duration_after_vad,flush=True)
    mode='a' if old_count else 'w'
    with target.with_suffix('.jsonl').open(mode,encoding='utf-8') as raw, target.with_suffix('.txt').open(mode,encoding='utf-8') as txt:
        last_progress=offset-100
        for segment in segments:
            record=asdict(segment)
            record['start']+=offset;record['end']+=offset;record['id']=len(records)+1
            records.append(record)
            raw.write(json.dumps(record,ensure_ascii=False)+'\n'); raw.flush()
            txt.write(f'[{stamp(record["start"])} --> {stamp(record["end"])}] {segment.text.strip()}\n');txt.flush()
            if record['end']-last_progress>=120 or args.sample:
                print('PROGRESS',name,stamp(record['end']),'elapsed_seconds',round(time.time()-began),segment.text.strip(),flush=True)
                last_progress=record['end']
    saved_info=asdict(info)
    saved_info['duration']=full_duration
    complete.write_text(json.dumps({'source':str(source),'model':'faster-whisper large-v3-turbo int8',
        'transcription_info':saved_info,'resumed_from_seconds':offset,'segments_from_prior_pass':old_count,
        'elapsed_seconds_for_final_pass':time.time()-began,'segments':records},ensure_ascii=False,indent=2,default=str),encoding='utf-8')
    print('COMPLETE',name,'segments',len(records),'seconds',round(time.time()-began),flush=True)
