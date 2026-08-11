# ReadMatch M1 技术栈与模型/API 决策 v1

形成日期：2026-08-11
所有权：双方共创，项目负责人最终确认并理解主要取舍
状态：待确认；尚未创建工程骨架或安装依赖

## 一、本机环境核对

- Node.js：v24.18.0；
- npm：11.16.0，通过 `npm.cmd` 使用；
- pnpm：11.9.0，通过 `pnpm.cmd` 使用；
- Python：3.12.12；
- 当前 Python 没有 pip；
- 当前目录没有 package.json、pyproject.toml 或正式应用代码；
- PowerShell 执行策略阻止 npm.ps1/pnpm.ps1，因此 Windows 命令使用 `npm.cmd`/`pnpm.cmd`。

## 二、三种实现路线

### 方案 A：Streamlit + Python

#### 结构

```text
Streamlit UI
+ Python 分析逻辑
+ JSON/SQLite
+ 模型 API
```

#### 优点

- 最快完成界面；
- 数据处理和评测容易；
- Python 对 AI 实验友好。

#### 缺点

- 当前 Python 环境缺少 pip，需要先修环境；
- UI 和交互更像实验工具；
- 作品集展示质量和前端交互上限较低；
- 后续迁移到正式 Web 产品可能重做界面。

#### 适用

只追求快速验证，不重视产品化展示。

### 方案 B：Next.js + FastAPI

#### 结构

```text
Next.js 前端
→ FastAPI 后端
→ Python AI/评测
→ SQLite/PostgreSQL
```

#### 优点

- 前后端职责清楚；
- Python 适合 AI 数据和评测；
- 接近团队式产品架构；
- 后续扩展方便。

#### 缺点

- 同时维护 Node 和 Python；
- 需要两个开发服务、接口和部署；
- 当前 Python 环境需要补 pip；
- 一个月个人项目容易把时间花在接口和环境上。

#### 适用

已有 FastAPI 和 React 经验、开发周期更长的项目。

### 方案 C：Next.js 全栈 TypeScript + 本地证据数据

#### 结构

```text
Next.js App Router
├─ 页面和交互
├─ Route Handlers/API
├─ ReadMatch Workflow
├─ 规则校验
├─ 模型适配器
└─ 评测脚本

M1 数据：JSON Fixtures
后续数据：SQLite
```

#### 优点

- 当前 Node/pnpm 环境可直接使用；
- 一个项目、一个开发服务器；
- 页面和 API 使用同一套 TypeScript 类型；
- AnalysisResult Schema 可以前后端复用；
- 更容易做出作品集级 Web 界面；
- 减少 FastAPI 和 Python 环境配置；
- 后续仍可单独增加 Python 数据/评测脚本。

#### 缺点

- AI 数据处理不如 Python 生态自然；
- 需要理解 TypeScript、React 和服务端 Route Handler；
- 如果后期复杂离线数据处理增加，可能仍需 Python 工具。

#### 适用

一个月内完成可展示 Web MVP，同时保留评测和扩展能力。

## 三、推荐方案

> **M1 选择方案 C：Next.js 全栈 TypeScript。**

原因不是“Next.js 更高级”，而是：

1. 当前 Node 环境已可用，Python 缺少 pip；
2. 一套 Schema 可以同时服务前端、API 和评测；
3. M1 数据只有 3 本，无需先建立复杂数据库后端；
4. 减少两个服务和跨语言接口；
5. 作品集需要一个较完整的 Web 产品界面；
6. 后续如果离线数据处理复杂，再增加 Python 工具，不影响在线产品。

## 四、M1 数据与数据库策略

### M1：JSON Fixtures

```text
data/
├─ books.json
├─ evidence.json
├─ preference-options.json
└─ evaluation-cases.json
```

优点：

- 先验证端到端数据流；
- 数据可以直接 Git diff 和人工审核；
- 不因数据库迁移阻塞三本 Demo；
- 方便建立固定评测输入。

### M2：SQLite

只有在以下需求出现后加入：

- AnalysisRun 和 Feedback 需要持久化；
- BookRequest 需要聚合；
- 评测结果需要查询；
- JSON 文件更新开始不方便。

M1 不因为 PRD 中设计了数据库 Schema 就必须第一天建立全部表。

## 五、项目目录建议

```text
apps/web/
├─ app/
│  ├─ page.tsx
│  ├─ analyze/page.tsx
│  ├─ result/[runId]/page.tsx
│  └─ api/analyze/route.ts
├─ components/
├─ lib/
│  ├─ books.ts
│  ├─ retrieve-evidence.ts
│  ├─ build-prompt.ts
│  ├─ validate-result.ts
│  └─ model-provider.ts
├─ schemas/
│  ├─ book.ts
│  ├─ evidence.ts
│  ├─ preference.ts
│  └─ analysis-result.ts
└─ data/
   ├─ books.json
   ├─ evidence.json
   └─ preference-options.json

evals/
├─ cases/
├─ run-baseline.ts
├─ run-readmatch.ts
├─ score-output.ts
└─ reports/
```

逻辑上仍然区分 UI、数据、检索、模型和规则，只是不在 M1 物理拆成两个服务。

## 六、模型/API 候选

官方模型指南当前将 GPT-5.6 系列分为：

- `gpt-5.6-sol`：复杂专业任务和高质量参考；
- `gpt-5.6-terra`：智能与成本平衡；
- `gpt-5.6-luna`：成本敏感和批量任务。

官方建议使用 Responses API，并根据工作负载有意选择 reasoning effort。GPT-5.6 Terra 支持 Structured Outputs。

参考：

- `https://developers.openai.com/api/docs/guides/latest-model`
- `https://developers.openai.com/api/docs/models/gpt-5.6-terra`

## 七、推荐模型分工

### 产品默认模型

```text
gpt-5.6-terra
reasoning.effort = medium
```

用途：

- 用户补充文本结构化；
- 基于证据生成 AnalysisResult；
- M1 响应质量/成本/速度平衡。

### 高质量参考模型

```text
gpt-5.6-sol
reasoning.effort = high
```

用途：

- 难例参考；
- Gold Label 辅助复核；
- 和 Terra 做少量质量上限比较。

不作为默认产品模型，避免预测试中数分钟等待和更高成本。

### 批量评测候选

```text
gpt-5.6-luna
reasoning.effort = low/medium
```

用途：

- 低成本批量 Baseline；
- 简单分类或格式任务；
- 需要通过 10 Case 比较后再决定是否使用。

## 八、API 使用原则

### 使用 Responses API

原因：

- 当前官方推荐的生产 API 路线；
- 支持 reasoning、工具和结构化输出；
- 后续可保持 provider adapter，不把业务逻辑写死在页面中。

### 使用 Structured Outputs

AnalysisResult 必须符合 JSON Schema：

```text
verdict
match_points
evidence_ids
risk_points
hard_constraint_checks
conflicting_views
unknown_items
suggested_action
summary
```

模型输出后仍需规则校验，Structured Outputs 不替代业务规则。

### 产品运行时不使用 Web Search

M1 模型只能看到受控 Evidence ID，不允许自行联网补充作品信息。

原因：

- 防止证据来源漂移；
- 保持可复现；
- 降低剧透和错误来源；
- 使 ReadMatch 与联网 Baseline 的差异清楚。

Web Search 只用于离线数据准备和 Baseline 实验，不进入 v1 在线分析 Workflow。

## 九、无 API Key 时的 Mock 模式

工程必须支持：

```text
READMATCH_MODEL_MODE=mock
```

Mock 模式：

- 使用 CASE-001B 和 CASE-004B 的固定方案 C 结果；
- 先完成页面、检索、规则和反馈流程；
- 不因为 API Key 阻塞基础工程；
- 获得 API Key 后切换到 `openai` adapter。

真实 Key 只能存放于：

```text
.env.local
```

不得提交 GitHub。

## 十、需要项目负责人确认

1. 是否同意 M1 使用 Next.js 全栈 TypeScript，而不是 Next.js + FastAPI？
2. 是否同意 M1 使用 JSON Fixtures，等需要运行日志/反馈持久化时再加入 SQLite？
3. 是否同意默认模型使用 `gpt-5.6-terra` medium，`gpt-5.6-sol` high 只作为质量参考？
4. 是否同意产品运行时不联网，只使用受控 Evidence；联网仅用于离线准备和 Baseline？
5. 是否有可用于 OpenAI API 的 Key 和少量测试预算？如果暂时没有，先使用 Mock 模式，不阻塞前端和规则开发。

## 十一、项目负责人必须理解

- 为什么单体应用不等于没有架构；
- 为什么 M1 不急着建数据库；
- 为什么模型需要分默认、质量参考和批量评测角色；
- 为什么 Structured Outputs 仍然需要规则校验；
- 为什么产品运行时不联网；
- 为什么 API Key 不能写进代码或上传 GitHub。
