from pathlib import Path
from typing import List

from confz import ConfZ, ConfZFileSource
from pydantic import AnyUrl


CONFIG_DIR = Path(__file__).parent.parent.resolve() / "env_files"


class AppConfig(ConfZ):
    title: str
    version: str

    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    cors_origins: List[AnyUrl]

    CONFIG_SOURCES = ConfZFileSource(file=CONFIG_DIR / "api.yml")
