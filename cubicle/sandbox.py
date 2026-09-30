"""Runs agent-generated code inside Docker; it never executes on the host."""

from pathlib import Path


def run(worktree: Path, image: str, command: str) -> tuple[int, str]:
  """`docker run --rm -v worktree:/src image command` -> (exit_code, output)."""
  raise NotImplementedError("sandbox.run: build order step 3")
