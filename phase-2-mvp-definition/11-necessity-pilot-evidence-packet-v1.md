# ReadMatch 必要性预测试最小证据包 v1

形成日期：2026-08-11
所有权：助手整理来源；用户参与证据审核和 gold label 确认
状态：仅供 CASE-001B 与 CASE-004B 手工模拟；不代表完整书籍画像

## 一、证据使用规则

- 官方页面只用于基础事实、官方标签、简介和作品状态；
- 读者书评只代表该读者观点，不自动升级为作品事实；
- 两个读者来源一致可以提高证据强度，但仍需标明来源类型；
- 不保存完整小说正文或完整书评；
- 本文件只写最小必要摘要和来源地址；
- 重大后期情节标记为 `major`，产品默认不展示细节；
- 没有证据不能输出“不存在”。

## 二、CASE-001B《撒野》证据包

### E-SZ-001｜官方作品基础信息

- source_type：official；
- source_ref：`https://m.jjwxc.net/book2/2956313?whole=1`；
- aspect：relationship / setting / status；
- spoiler_level：none；
- evidence_strength：high；
- 摘要：晋江官方作品页标注为近代现代纯爱、互攻视角，标签包含强强，简介明确为校园文，状态已完结；
- 可支持：互攻视角、校园背景、完结；
- 不可支持：家庭经济困境程度、作品是否适合所有读者。

### E-SZ-002｜出版页面简介

- source_type：publisher_or_bookseller_summary；
- source_ref：`https://www.books.com.tw/products/CN11587694`；
- aspect：family_background / setting；
- spoiler_level：mild；
- evidence_strength：medium；
- 摘要：出版页面简介描述主角从原有生活环境回到亲生父亲所在的钢厂地区，并强调父亲和新环境带来的压抑；
- 可支持：主角家庭和生活环境发生显著变化、钢厂/校园背景；
- 不可直接支持：用统一客观标准认定“主角家里穷”。

### E-SZ-003｜豆瓣读者书评 A

- source_type：reader_review；
- source_ref：`https://book.douban.com/review/12834049/`；
- aspect：family_background / growth / relationship；
- spoiler_level：mild；
- evidence_strength：medium；
- 摘要：该读者认为两名主角的故事具有互相扶持和救赎特征，并描述其中一名主角从较优渥环境进入亲生父亲家庭、面临生活费和环境落差；
- 可支持：部分读者认为存在相互救赎；存在家庭与经济环境压力的读者观点；
- 不可支持：所有读者都认同“贫穷”标签。

### E-SZ-004｜豆瓣读者书评 B

- source_type：reader_review；
- source_ref：`https://book.douban.com/review/9434710/`；
- aspect：family_background / environment；
- spoiler_level：mild；
- evidence_strength：medium；
- 摘要：该读者强调退养、钢厂环境和家庭关系带来的压抑体验；
- 可支持：作品包含明显家庭和生活环境困境；
- 不可支持：精确经济收入或两位主角都属于同一贫困程度。

### CASE-001B gold label 草案

| 用户条件 | 预期状态 | 依据 | 备注 |
|---|---|---|---|
| 互攻/攻受位不明确 | present | E-SZ-001 | 官方页面标注互攻视角 |
| 校园背景 | present | E-SZ-001 | 官方简介明确校园文 |
| 主角家庭经济困境 | possible | E-SZ-002/003/004 | 有家庭和经济压力线索，但“穷”的阈值主观，避免绝对化 |

### 禁止结论

- 不得说“两个主角都一定贫穷”；
- 不得把家庭环境困难写成作品质量缺陷；
- 不得在有官方互攻标注时输出“确定不是互攻”；
- 不得因满足三个避开条件就断言所有用户都不适合阅读。

## 三、CASE-004B《囚于永夜》证据包

### E-QY-001｜官方作品基础信息

- source_type：official；
- source_ref：`https://m.jjwxc.net/book2/10526441?more=0&whole=1`；
- aspect：setting / relationship / warning / status；
- spoiler_level：mild；
- evidence_strength：high；
- 摘要：晋江官方页面标注主受视角、已完结；简介明确角色从 beta 被植入 omega 腺体、具有高匹配度，并使用先订婚后爱、狗血等描述；
- 可支持：ABO 世界设定、关系位官方视角、先订婚后爱、存在强制改造背景；
- 不可直接支持：攻方是否构成所有读者定义下的“虐受”、后期假死情节。

### E-QY-002｜晋江读者长评

- source_type：reader_review_on_official_platform；
- source_ref：`https://www.jjwxc.net/comment.php?commentid=552424&novelid=10526441`；
- aspect：relationship_harm / fake_death / ending；
- spoiler_level：major；
- evidence_strength：medium；
- 摘要：读者长评描述早期关系中的恶劣言语、角色因外部安排被迫改变身份，以及后期爆炸、被认为死亡、实际生还和多年后重逢；
- 可支持：存在情感伤害/关系冲突的读者描述；存在符合“假死推动剧情”定义的后期情节线索；
- 不可支持：所有伤害均由攻方造成，或所有读者都会将其归为攻虐受。

### E-QY-003｜读者书评/推荐文

- source_type：reader_review；
- source_ref：`https://www.txtnovel.vip/thread-4114884-1-1.html`；
- aspect：setting / family_control / emotional_tone；
- spoiler_level：mild；
- evidence_strength：medium；
- 摘要：该读者将作品描述为 ABO 系列背景、家族控制和狗血/破镜重圆体验，并提到角色被改造成匹配对象；
- 可支持：ABO、家族控制、情绪和关系冲突的读者观点；
- 不可支持：死盾梗的完整情节或伤害责任归属。

### E-QY-004｜第二个后期情节读者来源

- source_type：reader_summary；
- source_ref：`https://www.sohu.com/a/930414894_122177875`；
- aspect：fake_death / reunion；
- spoiler_level：major；
- evidence_strength：low_to_medium；
- 摘要：该来源同样描述角色通过假死离开并在多年后重逢；
- 可支持：作为 E-QY-002 的第二条读者来源，增强假死情节存在的可信度；
- 不可单独支持：复杂剧情动机和全部时间线。

### CASE-004B gold label 草案

| 用户条件 | 预期状态 | 依据 | 备注 |
|---|---|---|---|
| ABO | present | E-QY-001/003 | 官方简介已包含 beta/omega 设定 |
| 攻虐受 | conflicting/possible | E-QY-001/002/003 | 有强制背景、恶劣言语和关系伤害描述，但伤害来源、程度和读者定义需要拆分 |
| 死盾梗 | present_with_medium_evidence | E-QY-002/004 | 两个读者来源描述假死与后续重逢；属于重大剧透，默认只显示状态 |

### 禁止结论

- 不得把角色被家族强制改造全部归因于攻方；
- 不得只使用“攻虐受”而不拆分具体伤害；
- 不得在未警告的情况下展开假死和重逢情节；
- 不得因为读者来源提到假死就生成未被证据支持的完整剧情；
- 不得把 ABO 设定本身表述为作品缺陷。

## 四、证据包局限

- 该证据包只服务两个用户条件 Case，不是完整作品画像；
- 《撒野》的家庭经济困境存在阈值和角色差异，gold label 暂定 possible；
- 《囚于永夜》的“攻虐受”属于复合圈层词，不能形成单一二元事实；
- 后期假死证据来自读者来源而非官方简介，需要标注证据等级和剧透；
- 后续用户审核可以调整 gold label，但必须记录调整理由。
