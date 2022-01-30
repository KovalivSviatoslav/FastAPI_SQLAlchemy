from fastapi import FastAPI
from components.user.models import User
from components.post.models import Post, Rating
from components.comment.models import Comment

app = FastAPI()


@app.get("/")
async def hello_world():
    return "hello_world"

# https://dbdiagram.io/d/61f53b7085022f4ee50e4469
# Alembic:
# alembic revision --autogenerate -m "init"
# alembic upgrade head
