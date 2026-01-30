from __future__ import annotations

import argparse
from pathlib import Path

from ae_sandbox.optimizers.evolution_loop import EvolutionLoop
from ae_sandbox.benchmarks.registry import get_benchmark
from ae_sandbox.governance.reporting import RunReport


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AlphaEvolve-style evaluator-driven optimization sandbox")
    p.add_argument("--benchmark", default="toy_clustering", help="Benchmark name (see registry)")
    p.add_argument("--steps", type=int, default=25, help="Number of evolution steps")
    p.add_argument("--out", default="run_reports", help="Output folder for JSON reports")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    bench = get_benchmark(args.benchmark)
    loop = EvolutionLoop(benchmark=bench)

    result = loop.run(steps=args.steps)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.benchmark}_report.json"
    RunReport.save(result, out_path)
    print(f"Saved report: {out_path.resolve()}")


if __name__ == "__main__":
    main()
