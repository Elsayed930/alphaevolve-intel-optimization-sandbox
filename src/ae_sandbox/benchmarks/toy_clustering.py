from __future__ import annotations

import time
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

from ae_sandbox.benchmarks.types import Candidate, Score, Benchmark
from ae_sandbox.governance.policy import governance_check

class ToyClusteringBenchmark(Benchmark):
    name = "toy_clustering"

    def __init__(self) -> None:
        self.X, _ = make_blobs(n_samples=800, centers=4, random_state=42, cluster_std=2.2)

    def initial_candidate(self) -> Candidate:
        return Candidate(params={"k": 4, "n_init": 10, "max_iter": 200})

    def propose(self, base: Candidate, rng_seed: int) -> Candidate:
        rng = np.random.default_rng(rng_seed)
        k = int(np.clip(int(base.params["k"]) + int(rng.integers(-1, 2)), 2, 8))
        n_init = int(np.clip(int(base.params["n_init"]) + int(rng.integers(-5, 6)), 5, 30))
        max_iter = int(np.clip(int(base.params["max_iter"]) + int(rng.integers(-50, 51)), 50, 400))
        return Candidate(params={"k": k, "n_init": n_init, "max_iter": max_iter})

    def evaluate(self, cand: Candidate) -> Score:
        ok = governance_check(cand)
        start = time.perf_counter()
        model = KMeans(
            n_clusters=int(cand.params["k"]),
            n_init=int(cand.params["n_init"]),
            max_iter=int(cand.params["max_iter"]),
            random_state=42,
        )
        model.fit(self.X)
        latency_ms = (time.perf_counter() - start) * 1000.0

        # Higher-is-better: convert inertia to bounded score
        quality = float(1.0 / (1.0 + model.inertia_))
        return Score(quality=quality, latency_ms=float(latency_ms), governance_ok=ok)
