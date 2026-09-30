"""OpenAI wrapper: spec call, implement/test tool loops, token accounting."""

from pathlib import Path
from typing import Any


class LLM:
  """The three stage seams: spec, implement, write_tests."""

  def __init__(self, api_key: str, model: str):
    self.api_key = api_key
    self.model = model
    raise NotImplementedError("LLM: build order step 2")


def tool_loop(worktree: Path, tools: dict[str, Any]) -> None:
  """Bounded tool-use loop; the determinism seam. Build order step 2."""
  raise NotImplementedError("tool_loop: build order step 2")
