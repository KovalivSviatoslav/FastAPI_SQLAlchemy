from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from components.post.elastic import PostIndexService
from components.post.services import PostService
from config.db import engine
from config.elastic import es_client
from config.app import AppConfig
from components.user.views import user_router
from components.post.views import post_router
from components.comment.views import comment_router
from components.rating.views import rating_router
from components.user.models import User
from components.post.models import Post, Category
from components.comment.models import Comment
from components.rating.models import Rating

app = FastAPI(title=AppConfig().title, version=AppConfig().version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=AppConfig().cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(rating_router)


@app.on_event("startup")
async def init_indices():
    await PostIndexService().init_index()


@app.on_event("startup")
@repeat_every(seconds=3600, wait_first=True, raise_exceptions=True)
async def calculate_ratings() -> None:
    async with AsyncSession(engine) as session:
        await PostService(session).get_avg_rating()


@app.on_event("shutdown")
async def app_shutdown():
    await es_client.close()
