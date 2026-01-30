from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ae_sandbox.benchmarks.types import Benchmark, Candidate, Score

@dataclass
class EvolutionResult:
    benchmark: str
    best_candidate: Candidate
    best_score: Score
    history: list[dict[str, Any]]

class EvolutionLoop:
    def __init__(self, benchmark: Benchmark) -> None:
        self.benchmark = benchmark

    def run(self, steps: int = 25, seed: int = 123) -> EvolutionResult:
        best = self.benchmark.initial_candidate()
        best_score = self.benchmark.evaluate(best)
        history: list[dict[str, Any]] = [{
            "step": 0,
            "candidate": best.params,
            "score": {
                "quality": best_score.quality,
                "latency_ms": best_score.latency_ms,
                "governance_ok": best_score.governance_ok,
                "total": best_score.total,
            },
            "best_total": best_score.total,
        }]

        for i in range(1, steps + 1):
            cand = self.benchmark.propose(best, rng_seed=seed + i)
            score = self.benchmark.evaluate(cand)

            if score.total > best_score.total:
                best, best_score = cand, score

            history.append({
                "step": i,
                "candidate": cand.params,
                "score": {
                    "quality": score.quality,
                    "latency_ms": score.latency_ms,
                    "governance_ok": score.governance_ok,
                    "total": score.total,
                },
                "best_total": best_score.total,
            })

        return EvolutionResult(
            benchmark=self.benchmark.name,
            best_candidate=best,
            best_score=best_score,
            history=history,
        )
