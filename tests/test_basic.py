from ae_sandbox.benchmarks.registry import get_benchmark
from ae_sandbox.optimizers.evolution_loop import EvolutionLoop

def test_run_produces_history():
    bench = get_benchmark("toy_clustering")
    result = EvolutionLoop(bench).run(steps=5)
    assert result.benchmark == "toy_clustering"
    assert len(result.history) == 6
    assert result.best_score.total == max(h["score"]["total"] for h in result.history)
