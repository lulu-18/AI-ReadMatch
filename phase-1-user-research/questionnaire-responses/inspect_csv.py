import pandas as pd, json, os, re
from pathlib import Path
base=Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses\raw')
files=list(base.glob('*.csv'))
for f in files:
    df=pd.read_csv(f, dtype=str, keep_default_na=False, encoding='utf-8-sig')
    print('\nFILE', f.name)
    print('shape', df.shape)
    print('columns', len(df.columns))
    for i,c in enumerate(df.columns[:25]): print(i, repr(c))
    print('last columns')
    for i,c in enumerate(df.columns[-20:], start=len(df.columns)-20): print(i, repr(c))
    print('first ids', df.iloc[:5,0].tolist())
    print('duration stats', df.iloc[:,3].head().tolist() if df.shape[1]>3 else '')
