from datetime import date
from typing import Optional, List

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
                    "name": {
                        "type": "text"
                    },
                    "body": {
                        "type": "text"
                    },
                    "category": {
                        "type": "keyword"
                    },
                    "created_at": {
                        "type": "date"
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
        document = self._prepare_document(post)
        await self._client.create(
            index=self.INDEX_NAME,
            id=post.id,
            document=document
        )

    async def update_doc(self, post: Post) -> None:
        document = self._prepare_document(post)
        await self._client.update(
            index=self.INDEX_NAME,
            id=post.id,
            doc=document
        )

    async def delete_doc(self, post: Post) -> None:
        await self._client.delete(
            index=self.INDEX_NAME,
            id=post.id
        )

    async def search(
            self,
            search: Optional[str],
            category: Optional[str],
            start_date: Optional[date],
            end_date: Optional[date]
    ):
        query = self._build_search_query(search, category, start_date, end_date)
        response = await es_client.search(
            index=self.INDEX_NAME,
            query=query,
            filter_path=(
                'hits.hits._id',
                'hits.hits._source',
            )
        )
        return response['hits']['hits'] if response else []

    async def get_categories_rate(self):
        response = await es_client.search(
            index=self.INDEX_NAME,
            aggs={
                    "popular_category": {
                        "terms": {
                            "field": "category",
                            "size": 10
                        }
                    }
                },
            size=0,
            filter_path=(
                'aggregations.popular_category.buckets',
            )
        )
        return response['aggregations']['popular_category']['buckets']

    def _build_search_query(
            self,
            search: Optional[str],
            category: Optional[str],
            start_date: Optional[date],
            end_date: Optional[date]
    ):
        if any((search, category, start_date, end_date)):
            query = {
                "bool": dict()
            }
            if search:
                query['bool']['must'] = {
                    "multi_match": {
                        "query": search,
                        "fields": [
                            "name",
                            "body"
                        ]
                    },
                }

            if any((category, start_date, end_date)):
                query['bool']['filter'] = self._get_bool_filter(category, start_date, end_date)

            return query

    @staticmethod
    def _get_bool_filter(
            category: Optional[str], start_date: Optional[date], end_date: Optional[date]
    ) -> List[dict]:
        bool_filter = list()

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

        if category:
            bool_filter.append({
                "term": {
                    "category": category
                }
            })

        return bool_filter

    @staticmethod
    def _prepare_document(post: Post):
        document = post.dict(
            exclude={
                'id',
                'user_id',
                'category_id',
                'avg_rating',
                "updated_at",
            }
        )
        document["category"] = post.category.name
        return document
