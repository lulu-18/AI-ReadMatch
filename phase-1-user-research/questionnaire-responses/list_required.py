import pandas as pd, json, re
from pathlib import Path
f=next(p for p in Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses\raw').glob('*.csv') if '原始' in p.name)
df=pd.read_csv(f,dtype=str,keep_default_na=False,encoding='utf-8-sig')
for n in range(1,40):
    cols=[c for c in df.columns if c.startswith(f'{n}.')]
    if not cols: continue
    base=cols[0]
    m=re.match(r'\d+\.(.*?)(?:（|\(|:|$)', base)
    print(json.dumps({'q':n,'required_marker':any('必答' in c for c in cols),'first_header':base},ensure_ascii=True))
