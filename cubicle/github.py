"""Fetch issues and open PRs via GitHub REST (PAT auth); clone and
push via the git CLI."""

import httpx

from cubicle.models import Issue

API_ROOT = "https://api.github.com"


class GitHubClient:
  """Fetches issues from one repo. push_branch and open_pr land with
  the ship stage (build order step 4)."""

  def __init__(
    self, pat: str, repo: str, transport: httpx.BaseTransport | None = None
  ) -> None:
    self.repo = repo
    self._client = httpx.Client(
      base_url=API_ROOT,
      headers={
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
      },
      transport=transport,
    )

  def get_issue(self, number: int) -> Issue:
    """Fetch one issue and validate it into the shared Issue shape."""
    response = self._client.get(f"/repos/{self.repo}/issues/{number}")
    response.raise_for_status()
    return Issue.model_validate(response.json())
