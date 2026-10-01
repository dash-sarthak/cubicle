"""`cubicle run --repo owner/name --issue 42` -> gated PR."""

import argparse
import sys
from pathlib import Path

import httpx

from cubicle import config, github


def main(
  argv: list[str] | None = None,
  *,
  transport: httpx.BaseTransport | None = None,
) -> None:
  """Run the loop for one issue. `transport` injects the HTTP layer
  for tests."""
  parser = argparse.ArgumentParser(prog="cubicle")
  sub = parser.add_subparsers(dest="command", required=True)
  run_parser = sub.add_parser("run", help="issue in -> gated PR out")
  run_parser.add_argument("--repo", required=True, help="owner/name")
  run_parser.add_argument("--issue", type=int, required=True)
  args = parser.parse_args(argv)

  settings = config.load(Path(".env"))
  client = github.GitHubClient(settings.github_pat, args.repo, transport)
  issue = client.get_issue(args.issue)
  print(f"#{issue.number} {issue.title}")
  sys.exit(
    "cubicle: stopping before spec — pipeline wiring is build order"
    " step 4 (PLAN.md)"
  )
