from pathlib import Path
from typing import Literal, Union

from confz import ConfZ, ConfZFileSource, ConfZEnvSource
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

CONFIG_DIR = Path(__file__).parent.parent.resolve() / "env_files"


class SQLiteDB(ConfZ):
    type: Literal["sqlite"]
    path: Path


class PostgreSQL(ConfZ):
    type: Literal["postgresql"]
    user: str
    password: SecretStr
    host: str
    database: str


DBTypes = Union[SQLiteDB, PostgreSQL]


class DBConfig(ConfZ):
    echo: bool
    db: DBTypes

    CONFIG_SOURCES = [
        ConfZFileSource(
            file=CONFIG_DIR / "dbdev.yml"
        ),
        ConfZEnvSource(allow=[
            "db.user",
            "db.password"
        ])
    ]


def get_db_args(db: DBTypes):
    if isinstance(db, SQLiteDB):
        url = f"sqlite+aiosqlite:///{db.path}"
        args = {"future": True}
    elif isinstance(db, PostgreSQL):
        url = f"postgresql+asyncpg://{db.user}:{db.password.get_secret_value()}@{db.host}/{db.database}"
        args = {}
    else:
        raise ValueError(f"Invalid DB type '{type(db)}'.")

    return url, args


_url, _args = get_db_args(DBConfig().db)
engine = create_async_engine(_url, echo=DBConfig().echo, **_args)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
