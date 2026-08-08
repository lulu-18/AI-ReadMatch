import pandas as pd, json
from pathlib import Path
f=next(p for p in Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses\raw').glob('*.csv') if '原始' in p.name)
df=pd.read_csv(f,dtype=str,keep_default_na=False,encoding='utf-8-sig')
for n in [14,15,16,17,18,19,20,21,22,23,24,25,26,27,29,32,34,37,38,39]:
    cols=[c for c in df.columns if c.startswith(f'{n}.')]
    vals=[]
    for _,row in df.iterrows():
        for c in cols:
            v=str(row[c])
            if v: vals.append((df.iloc[_,0],c,v))
    print('Q',n,'nonempty cells',len(vals),'rows',len(set(x[0] for x in vals)))
    print(json.dumps([(x[0],x[2]) for x in vals[:20]],ensure_ascii=True))
