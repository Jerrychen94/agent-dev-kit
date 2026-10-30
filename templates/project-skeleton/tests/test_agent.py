"""单元测试：只测确定性的处理逻辑，不调用模型。"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import agent  # noqa: E402


class TestExtract(unittest.TestCase):
    def test_amount_with_thousand_separator(self):
        result = agent.extract("金额 1,280.50 元")
        self.assertEqual(result["amount"], 1280.5)

    def test_date_formats(self):
        for text, expected in [
            ("2026年3月5日", "2026-03-05"),
            ("2026-03-05", "2026-03-05"),
            ("2026/3/5", "2026-03-05"),
        ]:
            with self.subTest(text=text):
                self.assertEqual(agent.extract(text)["date"], expected)

    def test_missing_fields_are_none(self):
        result = agent.extract("只有 12 元")
        self.assertIsNone(result["date"])
        self.assertIsNone(result["vendor"])


class TestRun(unittest.TestCase):
    def test_empty_input_fails(self):
        output, code = agent.run("   ")
        self.assertEqual(code, 1)
        self.assertEqual(output["error"]["code"], "EMPTY_INPUT")

    def test_missing_amount_fails(self):
        output, code = agent.run("2026年3月5日发票，开票方：示例科技")
        self.assertEqual(code, 1)
        self.assertEqual(output["error"]["code"], "MISSING_AMOUNT")

    def test_happy_path(self):
        output, code = agent.run("2026年3月5日发票，金额 1280.50 元，开票方：示例科技")
        self.assertEqual(code, 0)
        self.assertTrue(output["ok"])
        self.assertEqual(output["result"]["amount"], 1280.5)


if __name__ == "__main__":
    unittest.main()
