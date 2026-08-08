import pandas as pd, json
from pathlib import Path
f=next(p for p in Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses\raw').glob('*.csv') if '原始' in p.name)
df=pd.read_csv(f,dtype=str,keep_default_na=False,encoding='utf-8-sig')
for n in [7,8,12,13,16,17,18,19,21,22,23,24,25,28,29,33,35,36]:
    cols=[c for c in df.columns if c.startswith(f'{n}.')]
    print('Q',n)
    for c in cols:
        vals=sorted(set(v for v in df[c].tolist() if v))
        print(json.dumps({'header':c,'values':vals},ensure_ascii=True))
