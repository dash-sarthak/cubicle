"""OpenAI wrapper: spec call, implement/test tool loops, token accounting."""

import json
from pathlib import Path
from typing import Any, cast

from openai import OpenAI
from openai.types.chat import (
  ChatCompletionMessageFunctionToolCall,
  ChatCompletionMessageParam,
  ChatCompletionToolParam,
)

from cubicle.models import Issue, Spec

MAX_TOOL_ITERATIONS = 30

FILE_TOOLS: list[ChatCompletionToolParam] = [
  {
    "type": "function",
    "function": {
      "name": "write_file",
      "description": "Write text to a file inside the repo, overwriting it.",
      "parameters": {
        "type": "object",
        "properties": {
          "path": {"type": "string"},
          "content": {"type": "string"},
        },
        "required": ["path", "content"],
      },
    },
  },
  {
    "type": "function",
    "function": {
      "name": "read_file",
      "description": "Read a text file inside the repo.",
      "parameters": {
        "type": "object",
        "properties": {"path": {"type": "string"}},
        "required": ["path"],
      },
    },
  },
  {
    "type": "function",
    "function": {
      "name": "list_files",
      "description": "List every file in the repo.",
      "parameters": {"type": "object", "properties": {}},
    },
  },
]


class LLM:
  """Produces a spec from an issue, implements changes in a
  worktree, and writes tests — the three stage behaviors."""

  def __init__(self, api_key: str, model: str, client: Any = None):
    self.model = model
    self.total_tokens = 0
    # ponytail: client is the injected OpenAI-compatible transport
    # (tests pass a stub); a Protocol is overkill for one seam.
    self._client = client or OpenAI(api_key=api_key)

  def spec(self, issue: Issue, file_tree: str) -> Spec:
    """One structured-output call: issue + file tree -> Spec."""
    completion = self._client.chat.completions.parse(
      model=self.model,
      messages=[
        {
          "role": "user",
          "content": (
            f"Issue #{issue.number}: {issue.title}\n\n{issue.body}\n\n"
            f"Repo files:\n{file_tree}\n\n"
            "Write the spec: one-paragraph summary and the files to touch."
          ),
        }
      ],
      response_format=Spec,
    )
    self.total_tokens += (
      completion.usage.total_tokens if completion.usage else 0
    )
    spec = completion.choices[0].message.parsed
    if spec is None:
      raise ValueError("spec call returned no parsed spec")
    return spec

  def implement(self, worktree: Path, spec: Spec) -> None:
    """Tool loop: turn the spec into files inside the worktree."""
    self._tool_loop(
      worktree,
      f"Implement this change in the repo: {spec.summary} "
      f"(files to touch: {', '.join(spec.files) or 'your call'}).",
    )

  def write_tests(self, worktree: Path, spec: Spec) -> None:
    """Tool loop: write the test suite for the spec'd change."""
    self._tool_loop(
      worktree,
      f"Write pytest tests covering this change: {spec.summary} "
      f"(files: {', '.join(spec.files) or 'your call'}).",
    )

  def _tool_loop(self, worktree: Path, instruction: str) -> None:
    """Capped file-tool loop; every file op stays inside the worktree."""
    messages: list[ChatCompletionMessageParam] = [
      {
        "role": "system",
        "content": (
          "You change the repo only through the file tools. "
          "When done, reply with a one-sentence summary and no tools."
        ),
      },
      {"role": "user", "content": instruction},
    ]
    for _ in range(MAX_TOOL_ITERATIONS):
      response = self._client.chat.completions.create(
        model=self.model,
        messages=messages,
        tools=FILE_TOOLS,
      )
      self.total_tokens += response.usage.total_tokens if response.usage else 0
      message = response.choices[0].message
      if not message.tool_calls:
        return
      messages.append(
        cast(
          ChatCompletionMessageParam,
          message.model_dump(exclude_none=True),
        )
      )
      for call in message.tool_calls:
        if not isinstance(call, ChatCompletionMessageFunctionToolCall):
          result = "error: unsupported tool call type"
        else:
          result = _apply_tool(
            worktree, call.function.name, call.function.arguments
          )
        messages.append(
          {"role": "tool", "tool_call_id": call.id, "content": result}
        )
    raise RuntimeError(f"tool loop exceeded {MAX_TOOL_ITERATIONS} iterations")


def _apply_tool(worktree: Path, name: str, arguments: str) -> str:
  """Run one file tool; returns the tool result text (errors included
  so the model can self-correct). Paths must resolve inside the repo."""
  root = worktree.resolve()
  try:
    args = json.loads(arguments)
  except json.JSONDecodeError:
    return "error: arguments were not valid JSON"
  path_arg = args.get("path")
  if name in ("write_file", "read_file"):
    if not isinstance(path_arg, str):
      return "error: path must be a string"
    target = (root / path_arg).resolve()
    if not target.is_relative_to(root):
      return "error: path escapes the repo"
    if name == "write_file":
      target.parent.mkdir(parents=True, exist_ok=True)
      target.write_text(args.get("content") or "")
      return "ok"
    if not target.exists():
      return "error: no such file"
    return target.read_text()
  if name == "list_files":
    return (
      "\n".join(
        sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())
      )
      or "(empty)"
    )
  return f"error: unknown tool {name}"
