"""Fetch issues and open PRs via GitHub REST (PAT auth); clone and
push via the git CLI. Build order step 1."""


class GitHubClient:
  """get_issue / push_branch / open_pr against one repo."""

  def __init__(self, pat: str, repo: str):
    self.pat = pat
    self.repo = repo
    raise NotImplementedError("GitHubClient: build order step 1")
