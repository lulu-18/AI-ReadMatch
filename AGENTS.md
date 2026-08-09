# AI ReadMatch：新对话承接与协作规则

## 必读顺序

每次在新的 Codex 对话中继续本项目时，先阅读以下文件，再开始提出计划、修改文档或编写代码：

1. `PROJECT_STATUS.md`：当前阶段、下一步和已冻结范围；
2. `PROJECT_HISTORY.md`：按日期记录的项目进展；
3. `PROJECT_COLLABORATION_AND_OWNERSHIP.md`：任务所有权与协作边界；
4. `phase-2-mvp-definition/00-mvp-scope-decision-workbook-v1.md`：用户已经亲自确认的产品决策；
5. `CONTEXT.md` 与 `COMMUNICATION_RECORD.md`：项目背景和早期沟通；
6. `git log --oneline -10` 与 `git status`：确认最新基线和未提交变更。

## 当前项目规则

- 项目负责人（用户）是产品 Owner 和最终决策者；
- 助手是 AI PM 导师、技术协作助手和文档/评测支持者；
- 不替用户做关键产品取舍，不伪造调研、用户测试、指标或结论；
- 所有重要任务区分 A（助手可直接完成）、B（双方共创）和 C（用户必须亲自完成）；
- B/C 类任务必须记录证据、选项、用户最终决定、理由和未验证风险；
- 每完成一个里程碑，更新 `PROJECT_STATUS.md`、`PROJECT_HISTORY.md` 和相关决策文件；
- Git 配置完成后，每个完整里程碑创建清晰的本地提交；GitHub 远程可用后推送同步；
- 原始问卷含身份和设备字段，严禁提交 `phase-1-user-research/questionnaire-responses/raw/` 或任何密钥、Token、个人信息。

## 当前下一步

已完成 MVP 范围冻结。下一阶段是共同产出 PRD v1、AI 系统架构、数据 Schema 与评测集设计；不得直接跳到完整编码。

## Windows Git 提示

Codex 沙箱用户与项目目录所有者不同。运行 Git 命令时若出现 `dubious ownership`，使用：

```text
git -c safe.directory='D:/桌面/AI ReadMatch' <command>
```

不要因此删除或重建 `.git`。
