# AlphaEvolve Intelligence Optimization Sandbox

A public, **evaluator-driven algorithm optimization** demo inspired by AlphaEvolve-style workflows. This repo shows how an
AI system can propose candidate changes (algorithms / parameters) and accept them **only when metrics improve**.

> This is a *simulation* of the evaluation loop (not Google/DeepMind code). It is designed to be mission-relevant and safe for public release.

## What this demo does
- Runs optimization loops over **benchmarks** (clustering + anomaly detection examples)
- Uses **evaluator functions** to score candidates (quality, latency proxy, and governance checks)
- Produces a **run report** (JSON) so results are auditable and repeatable

## Quickstart (Windows / PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m ae_sandbox.run --benchmark toy_clustering --steps 25
```

## Repo map
- `src/ae_sandbox/` core library
- `src/ae_sandbox/benchmarks/` toy benchmarks (replace with your own)
- `src/ae_sandbox/optimizers/` candidate proposal + selection loop
- `src/ae_sandbox/governance/` governance checks + traceability
- `tests/` unit tests
- `.github/workflows/` CI (lint + tests)

## Roadmap (suggested)
1. Add a second benchmark: entity resolution (synthetic)
2. Add latency proxy constraints + budgets
3. Add a policy gate: block unsafe transformations
4. Add plotting notebook to visualize score improvements
