from datetime import date

from components.post.models import Post
from config.elastic import es_client


class PostIndexService:
    def __init__(self):
        self.INDEX_NAME = 'posts'
        self._client = es_client

    async def init_index(self):
        request_body = {
            "settings": {
                "number_of_shards": 5,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
                    "body": {
                        "type": "text"
                    },
                    "created_at": {
                        "type": "date"
                    },
                    "name": {
                        "type": "text"
                    }
                }
            }
        }
        await self._client.indices.create(
            index=self.INDEX_NAME,
            body=request_body,
            ignore=[400]
        )

    async def search(self, search: str, start_date: date, end_date: date):
        response = await es_client.search(
            index=self.INDEX_NAME,
            query={
                "bool": {
                    "filter": (
                        {
                            "multi_match": {
                                "query": search,
                                "fields": [
                                    "name",
                                    "body"
                                ]
                            },
                        },
                        {
                            "range": {
                                "created_at": {
                                    "gte": start_date,
                                    "lte": end_date
                                }
                            }
                        }

                    )
                }
            },
            filter_path=(
                'hits.hits._id',
                'hits.hits._source',
            )
        )
        return response['hits']['hits'] if response else []

    async def put_doc(self, post: Post) -> None:
        await self._client.create(
            index=self.INDEX_NAME,
            id=post.id,
            document=post.dict(
                exclude={
                    'id',
                    'user_id',
                    'avg_rating'
                }
            )
        )

    async def update_doc(self, post: Post) -> None:
        await self._client.update(
            index=self.INDEX_NAME,
            id=post.id,
            doc=post.dict(
                exclude={
                    'id',
                    'user_id',
                    'avg_rating'
                }
            )
        )

    async def delete_doc(self, post: Post) -> None:
        await self._client.delete(
            index=self.INDEX_NAME,
            id=post.id
        )
