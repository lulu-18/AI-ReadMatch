import pandas as pd
from pathlib import Path
f=next(p for p in Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses\raw').glob('*.csv') if '原始' in p.name)
df=pd.read_csv(f,dtype=str,keep_default_na=False,encoding='utf-8-sig')
for n in [1,2,3,5,7,8,9,10,12,13,16,17,18,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]:
    cols=[c for c in df.columns if c.startswith(f'{n}.')]
    print(f'Q{n} ({len(cols)})')
    for c in cols: print('  '+c)
    print()
