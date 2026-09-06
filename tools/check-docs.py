"""Check this repository's Markdown paths, heading links, fences, and chapter inventory.

Supports the inline links and ATX headings used here, not arbitrary Markdown.
External URLs are outside this mechanical check; semantic review is separate.
"""

from __future__ import annotations

import html
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r'!?\[([^\]\n]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def prose(text: str) -> str:
    """Omit fenced examples and inline code from link checking."""
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            lines.append("")
        else:
            lines.append(line if fence is None else "")
    if fence is not None:
        raise ValueError("unclosed code fence")
    return "\n".join(lines)


def anchors(text: str) -> set[str]:
    result = set(re.findall(r'<a\s+(?:name|id)=["\']([^"\']+)', text))
    used: set[str] = set()
    for line in prose(text).splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)(?:\s+#+)?$", line)
        if not match:
            continue
        title = LINK.sub(lambda m: m[1], match[1])
        title = html.unescape(re.sub(r"<[^>]+>", "", title)).lower()
        slug = "".join(c for c in title if c.isalnum() or c in "_- ")
        slug = slug.replace(" ", "-")
        candidate, suffix = slug, 0
        while candidate in used:
            suffix += 1
            candidate = f"{slug}-{suffix}"
        used.add(candidate)
        result.add(candidate)
    return result


def main() -> None:
    files = sorted(p for p in ROOT.rglob("*.md") if not any(
        part.startswith(".") or part == "__pycache__"
        for part in p.relative_to(ROOT).parts
    ))
    texts = {p.resolve(): p.read_text(encoding="utf-8-sig") for p in files}
    targets = {p: anchors(t) for p, t in texts.items()}
    errors = []
    checked = 0
    for path, text in texts.items():
        try:
            body = re.sub(r"`+[^`\n]*`+", "", prose(text))
        except ValueError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        for number, line in enumerate(body.splitlines(), 1):
            for match in LINK.finditer(line):
                raw = match[2]
                url = urlsplit(raw)
                if url.scheme or url.netloc:
                    continue
                checked += 1
                target = (path.parent / unquote(url.path)).resolve() if url.path else path
                reason = None
                if not target.exists():
                    reason = "missing file"
                elif url.fragment and target.suffix == ".md":
                    if target not in targets:
                        targets[target] = anchors(target.read_text(encoding="utf-8-sig"))
                    if unquote(url.fragment) not in targets[target]:
                        reason = "missing heading/anchor"
                if reason:
                    errors.append(f"{path.relative_to(ROOT)}:{number}: {reason}: {raw}")

    for number in range(12):
        matches = list((ROOT / "docs").glob(f"{number:02d}-*.md"))
        if len(matches) != 1:
            errors.append(f"Expected one chapter {number:02d}; found {len(matches)}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Markdown: {len(files)} files, {checked} local links, chapters 00–11 checked.")


if __name__ == "__main__":
    main()
