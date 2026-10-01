"""Orchestrates the core loop (see PLAN.md): issue in, gated PR out."""

import subprocess
import sys
from pathlib import Path
from typing import Any


def run(
  repo: Path, issue_number: int, *, github: Any, llm: Any
) -> dict[str, Any]:
  """Issue in, gated PR out: spec, implement, test, ship."""
  issue = github.get_issue(issue_number)
  # Not a git repo yet -> git ls-files fails; an empty tree is honest.
  tree = (
    subprocess.run(
      ["git", "ls-files"],
      cwd=repo,
      capture_output=True,
      text=True,
      check=False,
    ).stdout
    or ""
  )
  spec = llm.spec(issue, tree)
  llm.implement(repo, spec)
  llm.write_tests(repo, spec)
  passed, output = _run_tests(repo)
  branch = f"cubicle/issue-{issue_number}"
  body = f"{spec.summary}\n\nTest output:\n\n{output}"
  github.push_branch(branch)
  pr = github.open_pr(branch, issue.title, body)
  return {"issue": issue, "spec": spec, "tests_passed": passed, "pr": pr}


def _run_tests(worktree: Path) -> tuple[bool, str]:
  """Run the suite with captured output -> (passed, output)."""
  # ponytail: host pytest; the Docker sandbox (build order step 3)
  # restores the host-never-executes-agent-code rule.
  proc = subprocess.run(
    [sys.executable, "-m", "pytest", "-q"],
    cwd=worktree,
    capture_output=True,
    text=True,
    check=False,
  )
  return proc.returncode == 0, (proc.stdout + proc.stderr).strip()
