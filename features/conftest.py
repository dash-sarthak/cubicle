"""Fakes and fixtures for BDD scenarios.

These fake seams are the contract the real services (OpenAI loop,
GitHubClient) must structurally satisfy. `_`-prefixed params are kept
for signature parity with the real seams; the fakes ignore them.
"""

from pathlib import Path
from typing import Any

import pytest

Issue = dict[str, str | int]


class FakeGitHub:
  """Records branch pushes and PRs; serves canned issues."""

  def __init__(self) -> None:
    self.issues: dict[int, Issue] = {
      42: {"number": 42, "title": "Add greeting", "body": "Print a greeting."},
    }
    self.branches: list[str] = []
    self.prs: list[dict[str, str]] = []

  def get_issue(self, _repo: str, number: int) -> Issue:
    return self.issues[number]

  def push_branch(self, _repo: str, branch: str) -> None:
    self.branches.append(branch)

  def open_pr(self, _repo: str, branch: str, title: str, body: str) -> dict[str, int]:
    self.prs.append({"branch": branch, "title": title, "body": body})
    return {"number": 1}


class FakeLLM:
  """Canned spec + implementation; stands in for the OpenAI tool loop."""

  def spec(self, _issue: Issue, _file_tree: str) -> dict[str, Any]:
    return {"summary": "Print a greeting", "files": ["greet.py"]}

  def implement(self, worktree: Path, _spec: dict[str, Any]) -> None:
    (worktree / "greet.py").write_text("print('hello')\n")

  def write_tests(self, worktree: Path, _spec: dict[str, Any]) -> None:
    (worktree / "test_greet.py").write_text("def test_greet():\n  assert True\n")


@pytest.fixture
def fake_github() -> FakeGitHub:
  return FakeGitHub()


@pytest.fixture
def fake_llm() -> FakeLLM:
  return FakeLLM()
