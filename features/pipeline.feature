Feature: Core loop
  Cubicle turns a repo issue into a gated PR.
  Loop: repo -> spec -> implement -> test -> tiered gate -> merged PR.

  Scenario: Configuration loads from the environment
    Given a .env with GITHUB_PAT, OPENAI_API_KEY and CUBICLE_MODEL
    When the config is loaded
    Then the config exposes all three values

  Scenario: An issue is fetched from the GitHub API
    Given a GitHub API serving issue 42
    When the issue is fetched
    Then the issue is validated with its number, title and body

  Scenario: Run fetches the issue and stops before the next stage
    Given a .env with GITHUB_PAT, OPENAI_API_KEY and CUBICLE_MODEL
    And a GitHub API serving issue 42
    When cubicle runs for owner/name issue 42
    Then the fetched issue is shown
    And the run stops non-zero naming the stage it stopped before

  Scenario: An issue becomes a gated PR
    Given a target repo with issue 42
    And fake OpenAI and GitHub services
    When the pipeline runs
    Then a branch cubicle/issue-42 is pushed
    And a PR is opened whose body contains the spec summary and the test output
