# ReadMatch M1 架构与后期演进边界

形成日期：2026-08-11
所有权：双方共创；助手实现抽象边界，用户理解扩展条件
状态：M1 开发约束

## 一、M1 当前架构

```text
Next.js 页面
↓
Next.js Route Handler
↓
ReadMatch Domain Service
├─ BookRepository(JSON)
├─ EvidenceRetriever(结构化标签)
├─ ModelProvider(Mock)
└─ ResultValidator(规则)
```

M1 的目标是验证业务数据流和产品规则，不是证明单体架构可以支撑所有未来需求。

## 二、必须提前保留的四个可替换接口

### 1. BookRepository

统一能力：

```text
findBookById
searchBooks
getEvidenceByBook
```

M1 实现：JSON。

未来实现：SQLite、PostgreSQL 或远程数据服务。

页面和业务逻辑不得直接读取具体 JSON 路径。

### 2. EvidenceRetriever

统一能力：

```text
retrieve(bookId, positivePreferences, hardConstraints)
```

M1 实现：book_id + aspect + warning_tags + 关键词。

未来实现：Embedding、混合检索、Rerank、外部合法来源 Connector。

### 3. ModelProvider

统一能力：

```text
analyze(input): AnalysisResult
```

M1 实现：MockProvider。

未来实现：OpenAIProvider、其他模型 Provider 或模型路由。

业务逻辑不得直接写死模型名称和 API 调用。

### 4. AnalysisApiClient

前端只调用统一 `/api/analyze` 合同。

M1：Route Handler 在 Next.js 内处理。

未来：Route Handler 可以改为转发给 Python/FastAPI，前端输入输出合同保持不变。

## 三、数据库扩展条件

满足任一条件时从 JSON 迁移到 SQLite/PostgreSQL：

- 需要保存 AnalysisRun；
- 需要保存 Feedback；
- 需要聚合 BookRequest；
- 书库更新频繁；
- 多人协作标注；
- JSON 查询和版本管理开始困难。

推荐路径：

```text
3 本 JSON
→ 30 本 JSON/SQLite 评估
→ SQLite
→ 部署或多人协作后 PostgreSQL
```

## 四、Python 后端扩展条件

满足任一条件时考虑独立 FastAPI：

- 复杂离线数据清洗和批处理；
- Python AI/评测库成为核心依赖；
- 模型调用和检索任务需要后台队列；
- Next.js 请求超时或资源限制；
- 多个客户端共同使用同一后端；
- Agent 或工具调用状态需要独立服务管理。

Python 服务不是“更专业”的装饰，而是在在线业务复杂度超过单体边界时引入。

## 五、联网扩展条件

M1 不联网分析。未来满足以下条件时才增加受约束联网：

- 用户未收录请求集中在可合法接入的来源；
- 受控书库覆盖成为主要留存障碍；
- 来源权限、版权和平台规则已经评审；
- 已有来源可信度、去重、作品身份和剧透规则；
- 可以为联网结果建立独立评测集。

联网层必须通过 Connector 接口，不能让模型任意访问网站并直接写入结论。

## 六、Agent 扩展条件

只有当模型需要根据中间结果自主决定：

- 查询哪个合法来源；
- 是否继续搜索；
- 是否需要交叉核验；
- 何时停止；

才考虑 Agent。

固定流程能解决时继续使用 Workflow。

## 七、面试表达

> M1 我选择 Next.js 单体、JSON 和 Mock，不是因为最终产品只需要这些，而是为了先验证核心数据流和质量规则。我通过 Repository、Retriever、ModelProvider 和 API Contract 保留替换边界；只有出现持久化、复杂数据处理、联网覆盖或动态工具规划需求时，才分别引入数据库、FastAPI、Connector 或 Agent。
