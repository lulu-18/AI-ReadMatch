# ReadMatch Git 与 GitHub 记录规范

生效日期：2026-08-09

## 一、当前状态

- 本地 Git 仓库：已初始化；
- 默认分支：`main`；
- 初始项目基线提交：`1c2fdd6 chore: preserve project state and product decisions`；
- GitHub 远程：尚未配置；
- 原始问卷目录：已通过 `.gitignore` 排除，不得上传；
- 当前临时提交身份：`ReadMatch Project <readmatch-project@users.noreply.github.com>`，获得用户 GitHub 身份后可改为用户指定身份。

## 二、每次任务结束时的记录顺序

1. 更新与任务直接相关的 PRD、决策、设计、代码或评测文件；
2. 更新 `PROJECT_STATUS.md`：当前阶段、已完成、下一步和阻塞项；
3. 更新 `PROJECT_HISTORY.md`：只记录有实质影响的里程碑；
4. 对 B/C 类产品决策更新相应决策文件，保留用户原始决定和正式表述；
5. 检查 `git status`、`.gitignore` 和暂存文件，确保没有原始问卷、密钥、Token、个人信息或临时文件；
6. 以一个完整里程碑为单位创建提交；
7. 配置 GitHub 远程后推送到 `origin/main`；
8. 最终回复用户时说明提交摘要和是否已推送。

## 三、提交规范

建议使用 Conventional Commits：

- `docs:` 文档、PRD、决策和历史记录；
- `feat:` 新产品功能；
- `fix:` Bug 或评测发现的问题；
- `data:` 数据 Schema、受控书库和标注；
- `eval:` 评测集、评测脚本和结果；
- `refactor:` 不改变功能的结构调整；
- `chore:` 工具、配置和工程维护。

示例：

```text
docs: freeze ReadMatch MVP scope
feat: add single-book preference input
eval: add baseline and grounding test cases
fix: block unsupported risk conclusions
```

## 四、分支建议

一个月个人 MVP 阶段保持简单：

- `main`：稳定里程碑；
- 短期功能分支：只有代码变更较大或需要隔离时使用；
- 文档和小改动可以直接在 `main` 完成后提交；
- 不为了展示工程流程建立过度复杂的 Git Flow。

## 五、安全规则

绝不提交：

- `phase-1-user-research/questionnaire-responses/raw/`；
- `.env`、API Key、GitHub Token；
- 用户昵称、IP、UA、联系方式或未去标识化数据；
- 未获授权的完整书评、小说正文或平台抓取内容；
- 本地数据库、上传文件和临时产物。

上传前执行：

```text
git status --short
git diff --cached --name-only
git check-ignore -v <sensitive-path>
```

## 六、新对话承接

新对话中的助手先读取 `AGENTS.md` 和 `PROJECT_STATUS.md`，再检查 Git 状态和最新提交。除非用户明确要求，不重复询问已经写入决策工作表的产品决定。
