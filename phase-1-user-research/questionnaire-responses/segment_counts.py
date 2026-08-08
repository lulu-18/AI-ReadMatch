import pandas as pd,re,json
from pathlib import Path
f=next(p for p in Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses\raw').glob('*.csv') if '原始' in p.name)
df=pd.read_csv(f,dtype=str,keep_default_na=False,encoding='utf-8-sig')
def single(q):
 c=next(c for c in df.columns if c.startswith(f'{q}.') and '[选项填空]' not in c and ':' not in c)
 return df[c].str.extract(r'^([A-Z])\.',expand=False).fillna('')
q2=single(2); q7=single(7); q16=single(16); q29=single(29); q33=single(33)
high=q2.isin(['C','D','E'])
search_fail=q7.isin(['B','C'])
search_success=q7.eq('A')
abandon=q16.eq('A')
satisfied=q29.isin(['A','B'])
print(json.dumps({
 'N':len(df),
 'high_freq':int(high.sum()),
 'high_search_fail':int((high&search_fail).sum()),
 'high_search_success':int((high&search_success).sum()),
 'high_abandon':int((high&abandon).sum()),
 'low_search_fail':int((~high&search_fail).sum()),
 'low_search_success':int((~high&search_success).sum()),
 'low_abandon':int((~high&abandon).sum()),
 'search_fail_satisfied_current_recs':int((search_fail&satisfied).sum()),
 'search_fail_total':int(search_fail.sum()),
 'abandon_and_search_fail':int((abandon&search_fail).sum()),
 'no_or_little_ai':int(q33.isin(['C','D','E']).sum()),
 'occasional_ai':int(q33.eq('B').sum()),
 'frequent_ai':int(q33.eq('A').sum()),
},ensure_ascii=True,indent=2))
