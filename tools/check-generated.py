"""Regenerate and compare published CSV/SVG artifacts without overwriting them."""

from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(*args: object) -> None:
    subprocess.run([sys.executable, *map(str, args)], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="blobject-artifacts-") as directory:
        temporary = Path(directory)
        output = temporary / "models"
        figures = temporary / "figures"
        run("models/spot_simulation.py", "--output-dir", output)
        run("models/render_charts.py", "--input-dir", output, "--output-dir", output)
        run("tools/render-rfc-figures.py", "--output-dir", figures)
        errors = []
        count = 0
        for generated, published in ((output, ROOT / "models/output"),
                                     (figures, ROOT / "docs/assets/figures")):
            actual = {p.name for p in generated.iterdir() if p.suffix in {".csv", ".svg"}}
            expected = {p.name for p in published.iterdir() if p.suffix in {".csv", ".svg"}}
            for name in sorted(actual | expected):
                count += 1
                a, b = generated / name, published / name
                if not a.exists() or not b.exists() or a.read_text(encoding="utf-8") != b.read_text(encoding="utf-8"):
                    errors.append(str(b.relative_to(ROOT)))
        if errors:
            raise SystemExit("Generated artifacts differ: " + ", ".join(errors))
        print(f"Generated artifacts: {count} CSV/SVG files match isolated regeneration.")


if __name__ == "__main__":
    main()
