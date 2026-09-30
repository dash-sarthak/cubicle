"""Shared fakes for BDD scenarios. Real services replace these via the same seams."""

import pytest


class FakeGitHub:
  """Records branch pushes and PRs; serves canned issues."""

  def __init__(self):
    self.issues = {
      42: {"number": 42, "title": "Add greeting", "body": "Print a greeting."},
    }
    self.branches = []
    self.prs = []

  def get_issue(self, repo, number):
    return self.issues[number]

  def push_branch(self, repo, branch):
    self.branches.append(branch)

  def open_pr(self, repo, branch, title, body):
    self.prs.append({"branch": branch, "title": title, "body": body})
    return {"number": 1}


class FakeLLM:
  """Canned spec + implementation; stands in for the OpenAI tool loop."""

  def spec(self, issue, file_tree):
    return {"summary": "Print a greeting", "files": ["greet.py"]}

  def implement(self, worktree, spec):
    (worktree / "greet.py").write_text("print('hello')\n")

  def write_tests(self, worktree, spec):
    (worktree / "test_greet.py").write_text("def test_greet():\n  assert True\n")


@pytest.fixture
def fake_github():
  return FakeGitHub()


@pytest.fixture
def fake_llm():
  return FakeLLM()
