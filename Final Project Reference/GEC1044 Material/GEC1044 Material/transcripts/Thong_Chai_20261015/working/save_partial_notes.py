import json
import re
from pathlib import Path

root=Path(__file__).resolve().parent
out=root.parent
omissions=json.loads((root/'background_intervals.json').read_text(encoding='utf-8'))

def stamp(t):
    sec=round(t)
    return f'{sec//3600:02}:{sec//60%60:02}:{sec%60:02}'

for key,prefix,label,total in [('obsidian','obsidian','Obsidian recording',4442.26),('backup','backup_independent','Backup recording',4400.64)]:
    records=[json.loads(line) for line in (root/f'{prefix}.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
    end=records[-1]['end']
    lines=[f'# Singapore Thong Chai Medical Institution partial transcript', '',f'**Source:** {label}  ',
           f'**Captured through:** {stamp(end)} of {stamp(total)}  ',
           '**Status:** Transcription stopped at the user\'s request on 16 October 2026. This is an incomplete automated draft.', '',
           'Ambient noise and unrelated practice-room chatter are omitted where identified. Other unclear wording remains marked for audio review. Technical terms, names and numbers have not been fully corrected; this text should not be treated as a verified quotation. Timestamps are approximate segment boundaries.', '',
           'The two recordings cover the same session. Obsidian time is approximately backup time plus 44.44 seconds. The Obsidian recording includes the earlier opening.', '',
           '## Captured speech', '']
    marked=set()
    for record in records:
        start,stop=record['start'],record['end']
        midpoint=(start+stop)/2
        excluded=None
        for index,(a,b) in enumerate(omissions[key]):
            if a<=midpoint<b:
                excluded=(index,a,b)
                break
        if excluded:
            index,a,b=excluded
            if index not in marked:
                lines.extend([f'*[{stamp(a)} to {stamp(min(b,end))}: ambient noise and unrelated background chatter omitted]*',''])
                marked.add(index)
            continue
        text=record['text'].strip()
        # Remove an unrelated conversation before the recognizable transition to pulse teaching.
        if key=='obsidian' and 774<=start<=776 and 'Okay, now' in text:
            text=text[text.index('Okay, now'):]
        tiny=re.sub(r'[^a-z ]','',text.lower()).strip()
        if tiny and set(tiny.split())<= {'thank','you','very','much','ha','um','oh'}:
            continue
        # Contextually clear acronym variants are normalized, without guessing other terms.
        text=re.sub(r'\b(?:KCM|TCN|CCM)\b','TCM',text)
        flag=record.get('avg_logprob',0)<-.65 or record.get('compression_ratio',0)>2.5
        flag=flag or bool(re.search(r'\b(?:house|houses|cows|towels|glycemic|artificial|Shinsu|Hukipatok|Angokyo|Shinsui|Putipato|Amokyo|teeth|spine)\b',text,re.I))
        lines.extend([f'**[{stamp(start)} to {stamp(stop)}]** '+('**Wording needs review:** ' if flag else '')+text,''])
    lines.extend([f'*Transcription stops at {stamp(end)}. The remaining audio has not been transcribed.*',''])
    name=f'0{1 if key=="obsidian" else 2}_{key.title()}_Partial_Transcript.md'
    (out/name).write_text('\n'.join(lines),encoding='utf-8')
    print(name,stamp(end),len(records),'segments')
