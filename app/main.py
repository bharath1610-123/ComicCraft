from fastapi import FastAPI

app = FastAPI(title="ComicCraft")

@app.get("/")
def home():
    return {"message": "Welcome to ComicCraft!"}