"""Stage agents (spec / implement / test) and their prompts. Prompts live here."""


def spec(llm, issue, file_tree) -> dict:
  raise NotImplementedError("agents.spec: build order step 4")


def implement(llm, worktree, spec) -> None:
  raise NotImplementedError("agents.implement: build order step 2")


def tests(llm, worktree, spec) -> None:
  raise NotImplementedError("agents.tests: build order step 2")
