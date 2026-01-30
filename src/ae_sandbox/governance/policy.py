from __future__ import annotations
from ae_sandbox.benchmarks.types import Candidate

def governance_check(cand: Candidate) -> bool:
    k = int(cand.params.get("k", 0))
    n_init = int(cand.params.get("n_init", 0))
    max_iter = int(cand.params.get("max_iter", 0))
    return (2 <= k <= 8) and (5 <= n_init <= 30) and (50 <= max_iter <= 400)
