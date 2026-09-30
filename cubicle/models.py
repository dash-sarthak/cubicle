"""Data shapes the pipeline passes around: an Issue fetched from
GitHub, a Spec written for the implementer, a PRRecord describing
the pull request the ship stage opens."""

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
