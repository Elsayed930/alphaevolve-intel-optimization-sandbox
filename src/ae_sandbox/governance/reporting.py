from __future__ import annotations
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from ae_sandbox.optimizers.evolution_loop import EvolutionResult

class RunReport:
    @staticmethod
    def to_dict(result: EvolutionResult) -> dict[str, Any]:
        return asdict(result)

    @staticmethod
    def save(result: EvolutionResult, path: Path) -> None:
        path.write_text(json.dumps(RunReport.to_dict(result), indent=2), encoding="utf-8")
