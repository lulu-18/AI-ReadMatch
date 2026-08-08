import pandas as pd, re
from pathlib import Path
from collections import defaultdict

root=Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses')
raw_file=next(p for p in (root/'raw').glob('*.csv') if '原始' in p.name)
df=pd.read_csv(raw_file,dtype=str,keep_default_na=False,encoding='utf-8-sig')

groups=defaultdict(list)
for c in df.columns:
    m=re.match(r'^(\d+)\.',str(c))
    if m: groups[int(m.group(1))].append(c)

def clean(v):
    return re.sub(r'^[A-Z]\.','',str(v).strip()).strip()

def answers(row,q):
    out=[]
    for c in groups.get(q,[]):
        v=str(row[c]).strip()
        if not v: continue
        if ':' in c:
            if '[选项填空]' in c:
                out.append('其他：'+v)
            else:
                option=c.split(':',1)[1]
                option=re.sub(r'\[选项填空\]$','',option).rstrip('_').strip()
                out.append(option)
        else:
            out.append(clean(v))
    # stable de-dup
    seen=[]
    for x in out:
        if x not in seen: seen.append(x)
    return seen

def one(row,q):
    a=answers(row,q)
    return a[0] if a else ''

def join(row,q):
    return '；'.join(answers(row,q)) or '未记录'

def esc(s):
    return str(s).replace('|','／').replace('\n',' ').strip()

def meaningful(text):
    t=text.strip().replace('。','')
    return bool(t and t not in {'无','没有','无弃书和踩雷经验','不记得了'})

search=[]
abandon=[]
for _,row in df.iterrows():
    uid=str(row.iloc[0]).zfill(3)
    freq=one(row,2)
    q7=one(row,7)
    if q7 and not q7.startswith('没有'):
        quote=one(row,15)
        basis='结构化回答 + 开放描述' if meaningful(quote) else '结构化回答'
        search.append({
            '事件':f'S{uid}','用户':uid,'阅读频率':freq,'找书状态':q7,'触发':one(row,8),
            '筛选条件':join(row,9),'查看信息':join(row,10),'耗时':one(row,11),'试读结果':one(row,12),
            '结果评价':one(row,14) or '未回答','开放描述':quote or '未回答','证据基础':basis,
            '证据题号':'Q7—Q15'
        })
    q16=one(row,16)
    if q16=='有':
        quote=one(row,21)
        other18=[x for x in answers(row,18) if x.startswith('其他：')]
        basis='结构化回答 + 开放描述' if meaningful(quote) or other18 else '结构化回答'
        abandon.append({
            '事件':f'A{uid}','用户':uid,'阅读频率':freq,'弃书位置':one(row,17),'弃书原因':join(row,18),
            '提前知道是否开始':one(row,19),'造成影响':join(row,20),'开放描述':quote or '未回答',
            '证据基础':basis,'证据题号':'Q16—Q21'
        })

lines=['# ReadMatch 事件级编码总表 v1','',f'数据来源：`{raw_file.name}`','',
       '> 本表是去标识化的事件级事实整理。它不自动把每一行升级为强证据，也不假设同一用户的 S 和 A 事件是同一本书。','',
       f'- 主动找书事件：{len(search)} 个','- 弃书/踩雷事件：%d 个'%len(abandon),'']
lines += ['## 一、主动找书事件','','| 事件 | 用户 | 阅读频率 | 找书状态 | 触发 | 筛选条件 | 查看信息 | 耗时 | 试读结果 | 结果评价 | 开放描述 | 证据基础 |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
for x in search:
    lines.append('| '+' | '.join(esc(x[k]) for k in ['事件','用户','阅读频率','找书状态','触发','筛选条件','查看信息','耗时','试读结果','结果评价','开放描述','证据基础'])+' |')
lines += ['','## 二、弃书/踩雷事件','','| 事件 | 用户 | 阅读频率 | 弃书位置 | 弃书原因 | 提前知道是否开始 | 造成影响 | 开放描述 | 证据基础 |',
          '|---|---|---|---|---|---|---|---|---|']
for x in abandon:
    lines.append('| '+' | '.join(esc(x[k]) for k in ['事件','用户','阅读频率','弃书位置','弃书原因','提前知道是否开始','造成影响','开放描述','证据基础'])+' |')
lines += ['','## 三、使用规则','',
          '- 表中的选择题事件可以用于统计和方向性编码；','- 只有包含具体行为链、结果、损失或开放描述的事件，才适合升级为详细案例；',
          '- “太难看”“无”等开放回答不能单独作为强证据；','- 具体渠道未在事件模块询问时，不得用 Q4—Q6 的一般习惯代替；',
          '- S 与 A 是否属于同一本书必须标记为未知，除非原始回答明确说明；','- 背景偏好、信任和隐私应从 Q22—Q39 单独补充，不混入事件事实。','']
(root/'case-coding-master-v1.md').write_text('\n'.join(lines),encoding='utf-8')
print('search',len(search),'abandon',len(abandon),'written',root/'case-coding-master-v1.md')
