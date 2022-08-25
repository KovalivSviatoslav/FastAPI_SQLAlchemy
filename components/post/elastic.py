from datetime import date

from components.post.models import Post
from config.elastic import es_client


class PostIndexService:
    def __init__(self):
        self.INDEX_NAME = 'posts'
        self._client = es_client

    async def init_index(self):
        mapping = {
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
            body=mapping,
            ignore=[400]
        )

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

    async def search(self, search: str, start_date: date, end_date: date):
        query = self._build_search_query(search, start_date, end_date)
        response = await es_client.search(
            index=self.INDEX_NAME,
            query=query,
            filter_path=(
                'hits.hits._id',
                'hits.hits._source',
            )
        )
        return response['hits']['hits'] if response else []

    @staticmethod
    def _build_search_query(search: str, start_date: date, end_date: date):
        if search or start_date or end_date:
            bool_filter = list()
            query = {
                "bool": {
                    "filter": bool_filter
                }
            }

            if search:
                bool_filter.append({
                    "multi_match": {
                        "query": search,
                        "fields": [
                            "name",
                            "body"
                        ]
                    },
                })

            if start_date or end_date:
                created_at = dict()
                if start_date:
                    created_at["gte"] = start_date
                if end_date:
                    created_at["lte"] = end_date

                range_filter = {
                    "range": {
                        "created_at": created_at
                    }
                }
                bool_filter.append(range_filter)

            return query
