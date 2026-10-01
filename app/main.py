from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="ComicCraft")

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Welcome to ComicCraft!"}