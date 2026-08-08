import pandas as pd, re, json
from pathlib import Path
base=Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses\raw')
f=next(p for p in base.glob('*.csv') if '原始' in p.name)
df=pd.read_csv(f,dtype=str,keep_default_na=False,encoding='utf-8-sig')
row=df[df.iloc[:,0].astype(str)=='6'].iloc[0]
for c in df.columns:
    if not re.match(r'^\d+\.',c): continue
    v=str(row[c]).strip()
    if v:
        print(f'{c}\t{v}')
