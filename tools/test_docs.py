"""Regression checks for links hidden in examples and GitHub heading targets."""

import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("check_docs", Path(__file__).with_name("check-docs.py"))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class MarkdownChecks(unittest.TestCase):
    def test_heading_links_and_duplicate_suffixes(self):
        text = "# A [link](https://example.org) and `code`\n# Same\n# Same\n# Same-1\n"
        self.assertEqual(checker.anchors(text), {"a-link-and-code", "same", "same-1", "same-1-1"})

    def test_short_inner_fence_does_not_end_outer_example(self):
        self.assertNotIn("broken.md", checker.prose("````\n```\n[x](broken.md)\n```\n````"))
        with self.assertRaises(ValueError):
            checker.prose("~~~\nunclosed")

    def test_missing_fragment_fails_but_example_link_is_ignored(self):
        with tempfile.TemporaryDirectory(prefix="blobject-doc-test-") as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            for n in range(12):
                (root / "docs" / f"{n:02d}-test.md").write_text("# Existing\n", encoding="utf-8")
            readme = root / "README.md"
            readme.write_text("[bad](docs/00-test.md#missing)\n", encoding="utf-8")
            previous = checker.ROOT
            checker.ROOT = root
            try:
                with self.assertRaisesRegex(SystemExit, "missing heading"):
                    checker.main()
                readme.write_text("[good](docs/00-test.md#existing)\n`[example](missing.md)`\n", encoding="utf-8")
                with contextlib.redirect_stdout(io.StringIO()):
                    checker.main()
            finally:
                checker.ROOT = previous


if __name__ == "__main__":
    unittest.main()
