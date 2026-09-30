"""Seam shapes shared by real services and their fakes."""

from pydantic import BaseModel


class Issue(BaseModel):
  number: int
  title: str
  body: str


class Spec(BaseModel):
  """What the spec stage produces and the implementer builds from."""

  summary: str
  files: list[str]


class PRRecord(BaseModel):
  branch: str
  title: str
  body: str
