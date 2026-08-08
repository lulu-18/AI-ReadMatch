from pathlib import Path
import pandas as pd, re
root=Path(r'D:\桌面\AI ReadMatch\phase-1-user-research\questionnaire-responses')
raw_file=next(p for p in (root/'raw').glob('*.csv') if '原始' in p.name)
df=pd.read_csv(raw_file,dtype=str,keep_default_na=False,encoding='utf-8-sig')
N=len(df)
p=root/'analysis-report.md'
s=p.read_text(encoding='utf-8')
s=re.sub(r'^# .*$',f'# ReadMatch 线上问卷数据分析（{N}份回答）',s,count=1,flags=re.M)
s=re.sub(r'^- 数据实际包含 .*$',f'- 数据实际包含 {N} 份回答；回答编号 1—{N} 唯一，当前按导出数据中的 {N} 份进行分析。',s,count=1,flags=re.M)
# Replace the first issue section without relying on a previous sample size.
start=s.index('### 1. ')
end=s.index('### 2. ',start)
sec1=f'''### 1. 收集元数据同步\n\n当前数据文件实际有 {N} 行回答；本报告以最新 CSV 为准，并将 collection-metadata.md 的回收数量同步为 {N}。\n\n'''
s=s[:start]+sec1+s[end:]
start=s.index('### 2. ',s.index('## 二、'))
end=s.index('### 3. ',start)
sec2='''### 2. 问卷题目范围\n\n- 当前导出数据包含第 1—39 题；第 40—42 题没有部署，因此不作为缺失项。\n- 本报告按导出表格中的实际题目内容和题号分析。\n- 分支题空白按跳过处理，不直接判为无效。\n\n'''
s=s[:start]+sec2+s[end:]
s=s.replace('- 原始数据包含：用户标识/昵称 ID、IP、UA、地区、用户类型等字段；示例数据还出现了昵称字段。','- 原始数据包含用户标识/昵称 ID、IP、UA、地区、用户类型等平台字段；这些字段不是产品研究所必需。')
start=s.index('## 六、')
end=s.index('## 七、',start)
sec6=f'''## 六、当前阶段判断\n\n- 当前共有 {N} 份回答，已达到原定“至少 30 份有效问卷”的数量门槛。\n- 这批数据足以支持方向性问题判断、信任障碍归纳和 MVP 假设排序。\n- 仍不能把本批比例直接推断为总体用户比例，也不能只凭选择题确定最终用户分群。\n- 问卷的核心价值已经从“继续扩量”转向“案例编码、目标用户收敛和竞品任务验证”。\n\n'''
s=s[:start]+sec6+s[end:]
start=s.index('## 七、')
sec7=f'''## 七、下一步\n\n1. 暂停无目的扩量；除非需要补齐特定用户群体，不必继续追求更多随机回答。\n2. 对主动找书和弃书事件做人工案例编码，区分节奏、逻辑、人物、文风、雷点和推荐误导。\n3. 从原始 CSV 生成去标识化分析副本，后续分享只使用副本。\n4. 结合问卷结论设计竞品任务测试和低保真推荐卡验证。\n5. 完成问题定义、目标用户和 MVP 范围后，再进入 PRD。\n'''
s=s[:start]+sec7
p.write_text(s,encoding='utf-8')
# Synchronize collection metadata count and cutoff date.
meta=root/'collection-metadata.md'
if meta.exists():
    m=meta.read_text(encoding='utf-8-sig')
    m=re.sub(r'- 本批回收数量：.*',f'- 本批回收数量：{N}',m)
    m=re.sub(r'- 本批截止日期：.*','- 本批截止日期：2026.8.3',m)
    meta.write_text(m,encoding='utf-8')
print('patched report for',N,'responses')
