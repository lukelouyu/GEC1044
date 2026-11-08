import json
from pathlib import Path
from datetime import datetime

root=Path(__file__).resolve().parent
print(datetime.now().isoformat(timespec='seconds'))
for name in ['obsidian','backup_independent']:
    path=root/f'{name}.jsonl'
    if not path.exists():
        print(name,'waiting for first batch')
        continue
    lines=path.read_text(encoding='utf-8').splitlines()
    records=[]
    for line in lines:
        try: records.append(json.loads(line))
        except json.JSONDecodeError: pass
    end=records[-1]['end'] if records else 0
    complete=(root/f'{name}.complete.json').exists()
    print(name,'complete',complete,'segments',len(records),'through',f'{int(end//60):02}:{int(end%60):02}')
