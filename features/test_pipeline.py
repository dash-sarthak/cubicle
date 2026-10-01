"""BDD steps for the core loop. Pipeline scenario: intentionally RED."""

from pathlib import Path
from typing import Any

import httpx
import pytest
from conftest import FakeGitHub, FakeLLM
from pytest_bdd import given, scenario, scenarios, then, when

from cubicle import cli, config, pipeline
from cubicle.github import GitHubClient
from cubicle.models import Issue

scenarios("pipeline.feature")


@scenario("pipeline.feature", "An issue becomes a gated PR")
def test_an_issue_becomes_a_gated_pr() -> None:
  """The core loop: issue in, gated PR out."""


@given(
  "a .env with GITHUB_PAT, OPENAI_API_KEY and CUBICLE_MODEL",
  target_fixture="env_file",
)
def env_file(tmp_path: Path) -> Path:
  env = tmp_path / ".env"
  env.write_text(
    "GITHUB_PAT=ghp_test\nOPENAI_API_KEY=sk-test\nCUBICLE_MODEL=gpt-test\n"
  )
  return env


@when("the config is loaded", target_fixture="loaded_config")
def loaded_config(env_file: Path) -> config.Config:
  return config.load(env_file)


@then("the config exposes all three values")
def config_exposes_values(loaded_config: config.Config) -> None:
  assert loaded_config.github_pat == "ghp_test"
  assert loaded_config.openai_api_key == "sk-test"
  assert loaded_config.model == "gpt-test"


@given("a GitHub API serving issue 42", target_fixture="api")
def api_serving_issue_42(
  github_api: httpx.MockTransport,
) -> httpx.MockTransport:
  return github_api


@when("the issue is fetched", target_fixture="fetched_issue")
def issue_fetched(api: httpx.MockTransport) -> Issue:
  client = GitHubClient(pat="ghp_test", repo="owner/name", transport=api)
  return client.get_issue(42)


@then("the issue is validated with its number, title and body")
def issue_is_validated(fetched_issue: Issue) -> None:
  assert fetched_issue == Issue(
    number=42, title="Add greeting", body="Print a greeting."
  )


@when("cubicle runs for owner/name issue 42", target_fixture="cli_run")
def cli_runs(
  api: httpx.MockTransport,
  env_file: Path,
  monkeypatch: pytest.MonkeyPatch,
  capsys: pytest.CaptureFixture[str],
) -> tuple[object, str]:
  monkeypatch.chdir(env_file.parent)
  with pytest.raises(SystemExit) as stopped:
    cli.main(["run", "--repo", "owner/name", "--issue", "42"], transport=api)
  return stopped.value.code, capsys.readouterr().out


@then("the fetched issue is shown")
def fetched_issue_shown(cli_run: tuple[object, str]) -> None:
  assert "#42 Add greeting" in cli_run[1]


@then("the run stops non-zero naming the stage it stopped before")
def run_stops_non_zero(cli_run: tuple[object, str]) -> None:
  code = cli_run[0]
  assert code != 0
  assert "spec" in str(code)


@given("a target repo with issue 42", target_fixture="target_repo")
def target_repo(tmp_path: Path) -> Path:
  repo = tmp_path / "repo"
  repo.mkdir()
  return repo


@given("fake OpenAI and GitHub services", target_fixture="fakes")
def fakes(fake_github: FakeGitHub, fake_llm: FakeLLM) -> dict[str, Any]:
  return {"github": fake_github, "llm": fake_llm}


@when("the pipeline runs", target_fixture="run_pipeline")
def run_pipeline(target_repo: Path, fakes: dict[str, Any]) -> dict[str, Any]:
  return pipeline.run(target_repo, 42, **fakes)


@then("a branch cubicle/issue-42 is pushed")
def branch_pushed(fakes: dict[str, Any]) -> None:
  github: FakeGitHub = fakes["github"]
  assert "cubicle/issue-42" in github.branches


@then("a PR is opened whose body contains the spec summary and the test output")
def pr_body_has_spec_and_tests(fakes: dict[str, Any]) -> None:
  github: FakeGitHub = fakes["github"]
  pr = github.prs[0]
  assert "Print a greeting" in pr.body
  assert "1 passed" in pr.body
