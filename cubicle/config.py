"""Configuration loaded from a .env file — the BYOK seam.

Every run needs exactly three secrets/values. Missing keys must fail loudly,
listing all of them: partial config is worse than no config.
"""

from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

REQUIRED = ("GITHUB_PAT", "OPENAI_API_KEY", "CUBICLE_MODEL")


@dataclass(frozen=True)
class Config:
  github_pat: str
  openai_api_key: str
  model: str


def load(env_path: Path) -> Config:
  """Parse an env file into a Config; raise listing every missing key."""
  values = {key: value for key in REQUIRED if (value := dotenv_values(env_path).get(key))}
  missing = [key for key in REQUIRED if key not in values]
  if missing:
    raise ValueError(f"missing required config: {', '.join(missing)} (in {env_path})")
  return Config(
    github_pat=values["GITHUB_PAT"],
    openai_api_key=values["OPENAI_API_KEY"],
    model=values["CUBICLE_MODEL"],
  )
