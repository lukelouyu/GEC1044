import json
import struct
from pathlib import Path

root=Path(__file__).resolve().parent
path=(root/'backup.wav').resolve()
assert path.parent==root and path.name=='backup.wav'
intervals=json.loads((root/'background_intervals.json').read_text(encoding='utf-8'))['backup']
with path.open('r+b') as file:
    assert file.read(4)==b'RIFF'
    file.read(4)
    assert file.read(4)==b'WAVE'
    while True:
        chunk=file.read(8)
        assert len(chunk)==8
        name,size=struct.unpack('<4sI',chunk)
        if name==b'data':
            data_start=file.tell()
            data_size=size
            break
        file.seek(size+size%2,1)
    for start,end in intervals:
        first=round(start*16000)*2
        last=min(data_size,round(end*16000)*2)
        assert 0<=first<last<=data_size
        file.seek(data_start+first)
        remaining=last-first
        while remaining:
            count=min(remaining,1048576)
            file.write(bytes(count))
            remaining-=count
        print('BACKGROUND_EXCLUDED_FROM_DECODED_BACKUP_CACHE',start,end,flush=True)
(root/'background_mask_applied.json').write_text(json.dumps({'cache':str(path),'original_m4a_modified':False,'intervals':intervals},indent=2),encoding='utf-8')
