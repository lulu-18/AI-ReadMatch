import pandas as pd, re, json, statistics, math
from pathlib import Path
from collections import Counter, defaultdict

root=Path(r'D:\桌面\AI ReadMatch\phase-1-user-research')
raw_dir=root/'questionnaire-responses'/'raw'
raw_file=next(p for p in raw_dir.glob('*.csv') if '原始' in p.name)
coded_file=next(p for p in raw_dir.glob('*.csv') if '编码' in p.name)
raw=pd.read_csv(raw_file,dtype=str,keep_default_na=False,encoding='utf-8-sig')
coded=pd.read_csv(coded_file,dtype=str,keep_default_na=False,encoding='utf-8-sig')

N=len(raw)

def qnum_from_col(c):
    m=re.match(r'^(\d+)\.', str(c))
    return int(m.group(1)) if m else None

groups=defaultdict(list)
for c in raw.columns:
    n=qnum_from_col(c)
    if n is not None:
        groups[n].append(c)

def strip_code(v):
    v=str(v).strip()
    return re.sub(r'^[A-Z]\.', '', v).strip()

def option_from_col(c):
    if ':' in c:
        s=c.split(':',1)[1]
    else:
        s=c
    s=re.sub(r'\[选项填空\]$','',s).strip()
    s=s.rstrip('_').strip()
    return s

def base_text(n):
    c=groups[n][0]
    s=c.split(':',1)[0]
    s=re.sub(r'^\d+\.', '', s).strip()
    s=re.sub(r'（.*?）','',s).strip()
    return s

def row_answers(row,n):
    vals=[]
    for c in groups.get(n,[]):
        v=str(row[c]).strip()
        if not v:
            continue
        if ':' in c:
            opt=option_from_col(c)
            if '[选项填空]' in c or '____' in opt:
                vals.append('其他填写：'+v)
            else:
                vals.append(opt if v.startswith(tuple('ABCDEFGHIJKLMNOPQRSTUVWXYZ')) else strip_code(v))
        else:
            vals.append(strip_code(v))
    return vals

def q7_is_search(row):
    vals=row_answers(row,7)
    return any(v.startswith('有') and not v.startswith('没有') for v in vals)

def q16_is_abandon(row):
    vals=row_answers(row,16)
    return any(v.startswith('有') for v in vals)

def eligible(n,row):
    if 8 <= n <= 15:
        return q7_is_search(row)
    if 17 <= n <= 21:
        return q16_is_abandon(row)
    return True

def fmt_pct(x,den=N):
    return f'{(x/den*100):.1f}%'

def count_single(n):
    counts=Counter()
    for _,r in raw.iterrows():
        if not eligible(n,r):
            continue
        vals=row_answers(r,n)
        if vals:
            counts[vals[0]]+=1
    return counts

def count_multi(n):
    counts=Counter()
    for _,r in raw.iterrows():
        if not eligible(n,r):
            continue
        for v in row_answers(r,n): counts[v]+=1
    return counts

def response_stats(n):
    elig=sum(1 for _,r in raw.iterrows() if eligible(n,r))
    answered=sum(1 for _,r in raw.iterrows() if eligible(n,r) and row_answers(r,n))
    return elig,answered

def md_table_counts(counts,den,top=None):
    items=counts.most_common(top) if top else counts.most_common()
    lines=['| 选项 | 人数 | 占适用样本 |','|---|---:|---:|']
    for k,v in items:
        lines.append(f'| {k} | {v} | {fmt_pct(v,den)} |')
    return '\n'.join(lines)

# data quality
ids=raw.iloc[:,0].astype(str).tolist()
durations=pd.to_numeric(raw.iloc[:,3],errors='coerce')
start=pd.to_datetime(raw.iloc[:,1],errors='coerce')
end=pd.to_datetime(raw.iloc[:,2],errors='coerce')
question_nums=sorted(groups)
pii_keywords=['用户标识','用户昵称','IP','UA','地理位置','用户类型','自定义字段','Referrer','用户识别']
pii_cols=[c for c in raw.columns if any(k in c for k in pii_keywords)]
# q-level answer counts
qstats=[]
for n in question_nums:
    elig,ans=response_stats(n)
    qstats.append((n,base_text(n),elig,ans,ans/elig if elig else None))

# branching checks
branch_violations=[]
for idx,r in raw.iterrows():
    rid=ids[idx]
    if not q7_is_search(r):
        downstream=[n for n in range(8,16) if row_answers(r,n)]
        if downstream: branch_violations.append((rid,'Q7无主动找书但填写了Q8-Q15',downstream))
    if not q16_is_abandon(r):
        downstream=[n for n in range(17,22) if row_answers(r,n)]
        if downstream: branch_violations.append((rid,'Q16无弃书但填写了Q17-Q21',downstream))

# open text collection
open_rows=[]
for n in [15,21]:
    for idx,r in raw.iterrows():
        vals=row_answers(r,n)
        if vals:
            open_rows.append((ids[idx],n,vals[0]))
# other free text fields among multiselects
for n in question_nums:
    for idx,r in raw.iterrows():
        if not eligible(n,r): continue
        for c in groups[n]:
            if '[选项填空]' in c:
                v=str(r[c]).strip()
                if v: open_rows.append((ids[idx],n,'其他填写：'+v))

# Build report
report=[]
report.append('# ReadMatch 第一批问卷数据初步分析')
report.append('')
report.append('分析日期：2026-08-03')
report.append('')
report.append('> 本报告只基于导出的原始数据做去重、完整性、分流和描述性统计，不把本批样本直接推断为总体用户。')
report.append('')
report.append('## 一、数据概况')
report.append('')
report.append(f'- 原始数据文件：`{raw_file.name}`')
report.append(f'- 编码数据文件：`{coded_file.name}`')
report.append(f'- 两份文件行列数：原始 {raw.shape[0]} 行 × {raw.shape[1]} 列；编码 {coded.shape[0]} 行 × {coded.shape[1]} 列。')
report.append(f'- 数据中的回答编号：{", ".join(ids)}；唯一编号数：{len(set(ids))}。')
report.append(f'- 数据实际包含 22 份回答；收集元数据填写为 22 份，但此前沟通提到 20 份，需要确认其中是否有 2 份测试答卷。')
report.append(f'- 时间范围：{start.min()} 至 {end.max()}。')
if durations.notna().any():
    report.append(f'- 答题时长：最短 {durations.min():.0f} 秒，中位数 {durations.median():.0f} 秒，最长 {durations.max():.0f} 秒；少于 180 秒 {int((durations<180).sum())} 份，少于 300 秒 {int((durations<300).sum())} 份。')
report.append(f'- 导出中存在 {len(pii_cols)} 个潜在身份/设备/地理信息字段，见“隐私问题”。')
report.append('')
report.append('## 二、必须先沟通的异常')
report.append('')
report.append('### 1. 回收数量不一致')
report.append('')
report.append('数据文件实际有 22 行回答，收集元数据也填写了 22，但你前一条消息说收到 20 份。请确认编号 1—22 中是否有两份测试答卷，或“20 份”只是当时的估计。')
report.append('')
report.append('### 2. 导出问卷版本与当前 questionnaire.md 不一致')
report.append('')
report.append(f'- 导出数据只包含第 1—39 题，没有当前文档中的第 40—42 题。')
report.append('- 导出标题中记录的必答标记只出现在第 3、5、7、13 题附近，和后来确定的 15 道必答题不一致。')
report.append('- 导出的第 15 题是“用一句话描述弃书或踩雷经历”，而当前文档中的第 15 题是书名/关键词；说明这批数据来自较早的问卷版本。')
report.append('- 因此，本批数据可以分析，但不能直接按照当前最新版问卷的题号和必答规则解释。后续扩样前应冻结并标注版本。')
report.append('')
report.append('### 3. 原始文件含潜在个人信息')
report.append('')
report.append(f'- 原始数据包含：用户标识/昵称 ID、IP、UA、地区、用户类型等字段；示例数据还出现了昵称字段。')
report.append('- 这不影响当前在本地做分析，但不应把原始 CSV 上传到公开位置、发给无关人员或直接用于截图展示。')
report.append('- 后续分析应使用去标识化副本，至少排除这些平台元数据字段。')
report.append('')
report.append('### 4. 分流逻辑需要核验')
report.append('')
report.append(f'- 检查结果：发现 {len(branch_violations)} 条“分流后仍填写了不应出现的题目”记录。')
if branch_violations:
    for x in branch_violations[:10]: report.append(f'  - 编号 {x[0]}：{x[1]}，题号 {x[2]}')
else:
    report.append('- 当前未发现明显的分流穿透记录，但仍建议在问卷平台中保留一份测试答卷截图作为证据。')
report.append('')

report.append('## 三、样本与填写质量')
report.append('')
# answer completeness by row, adjusted only raw all q groups
row_answer_counts=[]
for idx,r in raw.iterrows():
    count=sum(bool(row_answers(r,n)) for n in question_nums)
    row_answer_counts.append((ids[idx],count))
report.append(f'- 每份回答填写了 {min(x[1] for x in row_answer_counts)}—{max(x[1] for x in row_answer_counts)} 个题组（共 39 个题号；分支跳过属于正常缺失）。')
report.append(f'- 中位答题时长 {durations.median():.0f} 秒，约 {durations.median()/60:.1f} 分钟。问卷预计 5—8 分钟，但本批中位数略高，和“有人反馈题目太长”一致。')
report.append('- 目前不应仅凭“空白题目多”判定无效，因为第 8—15、17—21 题存在分流跳过，且多个题目本来就是选答。')
report.append('')
report.append('### 各题组适用样本和回答率')
report.append('')
report.append('| 题号 | 适用人数 | 有回答人数 | 回答率 |')
report.append('|---:|---:|---:|---:|')
for n,txt,elig,ans,rate in qstats:
    report.append(f'| {n} | {elig} | {ans} | {rate*100:.1f}% |')
report.append('')

# key distributions
key_single=[1,2,6,7,8,11,12,14,16,17,19,25,26,29,33,35,36]
key_multi=[3,4,5,9,10,13,18,20,22,23,24,27,28,30,31,32,34,37,38,39]
report.append('## 四、关键选择题结果（描述性统计）')
report.append('')
for n in key_single:
    if n not in groups: continue
    elig,ans=response_stats(n)
    counts=count_single(n)
    report.append(f'### Q{n} {base_text(n)}')
    report.append(f'适用样本 {elig}，回答 {ans}。')
    report.append('')
    report.append(md_table_counts(counts,elig))
    report.append('')
for n in key_multi:
    if n not in groups: continue
    elig,ans=response_stats(n)
    counts=count_multi(n)
    report.append(f'### Q{n} {base_text(n)}')
    report.append(f'适用样本 {elig}，至少选择一项的回答人数 {ans}。')
    report.append('')
    report.append(md_table_counts(counts,elig,top=10))
    report.append('')

report.append('## 五、开放题和其他填写')
report.append('')
report.append(f'- Q15/Q21 等开放题和“其他填写”共提取 {len(open_rows)} 条非空内容。')
report.append('- 其中有些回答是“无”“没有”等否定性回答，不应直接当作可用于产品设计的具体案例。')
report.append('- 具体开放题内容另存于同目录的 `open-text-review.md`，暂不在本报告中大段复述。')
report.append('')
report.append('## 六、目前可以暂时说什么')
report.append('')
report.append('- 这批数据已经足够做问卷质量审计、题目回答率分析和初步模式发现。')
report.append('- 还不适合直接冻结用户分群、MVP 功能或总体用户比例。')
report.append('- 在确认 22 份中哪些是有效样本、哪个问卷版本后，才应把数字写入正式研究结论。')
report.append('')
report.append('## 七、下一步')
report.append('')
report.append('1. 先确认 22 份中是否包含 2 份测试答卷。')
report.append('2. 确认本批实际使用的是哪个问卷版本，并把版本号写入记录。')
report.append('3. 从原始文件生成去标识化分析副本，不再使用含平台身份字段的原始文件做分享。')
report.append('4. 审核问卷长度和版本差异后，再决定是否继续收集到至少 30 份有效回答。')
report.append('5. 对开放题中的真实案例进行人工编码，再写“多名用户证实”的结论。')
report.append('')

(root/'questionnaire-responses'/'analysis-report.md').write_text('\n'.join(report),encoding='utf-8')

open_lines=['# 开放题内容复核（内部分析用）','', '> 仅用于研究者在本地复核，不要公开或与原始身份字段一起传播。','']
for rid,n,text in sorted(open_rows, key=lambda x:(int(x[0]),x[1])):
    open_lines.append(f'- 编号 {rid} / Q{n}：{text}')
(root/'questionnaire-responses'/'open-text-review.md').write_text('\n'.join(open_lines),encoding='utf-8')

# machine-readable compact summary
summary={
 'raw_rows': int(len(raw)), 'raw_cols': int(raw.shape[1]), 'coded_rows': int(len(coded)), 'coded_cols': int(coded.shape[1]),
 'ids': ids, 'unique_ids': len(set(ids)), 'question_numbers': question_nums,
 'pii_columns': pii_cols, 'branch_violations': branch_violations,
 'duration_seconds': {'min': float(durations.min()), 'median': float(durations.median()), 'max': float(durations.max())},
 'question_response_stats': [{'q':n,'eligible':elig,'answered':ans,'rate':rate} for n,txt,elig,ans,rate in qstats],
}
(root/'questionnaire-responses'/'analysis-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print('wrote',root/'questionnaire-responses'/'analysis-report.md')
print('wrote',root/'questionnaire-responses'/'open-text-review.md')

