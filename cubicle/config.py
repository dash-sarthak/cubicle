"""Configuration loaded from a team's .env file: their own GitHub
and OpenAI keys plus model choice."""

from pathlib import Path

from dotenv import dotenv_values
from pydantic import BaseModel, Field


class Config(BaseModel):
  github_pat: str = Field(min_length=1, validation_alias="GITHUB_PAT")
  openai_api_key: str = Field(min_length=1, validation_alias="OPENAI_API_KEY")
  model: str = Field(min_length=1, validation_alias="CUBICLE_MODEL")


def load(env_path: Path) -> Config:
  """Parse an env file; missing or blank keys raise ValidationError."""
  return Config.model_validate(dotenv_values(env_path))
