import pandas as pd, json, glob, re
from pathlib import Path
f=[p for p in Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses\raw').glob('*.csv') if '原始' in p.name][0]
df=pd.read_csv(f,dtype=str,keep_default_na=False,encoding='utf-8-sig')
for r in [0,1,2]:
    out={}
    for i in list(range(0,15))+list(range(258,272)):
        out[str(i)+':'+df.columns[i]]=df.iloc[r,i]
    print('ROW',r, json.dumps(out,ensure_ascii=True,indent=2))
