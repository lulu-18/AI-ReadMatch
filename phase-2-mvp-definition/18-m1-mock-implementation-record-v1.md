# ReadMatch M1 Mock 端到端实现记录 v1

形成日期：2026-08-12
所有权：助手完成工程实现，项目负责人必须理解数据流、接口边界和验证结果
状态：M1 Mock 主链路已跑通；尚未接入真实模型、持久化数据库和自动评测批跑

## 一、本次完成范围

### 页面和交互

- 三本精选作品选择：《撒野》《囚于永夜》《天官赐福》；
- 正向偏好多选；
- 硬性条件多选；
- 可选自然语言补充；
- 分析结果、逐项雷点状态、Evidence ID、证据强度和重大剧透提示；
- 试读、排除、继续核验和分析不准确反馈。

### 后端/API

- `POST /api/analyze`：校验输入、确认作品、检索证据、调用 Provider、运行规则、返回结构化结果；
- `POST /api/feedback`：校验并记录 M1 Mock 反馈；
- 未收录/非 active 作品不进入分析；
- API 合同与页面解耦，后期可转发给 FastAPI。

### 数据和 Schema

- Book、Evidence、PreferenceOption、AnalysisRequest、AnalysisResult、Feedback 的 Zod Schema；
- 三本书 JSON Fixtures；
- 受控短证据、来源、状态、强度、剧透等级和人工审核字段；
- 所有主观结论通过 evidenceIds 追溯。

### 可替换架构

- Repository：当前 JSON，后期 SQLite/PostgreSQL；
- Retriever：当前结构化标签，后期 Embedding/混合检索；
- ModelProvider：当前 Mock，后期 OpenAI/Python 服务；
- API Contract：前端保持不变，后端可从 Route Handler 迁移到 FastAPI。

## 二、Mock 决策逻辑

1. 用户选择作品和条件；
2. Retriever 先按 `bookId` 限定证据，再按 optionIds 匹配；
3. MockProvider 根据证据状态生成：
   - present；
   - possible；
   - conflicting；
   - unknown；
   - no_evidence；
4. 出现已确认硬性条件时，verdict 为 likely_mismatch；
5. 只有不确定条件时，verdict 为 insufficient_evidence；
6. 规则验证 evidenceId 均来自本次检索；
7. likely_match 不得与 present 的硬性条件共存。

## 三、端到端验证结果

### 《撒野》预测试场景

输入：

- 互攻/攻受位不明确；
- 主角家庭经济困境；
- 校园背景。

输出：

- 互攻：present；
- 校园：present；
- 家庭经济困境：possible；
- 建议：排除。

与必要性预测试 Gold Label 一致。

### 《囚于永夜》预测试场景

输入：

- ABO；
- 关系中的伤害/压迫；
- 死盾/假死推动剧情。

输出：

- ABO：present；
- 关系伤害：conflicting；
- 死盾：possible；
- 重大剧透：只提示，不展开；
- 建议：排除。

与方案 C 的边界一致。

### 反馈

- 反馈 API 返回成功；
- 服务端记录 runId、userAction、helpful、issueTypes 和 optionalText；
- M1 暂未持久化，后续加入 SQLite。

## 四、工程验证

- ESLint：通过；
- TypeScript 独立类型检查：通过；
- Next.js 生产构建：通过；
- 首页：HTTP 200；
- `/api/analyze`：两个核心 Case HTTP 200；
- `/api/feedback`：HTTP 200；
- 浏览器视觉检查：通过；
- 原始问卷、node_modules、`.next` 和环境变量：保持 Git ignore。

## 五、实现中发现并修复的问题

1. TypeScript 7 与当前 typescript-eslint 不兼容，调整为 TypeScript 6.0.3；
2. JSON 文件的 UTF-8 BOM 导致 Turbopack 解析失败，转换为 UTF-8 无 BOM；
3. TypeScript 对 verdict 推断过宽，补充 AnalysisResult 枚举类型；
4. PowerShell/pnpm 无法直接解析 `tsc`，验证脚本改为本地编译器并最终写入标准 `typecheck` script；
5. 正向证据状态判断最初错误使用 `positive`，改为 `present/possible`；
6. 模型调用最初直接依赖 MockProvider，补充统一 ModelProvider 接口。

## 六、项目负责人必须掌握

### 用户点击“开始分析”后发生什么

```text
前端收集书名/偏好/雷点
→ POST /api/analyze
→ Zod 校验输入
→ Repository 找到 Book
→ Retriever 找 Evidence
→ ModelProvider 分析
→ Validator 拦截错误
→ 返回 AnalysisResult
→ 页面展示和收集反馈
```

### 为什么先 Mock

- 当前没有 API Key；
- Mock 先验证页面、数据流、检索和规则；
- 避免模型接入掩盖产品逻辑问题；
- 后续替换 Provider，不重写页面/API。

### 当前不能宣称

- 已使用真实 AI 生成结果；
- 已实现用户自然语言理解；
- 已实现真实成本/Token 记录；
- 已实现数据库持久化；
- 已完成 10 Case 自动评测；
- 已完成真实目标用户测试。

## 七、下一步

### 产品负责人任务

- 实际查看 M1 页面并提出产品层问题；
- 能用自己的话复述主链路；
- 确认当前标签和结果层级是否符合阅读语境。

### 助手任务

1. 建立自动评测 runner；
2. 将 10 个 Case 转为 JSON；
3. 增加 Mock/未来 OpenAI Provider 的统一运行日志；
4. 准备 API Key 获取与预算说明；
5. 在用户确认页面后进入真实模型接入或继续 Mock 评测。
