# ReadMatch Web M1

ReadMatch 的三本样例 Mock 端到端应用。

## 当前能力

- 选择《撒野》《囚于永夜》《天官赐福》；
- 选择正向偏好和硬性条件；
- 从 JSON Fixtures 检索受控证据；
- 使用 MockProvider 生成结构化结果；
- 校验证据引用和硬性条件冲突；
- 展示风险、未知、剧透等级和建议动作；
- 提交 M1 Mock 反馈。

## 开发

```bash
pnpm.cmd dev
```

## 验证

```bash
pnpm.cmd lint
pnpm.cmd exec tsc --noEmit
pnpm.cmd build
```

## 模型模式

当前仅支持 Mock。真实模型接入将通过 ModelProvider 替换，不修改页面和 API 合同。
