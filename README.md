# AlphaEvolve Intelligence Optimization Sandbox

A public **mission-oriented optimization sandbox** inspired by AlphaEvolve-style workflows, demonstrating how AI systems can propose algorithmic changes **only when evaluator metrics improve**.

This project is designed as a safe, unclassified portfolio artifact for **Intelligence Community mission engineering**, focused on:

- Evaluator-driven optimization loops  
- Governance + latency budget enforcement  
- Benchmarks aligned to analytic workflows (clustering + watchlisting/entity resolution)  
- Auditable run artifacts + one-page summaries  
- CI-backed reproducibility  

> **Note:** This is a simulation of evaluator-governed optimization principles — **not** Google/DeepMind source code.

---

## Why this matters (IC / Mission Engineering relevance)

In intelligence and national security environments, optimization is not simply “higher accuracy.”

Candidate algorithm changes must also satisfy:

- Mission performance constraints (**latency budgets**)  
- Governance bounds (**safe parameter ranges**)  
- Repeatability + auditability  
- Operational acceptance criteria  

This sandbox demonstrates that evaluator-first delivery pattern in a transparent and reproducible framework.

---

## Core idea: evaluator-governed optimization

The optimization loop follows a mission-style structure:

1. Start with a baseline candidate configuration  
2. Propose small controlled variations  
3. Evaluate candidates using mission metrics  
4. Accept changes **only when quality improves** *and* governance constraints hold  
5. Produce an auditable JSON report + summary artifact  

---

## Benchmarks included

### ✅ Toy clustering benchmark (`toy_clustering`)

Optimizes clustering configuration (KMeans parameters) under governance constraints.

- Quality proxy: inertia-based score  
- Constraints: bounded parameters + latency budget  

### ✅ Entity resolution / watchlisting benchmark (`entity_resolution`)

Simulates identity matching workflows relevant to:

- watchlisting  
- alias resolution  
- record linkage  
- analytic triage  

Features:

- synthetic alias/noise generation  
- similarity threshold evolution  
- F1 quality scoring + latency gating  

---

## Governance + mission constraints

The sandbox enforces lightweight governance gates:

- parameter bounds (safe ranges)  
- latency budgets (mission performance requirement)  
- fail-fast rejection for noncompliant candidates  

This mimics real-world delivery where optimization must remain operationally safe.

---

## Quickstart (Windows)

### 1) Create environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

