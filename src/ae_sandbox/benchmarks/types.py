from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class Candidate:
    params: dict[str, float | int]

@dataclass(frozen=True)
class Score:
    quality: float
    latency_ms: float
    governance_ok: bool

    @property
    def total(self) -> float:
        if not self.governance_ok:
            return float("-inf")
        return self.quality - 0.001 * self.latency_ms

class Benchmark(Protocol):
    name: str
    def initial_candidate(self) -> Candidate: ...
    def propose(self, base: Candidate, rng_seed: int) -> Candidate: ...
    def evaluate(self, cand: Candidate) -> Score: ...
