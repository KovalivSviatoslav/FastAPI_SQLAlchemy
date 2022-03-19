from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config.app import AppConfig
from components.user.views import user_router
from components.post.views import post_router
from components.comment.views import comment_router
from components.rating.views import rating_router
from components.user.models import User
from components.post.models import Post
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


# https://dbdiagram.io/d/61f53b7085022f4ee50e4469
# Alembic:
# alembic revision --autogenerate -m "init"
# alembic upgrade head
