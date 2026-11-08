import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent

def stamp(t):
    sec=int(t)
    return f'{sec//3600:02}:{sec//60%60:02}:{sec%60:02}'

for name,title,duration,source in [
    ('obsidian','Obsidian recording transcript','01:14:02',"Recording 20261015164725.m4a"),
    ('backup','Backup recording transcript','01:13:21','Singapore Thong Chai Medical Institution.m4a'),
]:
    result=json.loads((ROOT/f'{name}.complete.json').read_text(encoding='utf-8'))
    segments=result['segments']
    text=[f'# Singapore Thong Chai Medical Institution {title.lower()}', '',
          f'**Source:** {source}  ',f'**Duration:** {duration}  ',
          '**Prepared:** 16 October 2026  ',
          '**Format:** Timestamped automated English transcription', '',
          'This document preserves the speech recognizer output, including conversational wording. It is a working transcript, not a certified verbatim record. Punctuation and sentence boundaries are generated automatically. Speaker identities have not been verified and are not assigned.', '',
          'Every timestamp refers to this recording. The companion file covers the same session with a start offset of approximately 44.44 seconds: **Obsidian time = backup time + 00:44.44**. The Obsidian file includes the earlier opening; the backup extends about 2.82 seconds beyond the Obsidian ending.', '',
          'Passages marked **Review audio** have low model confidence, unusually repetitive output, or very little recognized speech across a long interval. This flag is a screening aid, not a measured error rate. Unflagged passages can still contain errors, especially names, technical vocabulary and numbers. Short responses, laughter and repeated phrases during audience activities can be recognition artifacts. Editorial clarifications and factual checks are kept in the separate content evaluation so they do not overwrite what was transcribed.', '',
          '## Transcript', '']
    review=[]
    last_heading=-1
    prev_end=0
    for s in segments:
        bucket=int(s['start']//300)
        if bucket!=last_heading:
            text.extend([f'### From {stamp(bucket*300)}',''])
            last_heading=bucket
        if s['start']-prev_end>15:
            text.extend([f'*[{stamp(prev_end)} to {stamp(s["start"])}: no speech transcribed by the model]*',''])
        words=s['text'].strip()
        word_rate=len(words.split())/max(1,s['end']-s['start'])
        flag=s.get('avg_logprob',0)<-.65 or s.get('compression_ratio',0)>2.5 or (s['end']-s['start']>20 and word_rate<.4)
        if flag:
            review.append({'start':s['start'],'end':s['end'],'text':words,'avg_logprob':s.get('avg_logprob'),'compression_ratio':s.get('compression_ratio')})
        text.extend([f'**[{stamp(s["start"])} to {stamp(s["end"])}]** '+('**Review audio:** ' if flag else '')+words,''])
        prev_end=s['end']
    audio_duration=result['transcription_info']['duration']
    if audio_duration-prev_end>15:
        text.extend([f'*[{stamp(prev_end)} to {stamp(audio_duration)}: no further speech transcribed by the model]*',''])
    (OUT/f'0{1 if name=="obsidian" else 2}_{name.title()}_Transcript.md').write_text('\n'.join(text),encoding='utf-8')
    (ROOT/f'{name}_review_flags.json').write_text(json.dumps(review,ensure_ascii=False,indent=2),encoding='utf-8')
    print(name,'segments',len(segments),'words',sum(len(re.findall(r"\S+",s['text'])) for s in segments),'review_flags',len(review))
