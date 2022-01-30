from fastapi import FastAPI
from db.config import init_db
from components.user.models import User
from components.post.models import Post, Rating
from components.comment.models import Comment

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def hello_world():
    return "hello_world"

# https://dbdiagram.io/d/61f53b7085022f4ee50e4469
