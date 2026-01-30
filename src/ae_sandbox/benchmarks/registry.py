from __future__ import annotations

from ae_sandbox.benchmarks.toy_clustering import ToyClusteringBenchmark
from ae_sandbox.benchmarks.types import Benchmark
from ae_sandbox.benchmarks.entity_resolution import EntityResolutionBenchmark

_REGISTRY: dict[str, type[Benchmark]] = {
    "toy_clustering": ToyClusteringBenchmark,
    "entity_resolution": EntityResolutionBenchmark,
}


def get_benchmark(name: str) -> Benchmark:
    if name not in _REGISTRY:
        raise ValueError(f"Unknown benchmark: {name}. Available: {', '.join(sorted(_REGISTRY))}")
    return _REGISTRY[name]()  # type: ignore[call-arg]
