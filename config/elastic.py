from pathlib import Path

from confz import ConfZ, ConfZFileSource
from elasticsearch import AsyncElasticsearch

CONFIG_DIR = Path(__file__).parent.parent.resolve() / "env_files"


class ElasticConfig(ConfZ):
    host: str

    CONFIG_SOURCES = ConfZFileSource(file=CONFIG_DIR / "elastic.yml")


es_client = AsyncElasticsearch(ElasticConfig().host)
