"""`cubicle run --repo owner/name --issue 42` -> gated PR."""

import argparse


def main(argv: list[str] | None = None) -> None:
  parser = argparse.ArgumentParser(prog="cubicle")
  sub = parser.add_subparsers(dest="command", required=True)
  run_parser = sub.add_parser("run", help="issue in -> gated PR out")
  run_parser.add_argument("--repo", required=True, help="owner/name")
  run_parser.add_argument("--issue", type=int, required=True)
  parser.parse_args(argv)
  raise NotImplementedError("cli wiring: build order step 1")
