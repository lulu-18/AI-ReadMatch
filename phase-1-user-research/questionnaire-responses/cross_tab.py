import pandas as pd, json
from pathlib import Path
f=next(p for p in Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses\raw').glob('*.csv') if '原始' in p.name)
df=pd.read_csv(f,dtype=str,keep_default_na=False,encoding='utf-8-sig')
# helper q group
import re
from collections import defaultdict
g=defaultdict(list)
for c in df.columns:
 m=re.match(r'^(\d+)\.',c)
 if m:g[int(m.group(1))].append(c)
def vals(r,n):
 out=[]
 for c in g[n]:
  v=str(r[c]).strip()
  if not v: continue
  if ':' in c:
   o=c.split(':',1)[1]
   o=re.sub(r'\[选项填空\]$','',o).rstrip('_').strip()
   if '[选项填空]' in c: out.append('OTHER:'+v)
   else: out.append(re.sub(r'^[A-Z]\.','',v).strip())
  else: out.append(re.sub(r'^[A-Z]\.','',v).strip())
 return out
rows=[]
for _,r in df.iterrows():
 rows.append({'id':r.iloc[0],'q2':vals(r,2)[0] if vals(r,2) else '', 'q7':vals(r,7)[0] if vals(r,7) else '', 'q16':vals(r,16)[0] if vals(r,16) else '', 'q29':vals(r,29)[0] if vals(r,29) else ''})
print(json.dumps(rows,ensure_ascii=False,indent=2))
from collections import Counter
print('q2 x q7')
print(Counter((x['q2'],x['q7']) for x in rows))
print('q2 x q16')
print(Counter((x['q2'],x['q16']) for x in rows))
