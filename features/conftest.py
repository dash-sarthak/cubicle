"""Fakes standing in for the GitHub and OpenAI services during BDD.

They use the same data shapes as the real services (cubicle.models)
and mirror the real method signatures. Ignored params carry a leading
underscore.
"""

from pathlib import Path

import httpx
import pytest

from cubicle.models import Issue, PRRecord, Spec


class FakeGitHub:
  """Records branch pushes and PRs; serves canned issues."""

  def __init__(self) -> None:
    self.issues: dict[int, Issue] = {
      42: Issue(number=42, title="Add greeting", body="Print a greeting."),
    }
    self.branches: list[str] = []
    self.prs: list[PRRecord] = []

  def get_issue(self, number: int) -> Issue:
    return self.issues[number]

  def push_branch(self, branch: str) -> None:
    self.branches.append(branch)

  def open_pr(self, branch: str, title: str, body: str) -> PRRecord:
    record = PRRecord(branch=branch, title=title, body=body)
    self.prs.append(record)
    return record


class FakeLLM:
  """Canned spec + implementation; stands in for the OpenAI tool loop."""

  def spec(self, _issue: Issue, _file_tree: str) -> Spec:
    return Spec(summary="Print a greeting", files=["greet.py"])

  def implement(self, worktree: Path, _spec: Spec) -> None:
    (worktree / "greet.py").write_text("print('hello')\n")

  def write_tests(self, worktree: Path, _spec: Spec) -> None:
    (worktree / "test_greet.py").write_text(
      "def test_greet():\n  assert True\n"
    )


@pytest.fixture
def fake_github() -> FakeGitHub:
  return FakeGitHub()


@pytest.fixture
def fake_llm() -> FakeLLM:
  return FakeLLM()


@pytest.fixture
def github_api() -> httpx.MockTransport:
  """Fake GitHub REST API: PAT-checked, serves issue 42 for owner/name."""

  def handler(request: httpx.Request) -> httpx.Response:
    if request.headers.get("authorization") != "Bearer ghp_test":
      return httpx.Response(401)
    if request.url.path == "/repos/owner/name/issues/42":
      return httpx.Response(
        200,
        json={
          "number": 42,
          "title": "Add greeting",
          "body": "Print a greeting.",
          "state": "open",
        },
      )
    return httpx.Response(404)

  return httpx.MockTransport(handler)
