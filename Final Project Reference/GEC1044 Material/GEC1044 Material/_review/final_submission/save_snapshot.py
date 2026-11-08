import sys, json, base64, ctypes
from pathlib import Path
k = ctypes.windll.kernel32
h = k.GetStdHandle(-10)
mode = ctypes.c_uint()
k.GetConsoleMode(h, ctypes.byref(mode))
k.SetConsoleMode(h, mode.value & ~4)
print('READY', flush=True)
for line in sys.stdin:
    item = json.loads(line)
    p = Path(item['path'])
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('ab' if item.get('append') else 'wb') as f:
        f.write(base64.b64decode(item['data']))
    print('SAVED', flush=True)
    if item.get('last'):
        break
