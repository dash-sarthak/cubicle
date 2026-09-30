"""Orchestrates the core loop (see PLAN.md): issue in, gated PR out."""

from pathlib import Path
from typing import Any


def run(
  repo: Path, issue_number: int, *, github: Any, llm: Any
) -> dict[str, Any]:
  """Issue in, gated PR out. RED until build order step 2 (see PLAN.md)."""
  raise NotImplementedError(
    "pipeline.run: build order step 2 (tool loop + PR assembly)"
  )
