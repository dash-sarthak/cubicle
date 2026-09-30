"""Docker sandbox — the only place agent-generated code executes (trust boundary)."""

from pathlib import Path


def run(worktree: Path, image: str, command: str) -> tuple[int, str]:
  """`docker run --rm -v worktree:/src image command` -> (exit_code, output)."""
  raise NotImplementedError("sandbox.run: build order step 3")
