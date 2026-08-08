import pandas as pd, json, re, glob
from pathlib import Path
base=Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses\raw')
for f in sorted(base.glob('*.csv')):
    df=pd.read_csv(f,dtype=str,keep_default_na=False,encoding='utf-8-sig')
    nums=[]
    for c in df.columns:
        m=re.match(r'(\d+)\.', str(c))
        if m: nums.append(int(m.group(1)))
    print(json.dumps({
      'file': f.name,
      'shape': list(df.shape),
      'first_columns': [c for c in df.columns[:10]],
      'question_numbers': sorted(set(nums)),
      'question_count_dist': {str(n):nums.count(n) for n in sorted(set(nums))},
      'last_columns': list(df.columns[-15:]),
      'first_ids': df.iloc[:5,0].tolist(),
      'duration_seconds': df.iloc[:5,3].tolist(),
    }, ensure_ascii=True, indent=2))
