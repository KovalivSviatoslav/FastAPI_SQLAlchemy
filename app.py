from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def hello_world():
    return "hello_world"

# https://dbdiagram.io/d/61f53b7085022f4ee50e4469
