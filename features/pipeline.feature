Feature: Core loop
  Cubicle turns a repo issue into a gated PR.
  Loop: repo -> spec -> implement -> test -> tiered gate -> merged PR.

  Scenario: Configuration loads from the environment
    Given a .env with GITHUB_PAT, OPENAI_API_KEY and CUBICLE_MODEL
    When the config is loaded
    Then the config exposes all three values

  Scenario: An issue becomes a gated PR
    Given a target repo with issue 42
    And fake OpenAI and GitHub services
    When the pipeline runs
    Then a branch cubicle/issue-42 is pushed
    And a PR is opened whose body contains the spec summary and the test output
