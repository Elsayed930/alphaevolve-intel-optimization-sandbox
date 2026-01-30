from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _fmt_float(x: Any, digits: int = 4) -> str:
    try:
        return f"{float(x):.{digits}f}"
    except Exception:
        return str(x)


def summarize(report_path: Path, out_path: Path) -> None:
    data = json.loads(report_path.read_text(encoding="utf-8"))

    benchmark = data.get("benchmark", "unknown")
    best_candidate = (data.get("best_candidate") or {}).get("params", {})
    best_score = data.get("best_score") or {}
    history = data.get("history") or []

    # Find best step by total score
    best_step = None
    best_total = float("-inf")
    for row in history:
        score = (row.get("score") or {})
        total = score.get("total")
        if isinstance(total, (int, float)) and total > best_total:
            best_total = float(total)
            best_step = row.get("step")

    lines = []
    lines.append(f"# Latest Run Summary — `{benchmark}`")
    lines.append("")
    lines.append(f"- Report: `{report_path.as_posix()}`")
    lines.append(f"- Best step: `{best_step}`")
    lines.append("")
    lines.append("## Best Candidate")
    lines.append("")
    for k in sorted(best_candidate.keys()):
        lines.append(f"- **{k}**: `{best_candidate[k]}`")
    lines.append("")
    lines.append("## Best Score")
    lines.append("")
    lines.append(f"- **quality**: `{_fmt_float(best_score.get('quality'))}`")
    lines.append(f"- **latency_ms**: `{_fmt_float(best_score.get('latency_ms'))}`")
    lines.append(f"- **governance_ok**: `{best_score.get('governance_ok')}`")
    total = best_score.get("total", best_total)
    lines.append(f"- **total**: `{_fmt_float(total)}`")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- This demo accepts candidate changes only when evaluator metrics improve.")
    lines.append("- Governance gates can fail a candidate (e.g., bounds or latency budget).")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    import argparse

    p = argparse.ArgumentParser(description="Write a one-page markdown summary for a run report JSON.")
    p.add_argument("--report", required=True, help="Path to report JSON")
    p.add_argument("--out", default="run_reports/latest_summary.md", help="Output markdown path")
    args = p.parse_args()

    summarize(Path(args.report), Path(args.out))
    print(f"Wrote summary: {Path(args.out).resolve()}")


if __name__ == "__main__":
    main()
