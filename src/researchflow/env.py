"""Local environment loading helpers.

ResearchFlow intentionally does not require python-dotenv. This tiny loader
supports ignored local `.env` files while keeping secrets out of the repository.
"""

from __future__ import annotations

import os
from pathlib import Path


def load_local_env(path: Path | None = None) -> None:
    """Load KEY=VALUE pairs from a local .env file without overriding env vars."""

    env_path = path or Path(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().lstrip("\ufeff")
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value
