import pandas as pd, json
from pathlib import Path
f=next(p for p in Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses\raw').glob('*.csv') if '原始' in p.name)
df=pd.read_csv(f,dtype=str,keep_default_na=False,encoding='utf-8-sig')
for c in [c for c in df.columns if c.startswith('5.')]:
    s=c.split(':',1)[1] if ':' in c else c
    print(json.dumps(s,ensure_ascii=True), [hex(ord(x)) for x in s])
