"""BDD steps for the core loop. Pipeline scenario is intentionally RED (see PLAN.md)."""

from pytest_bdd import given, scenarios, then, when

from cubicle import config, pipeline

scenarios("pipeline.feature")


# --- Scenario: Configuration loads from the environment --------------------


@given("a .env with GITHUB_PAT, OPENAI_API_KEY and CUBICLE_MODEL", target_fixture="env_file")
def env_file(tmp_path):
  env = tmp_path / ".env"
  env.write_text("GITHUB_PAT=ghp_test\nOPENAI_API_KEY=sk-test\nCUBICLE_MODEL=gpt-test\n")
  return env


@when("the config is loaded", target_fixture="loaded_config")
def loaded_config(env_file):
  return config.load(env_file)


@then("the config exposes all three values")
def config_exposes_values(loaded_config):
  assert loaded_config.github_pat == "ghp_test"
  assert loaded_config.openai_api_key == "sk-test"
  assert loaded_config.model == "gpt-test"


# --- Scenario: An issue becomes a gated PR ---------------------------------


@given("a target repo with issue 42", target_fixture="target_repo")
def target_repo(tmp_path):
  repo = tmp_path / "repo"
  repo.mkdir()
  return repo


@given("fake OpenAI and GitHub services", target_fixture="fakes")
def fakes(fake_github, fake_llm):
  return {"github": fake_github, "llm": fake_llm}


@when("the pipeline runs", target_fixture="run_pipeline")
def run_pipeline(target_repo, fakes):
  return pipeline.run(target_repo, 42, **fakes)


@then("a branch cubicle/issue-42 is pushed")
def branch_pushed(fakes):
  assert "cubicle/issue-42" in fakes["github"].branches


@then("a PR is opened whose body contains the spec summary and the test output")
def pr_body_has_spec_and_tests(fakes):
  pr = fakes["github"].prs[0]
  assert "Print a greeting" in pr["body"]
  assert "1 passed" in pr["body"]
