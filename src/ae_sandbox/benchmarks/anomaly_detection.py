from __future__ import annotations

import time
import numpy as np

from ae_sandbox.benchmarks.types import Candidate, Score, Benchmark
from ae_sandbox.governance.budgets import Budgets, within_latency_budget


class AnomalyDetectionBenchmark(Benchmark):
    """
    Synthetic rare-event / anomaly detection benchmark.

    Mission analogy:
      - Detect unusual activity spikes or outlier events
      - Candidate controls detection sensitivity (z-score threshold)
      - Evaluator scores F1 under latency + governance constraints
    """

    name = "anomaly_detection"

    def __init__(self) -> None:
        rng = np.random.default_rng(42)

        # Generate baseline "normal" signals
        normal = rng.normal(loc=0.0, scale=1.0, size=1200)

        # Inject rare anomalies (spikes)
        anomalies = rng.normal(loc=6.0, scale=1.0, size=60)

        # Combine dataset
        self.X = np.concatenate([normal, anomalies])
        self.labels = np.concatenate(
            [np.zeros(len(normal), dtype=int), np.ones(len(anomalies), dtype=int)]
        )

        # Shuffle
        idx = rng.permutation(len(self.X))
        self.X = self.X[idx]
        self.labels = self.labels[idx]

    def initial_candidate(self) -> Candidate:
        return Candidate(params={"z_threshold": 3.0})

    def propose(self, base: Candidate, rng_seed: int) -> Candidate:
        rng = np.random.default_rng(rng_seed)
        thr = float(base.params["z_threshold"])
        thr = float(np.clip(thr + float(rng.normal(0, 0.25)), 1.5, 6.0))
        return Candidate(params={"z_threshold": thr})

    def evaluate(self, cand: Candidate) -> Score:
        thr = float(cand.params["z_threshold"])

        # Governance: threshold must remain bounded
        ok_params = 1.5 <= thr <= 6.0

        start = time.perf_counter()

        # Compute z-scores
        mu = float(np.mean(self.X))
        sigma = float(np.std(self.X) + 1e-9)
        z = np.abs((self.X - mu) / sigma)

        # Predict anomaly if above threshold
        preds = (z >= thr).astype(int)

        latency_ms = (time.perf_counter() - start) * 1000.0

        # Compute F1
        tp = int(((preds == 1) & (self.labels == 1)).sum())
        fp = int(((preds == 1) & (self.labels == 0)).sum())
        fn = int(((preds == 0) & (self.labels == 1)).sum())

        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

        # Latency gate (demo)
        ok = ok_params and within_latency_budget(latency_ms, Budgets(max_latency_ms=30.0))

        return Score(quality=float(f1), latency_ms=float(latency_ms), governance_ok=ok)
