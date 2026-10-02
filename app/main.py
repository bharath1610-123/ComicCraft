from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import router
from app.services.comic_service import comic_service


app = FastAPI(title="ComicCraft")


# =========================================================
# API ROUTES
# =========================================================

app.include_router(router)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# =========================================================
# GENERATED COMIC IMAGES
# =========================================================

app.mount(
    "/generated",
    StaticFiles(directory="generated"),
    name="generated"
)


# =========================================================
# JINJA2 TEMPLATES
# =========================================================

templates = Jinja2Templates(
    directory="app/templates"
)


# =========================================================
# HOME PAGE
# =========================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to ComicCraft!"
    }


# =========================================================
# LIBRARY PAGE
# =========================================================

@app.get("/library")
def library_page(request: Request):

    from app.services.library_service import LibraryService

    library_service = LibraryService(comic_service)

    comics = library_service.get_all_comics()

    return templates.TemplateResponse(
        request=request,
        name="library.html",
        context={
            "comics": comics
        }
    )


# =========================================================
# COMIC EDITOR PAGE
# =========================================================

@app.get("/comic/{comic_id}/edit")
def edit_comic_page(
    request: Request,
    comic_id: str
):

    comic = comic_service.get_comic(comic_id)

    if comic is None:
        return {
            "error": "Comic not found"
        }

    return templates.TemplateResponse(
        request=request,
        name="editor.html",
        context={
            "comic": comic
        }
    )


# =========================================================
# COMIC PREVIEW PAGE
# =========================================================

@app.get("/comic/{comic_id}")
def comic_preview(
    request: Request,
    comic_id: str
):

    comic = comic_service.get_comic(comic_id)

    if comic is None:
        return {
            "error": "Comic not found"
        }

    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={
            "comic": comic
        }
    )