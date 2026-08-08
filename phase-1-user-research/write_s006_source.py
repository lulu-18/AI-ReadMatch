import pandas as pd,re
from pathlib import Path
base=Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses\raw')
f=next(p for p in base.glob('*.csv') if '原始' in p.name)
df=pd.read_csv(f,dtype=str,keep_default_na=False,encoding='utf-8-sig')
row=df[df.iloc[:,0].astype(str)=='6'].iloc[0]
lines=['# S006 原始数据复核摘录','',f'数据文件：{f.name}','', '> 仅保留与案例编码相关的问卷题目，不包含平台身份/设备字段。','']
for c in df.columns:
    if not re.match(r'^\d+\.',c): continue
    v=str(row[c]).strip()
    if not v: continue
    q=re.match(r'^(\d+)\.',c).group(1)
    if ':' in c:
        opt=c.split(':',1)[1]
        opt=re.sub(r'\[选项填空\]$','',opt).rstrip('_').strip()
        if '[选项填空]' in c:
            label='其他填写'
        else:
            label=opt
        val=re.sub(r'^[A-Z]\.', '', v).strip()
        lines.append(f'- Q{q}｜{label}：{val}')
    else:
        val=re.sub(r'^[A-Z]\.', '', v).strip()
        lines.append(f'- Q{q}｜{val}')
(Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\s006-source-review.md')).write_text('\n'.join(lines),encoding='utf-8')
