"""Checks for the LLM file-tool loop: writes land, spend counts,
escape paths are refused, runaway loops cap out."""

from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from openai.types.chat import (
  ChatCompletionMessage,
  ChatCompletionMessageFunctionToolCall,
)
from openai.types.chat.chat_completion_message_tool_call import Function

from cubicle.llm import LLM, MAX_TOOL_ITERATIONS
from cubicle.models import Spec


class StubCompletions:
  """Replays canned create() responses and records the calls."""

  def __init__(self, responses: list[Any]) -> None:
    self.responses = responses
    self.calls: list[Any] = []

  def create(self, **kwargs: Any) -> Any:
    self.calls.append(kwargs)
    return self.responses.pop(0)


def stub_client(completions: StubCompletions) -> SimpleNamespace:
  return SimpleNamespace(chat=SimpleNamespace(completions=completions))


def make_llm(responses: list[Any]) -> tuple[LLM, StubCompletions]:
  completions = StubCompletions(responses)
  llm = LLM("k", "m", client=stub_client(completions))
  return llm, completions


def tool_response(name: str, arguments: str) -> Any:
  call = ChatCompletionMessageFunctionToolCall(
    id="call_1",
    type="function",
    function=Function(name=name, arguments=arguments),
  )
  message = ChatCompletionMessage(
    role="assistant", content=None, tool_calls=[call]
  )
  return SimpleNamespace(
    usage=SimpleNamespace(total_tokens=7),
    choices=[SimpleNamespace(message=message)],
  )


def final_response() -> Any:
  message = ChatCompletionMessage(role="assistant", content="done")
  return SimpleNamespace(
    usage=SimpleNamespace(total_tokens=3),
    choices=[SimpleNamespace(message=message)],
  )


def test_loop_writes_files_and_counts_spend(tmp_path: Path) -> None:
  llm, completions = make_llm(
    [
      tool_response(
        "write_file", '{"path": "greet.py", "content": "print(1)"}'
      ),
      final_response(),
    ]
  )
  llm.implement(tmp_path, Spec(summary="s", files=["greet.py"]))
  assert (tmp_path / "greet.py").read_text() == "print(1)"
  assert llm.total_tokens == 10
  assert completions.calls[0]["tools"]


def test_loop_refuses_paths_outside_the_worktree(tmp_path: Path) -> None:
  llm, _ = make_llm(
    [
      tool_response("write_file", '{"path": "../evil.py"}'),
      final_response(),
    ]
  )
  llm.implement(tmp_path, Spec(summary="s", files=[]))
  assert not (tmp_path.parent / "evil.py").exists()


def test_loop_caps_runaway_tool_use(tmp_path: Path) -> None:
  responses = [
    tool_response("write_file", '{"path": "x.py"}')
    for _ in range(MAX_TOOL_ITERATIONS)
  ]
  llm, _ = make_llm(responses)
  with pytest.raises(RuntimeError, match=str(MAX_TOOL_ITERATIONS)):
    llm.implement(tmp_path, Spec(summary="s", files=[]))
