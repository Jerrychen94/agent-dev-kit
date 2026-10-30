#!/usr/bin/env python3
"""最小可跑示例 agent：从发票/账单文本中提取金额、日期、供应商。

这是**占位实现**（规则匹配），目的是让骨架开箱可跑、可评测。
替换成真实模型调用时，保持下面的输入输出契约不变：

  stdin  -> 纯文本，或 JSON {"text": "..."}
  stdout -> JSON {"ok": bool, "result": {...}, "warnings": [...], "error": {...}}
  退出码 -> 成功 0，失败 1（失败也要输出 JSON）

契约详见 docs/contract.md。
"""

import json
import re
import sys
from typing import Any

MONEY_RE = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(?:元|块|RMB|CNY)")
DATE_RE = re.compile(r"(\d{4})\s*[年/\-.]\s*(\d{1,2})\s*[月/\-.]\s*(\d{1,2})")
VENDOR_RE = re.compile(r"(?:开票方|供应商|销售方|vendor)\s*[:：]\s*([^\s,，。;；]+)")

INVOICE_HINTS = ("发票", "账单", "invoice", "金额", "元", "CNY")


def _to_float(raw: str) -> float:
    return float(raw.replace(",", ""))


def extract(text: str) -> dict[str, Any]:
    """规则实现：抽取字段。返回 result 字典（字段缺失时为 None）。"""
    warnings: list[str] = []

    money = MONEY_RE.search(text)
    amount = _to_float(money.group(1)) if money else None

    date_match = DATE_RE.search(text)
    date = None
    if date_match:
        year, month, day = (int(part) for part in date_match.groups())
        try:
            date = f"{year:04d}-{month:02d}-{day:02d}"
        except (TypeError, ValueError):
            warnings.append("date_parse_failed")

    vendor_match = VENDOR_RE.search(text)
    vendor = vendor_match.group(1) if vendor_match else None

    return {"amount": amount, "date": date, "vendor": vendor, "warnings": warnings}


def run(payload: str) -> tuple[dict[str, Any], int]:
    """执行一次，返回 (输出对象, 退出码)。"""
    text = payload.strip()
    if not text:
        return _fail("EMPTY_INPUT", "输入为空", "传入发票文本或 JSON {\"text\": ...}"), 1

    if text.startswith("{"):
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            return _fail("INVALID_INPUT", f"JSON 解析失败: {exc}", "检查 JSON 格式"), 1
        if not isinstance(data, dict):
            return _fail("INVALID_INPUT", "顶层必须是对象", "改成 {\"text\": ...}"), 1
        text = str(data.get("text", "")).strip()
        if not text:
            return _fail("EMPTY_INPUT", "text 字段为空", "提供待抽取的文本"), 1

    if not any(hint.lower() in text.lower() for hint in INVOICE_HINTS):
        return _fail("NO_INVOICE", "输入不像发票或账单", "确认传入的是发票文本"), 1

    result = extract(text)
    warnings = result.pop("warnings")

    if result["amount"] is None:
        return _fail("MISSING_AMOUNT", "未找到金额", "检查文本是否含「1280.50 元」这类表述"), 1

    if result["date"] is None:
        warnings.append("missing_date")
    if result["vendor"] is None:
        warnings.append("missing_vendor")

    return {"ok": True, "result": result, "warnings": warnings}, 0


def _fail(code: str, message: str, hint: str) -> dict[str, Any]:
    return {"ok": False, "error": {"code": code, "message": message, "hint": hint}}


def main() -> int:
    payload = sys.stdin.read()
    output, code = run(payload)
    sys.stdout.write(json.dumps(output, ensure_ascii=False) + "\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
