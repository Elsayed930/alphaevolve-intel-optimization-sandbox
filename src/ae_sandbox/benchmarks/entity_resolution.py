from __future__ import annotations

import time
import numpy as np

from ae_sandbox.benchmarks.types import Candidate, Score, Benchmark
from ae_sandbox.governance.budgets import Budgets, within_latency_budget


def _normalize(s: str) -> str:
    return "".join(ch.lower() for ch in s if ch.isalnum() or ch.isspace()).strip()


def _jaccard_char_ngrams(a: str, b: str, n: int = 3) -> float:
    a = _normalize(a)
    b = _normalize(b)
    if len(a) < n or len(b) < n:
        return 0.0
    A = {a[i : i + n] for i in range(len(a) - n + 1)}
    B = {b[i : i + n] for i in range(len(b) - n + 1)}
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


class EntityResolutionBenchmark(Benchmark):
    """
    Synthetic entity resolution / watchlisting-style benchmark.

    Goal:
      - Given pairs of records, predict match vs non-match
      - Candidate controls a similarity threshold
      - Evaluator scores F1 (quality) with latency + governance gates
    """

    name = "entity_resolution"

    def __init__(self) -> None:
        # Build a synthetic dataset of positive/negative pairs
        rng = np.random.default_rng(42)

        base_names = [
            "Michael McKeever",
            "John A Smith",
            "Sara Johnson",
            "Alejandro Martinez",
            "Wei Chen",
            "Fatima Al Zahra",
            "Omar Hassan",
            "Elena Petrova",
            "David Nguyen",
            "Priya Raman",
        ]

        def mutate(name: str) -> str:
            # simple synthetic noise: swap tokens, drop chars, add punctuation
            tokens = name.split()
            if rng.random() < 0.4 and len(tokens) >= 2:
                tokens[0], tokens[-1] = tokens[-1], tokens[0]
            s = " ".join(tokens)
            if rng.random() < 0.5 and len(s) > 6:
                idx = int(rng.integers(1, len(s) - 1))
                s = s[:idx] + s[idx + 1 :]
            if rng.random() < 0.4:
                s = s.replace(" ", "-")
            return s

        pairs = []
        labels = []

        # positives: base vs mutated
        for name in base_names:
            for _ in range(30):
                pairs.append((name, mutate(name)))
                labels.append(1)

        # negatives: random different names
        for _ in range(300):
            a, b = rng.choice(base_names, size=2, replace=False)
            pairs.append((a, mutate(b)))
            labels.append(0)

        self.pairs = pairs
        self.labels = np.array(labels, dtype=int)

    def initial_candidate(self) -> Candidate:
        return Candidate(params={"threshold": 0.55, "ngram_n": 3})

    def propose(self, base: Candidate, rng_seed: int) -> Candidate:
        rng = np.random.default_rng(rng_seed)
        thr = float(base.params["threshold"])
        thr = float(np.clip(thr + float(rng.normal(0, 0.03)), 0.30, 0.90))
        n = int(base.params["ngram_n"])
        # keep n small and stable in demo
        n = int(np.clip(n + int(rng.integers(-1, 2)), 2, 4))
        return Candidate(params={"threshold": thr, "ngram_n": n})

    def evaluate(self, cand: Candidate) -> Score:
        threshold = float(cand.params["threshold"])
        n = int(cand.params["ngram_n"])

        # Governance gate: keep candidate within bounds
        ok_params = (0.30 <= threshold <= 0.90) and (2 <= n <= 4)

        start = time.perf_counter()

        # Predict matches
        preds = []
        for (a, b) in self.pairs:
            sim = _jaccard_char_ngrams(a, b, n=n)
            preds.append(1 if sim >= threshold else 0)

        latency_ms = (time.perf_counter() - start) * 1000.0

        # Compute precision/recall/f1
        preds = np.array(preds, dtype=int)
        tp = int(((preds == 1) & (self.labels == 1)).sum())
        fp = int(((preds == 1) & (self.labels == 0)).sum())
        fn = int(((preds == 0) & (self.labels == 1)).sum())

        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

        # Latency budget gate (demo)
        ok = ok_params and within_latency_budget(latency_ms, Budgets(max_latency_ms=80.0))

        return Score(quality=float(f1), latency_ms=float(latency_ms), governance_ok=ok)
