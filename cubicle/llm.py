"""OpenAI wrapper: spec call, implement/test tool loops, token accounting."""


class LLM:
  """Produces a spec from an issue, implements changes in a
  worktree, and writes tests — the three stage behaviors."""

  def __init__(self, api_key: str, model: str):
    self.api_key = api_key
    self.model = model
    raise NotImplementedError("LLM: build order step 2")
