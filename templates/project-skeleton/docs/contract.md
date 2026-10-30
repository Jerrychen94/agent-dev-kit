# 契约：invoice-field-extractor

> 对外承诺。契约变化 = 主版本变化。

## 1. 输入

| 字段 | 类型 | 必填 | 约束 | 示例 |
|---|---|---|---|---|
| text | string | 是 | 1–8000 字符；纯文本或 JSON 包装 | `金额 1280.50 元` |

调用方式：stdin 写入纯文本，或写入 `{"text": "..."}`。最大 8000 字符，超出返回 `INPUT_TOO_LONG`。

## 2. 输出

成功（退出码 0）：

```json
{
  "ok": true,
  "result": {"amount": 1280.5, "date": "2026-03-05", "vendor": "示例科技"},
  "warnings": []
}
```

失败（退出码 1）：

```json
{
  "ok": false,
  "error": {"code": "MISSING_AMOUNT", "message": "未找到金额", "hint": "检查文本是否含金额表述"}
}
```

| 字段 | 类型 | 说明 | 缺失时 |
|---|---|---|---|
| result.amount | number | 金额，保留两位小数 | 失败（MISSING_AMOUNT） |
| result.date | string | `YYYY-MM-DD` 或 `YYYY-MM` | null + warning |
| result.vendor | string | 供应商名称 | null + warning |
| warnings | string[] | `missing_date`、`missing_vendor`、`multiple_amount` | 空数组 |

## 3. 错误码

| code | 含义 | 调用方可做什么 | 是否重试 |
|---|---|---|---|
| EMPTY_INPUT | 输入为空 | 提供文本 | 否 |
| INVALID_INPUT | JSON 解析失败或结构不对 | 修正格式 | 否 |
| NO_INVOICE | 输入不像发票 | 确认输入来源 | 否 |
| MISSING_AMOUNT | 未找到金额 | 检查文本 | 否 |
| INPUT_TOO_LONG | 超过 8000 字符 | 先分段 | 否 |
| UPSTREAM_TIMEOUT | 模型超时 | 稍后重试 | 是，最多 2 次 |
| INTERNAL | 内部错误 | 报告并附 trace_id | 视情况 |

## 4. 工具清单

| 工具 | 输入 | 输出 | 幂等 | 失败返回 |
|---|---|---|---|---|
| extract | 文本 | 三字段 + warnings | 是 | 字段为 null，不抛异常 |
| validate | 三字段 | 规范化结果 | 是 | 字段错误码 |

## 5. 边界（明确不做）

- 不做 OCR、不做图片输入。
- 不做真伪校验、不做多币种换算。
- 不猜缺失字段：文本没有的，一律 null + warning。

## 6. 行为约定

- 幂等：同一输入重复调用结果一致，无副作用。
- 并发：无状态，可并发。
- 超时：默认 30 秒（模型调用 2 次重试）。
- 留存：stdout 结果不落盘；调试日志保留 7 天，脱敏后保存。

## 7. 成本预算

- 单次最大 token：输入 1500 / 输出 200。
- 单次日成本上限：5 元。
- 超限行为：拒绝并返回 `BUDGET_EXCEEDED`。

## 8. 版本

当前版本：`0.1.0`
