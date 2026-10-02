from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any

from app.services.library_service import LibraryService
from app.services.comic_service import comic_service
from app.services.image_service import image_service


# ============================================================
# COMICCRAFT API ROUTER
# ============================================================

router = APIRouter(
    prefix="/api",
    tags=["ComicCraft"]
)

library_service = LibraryService(comic_service)


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "ComicCraft Backend",
        "message": "ComicCraft API is running"
    }


# ============================================================
# CREATE COMIC
# ============================================================

@router.post("/comics")
def create_comic(data: Dict[str, Any]):

    try:

        comic = comic_service.create_comic(

            prompt=data.get("prompt", ""),

            character=data.get(
                "character",
                ""
            ),

            setting=data.get(
                "setting",
                ""
            ),

            genre=data.get(
                "genre",
                "Adventure"
            ),

            mood=data.get(
                "mood",
                "Exciting"
            ),

            art_style=data.get(
                "art_style",
                "Comic"
            ),

            language=data.get(
                "language",
                "English"
            ),

            panel_count=data.get(
                "panel_count",
                5
            )
        )

        return {
            "success": True,
            "message": "Comic created successfully",
            "comic": comic
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        print(
            "COMIC CREATION ERROR:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# GET SINGLE COMIC
# ============================================================

@router.get("/comics/{comic_id}")
def get_comic(comic_id: str):

    try:

        comic = comic_service.get_comic(
            comic_id
        )

        if comic is None:

            raise HTTPException(
                status_code=404,
                detail="Comic not found"
            )

        return {
            "success": True,
            "comic": comic
        }

    except HTTPException:
        raise

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


# ============================================================
# UPDATE COMIC
# ============================================================

@router.put("/comics/{comic_id}")
def update_comic(
    comic_id: str,
    data: Dict[str, Any]
):

    try:

        comic = comic_service.update_comic(
            comic_id,
            **data
        )

        return {
            "success": True,
            "message": "Comic updated successfully",
            "comic": comic
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# DELETE COMIC
# ============================================================

@router.delete("/comics/{comic_id}")
def delete_comic(comic_id: str):

    try:

        deleted = comic_service.delete_comic(
            comic_id
        )

        if not deleted:

            raise HTTPException(
                status_code=404,
                detail="Comic not found"
            )

        return {
            "success": True,
            "message": "Comic deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as error:

        print(
            "DELETE COMIC ERROR:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to delete comic"
        )


# ============================================================
# UPDATE CHARACTER
# ============================================================

@router.put("/comics/{comic_id}/character")
def update_character(
    comic_id: str,
    data: Dict[str, Any]
):

    try:

        character = comic_service.update_character(

            comic_id,

            name=data.get("name"),

            description=data.get(
                "description"
            ),

            appearance=data.get(
                "appearance"
            ),

            personality=data.get(
                "personality"
            ),

            role=data.get("role")
        )

        return {
            "success": True,
            "message": "Character updated",
            "character": character
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# ADD PANEL
# ============================================================

@router.post("/comics/{comic_id}/panels")
def add_panel(
    comic_id: str,
    data: Dict[str, Any]
):

    try:

        panel = comic_service.add_panel(

            comic_id,

            panel_number=data.get(
                "panel_number"
            ),

            title=data.get(
                "title",
                ""
            ),

            scene_description=data.get(
                "scene_description",
                ""
            ),

            narration=data.get(
                "narration",
                ""
            ),

            dialogue=data.get(
                "dialogue",
                ""
            ),

            image_prompt=data.get(
                "image_prompt",
                ""
            ),

            image_path=data.get(
                "image_path"
            )
        )

        return {
            "success": True,
            "message": "Panel added",
            "panel": panel
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# UPDATE PANEL
# ============================================================

@router.put(
    "/comics/{comic_id}/panels/{panel_number}"
)
def update_panel(
    comic_id: str,
    panel_number: int,
    data: Dict[str, Any]
):

    try:

        panel = comic_service.update_panel(

            comic_id,
            panel_number,
            **data
        )

        return {
            "success": True,
            "message": "Panel updated",
            "panel": panel
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


# ============================================================
# DELETE PANEL
# ============================================================

@router.delete(
    "/comics/{comic_id}/panels/{panel_number}"
)
def delete_panel(
    comic_id: str,
    panel_number: int
):

    try:

        comic_service.delete_panel(
            comic_id,
            panel_number
        )

        return {
            "success": True,
            "message": "Panel deleted"
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


# ============================================================
# REGENERATE PANEL
# ============================================================

@router.post(
    "/comics/{comic_id}/panels/{panel_number}/regenerate"
)
def regenerate_panel(
    comic_id: str,
    panel_number: int,
    data: Optional[Dict[str, Any]] = None
):

    data = data or {}

    try:

        panel = comic_service.request_panel_regeneration(

            comic_id,

            panel_number,

            reason=data.get(
                "reason",
                ""
            )
        )

        return {
            "success": True,
            "message": "Panel regeneration requested",
            "panel": panel
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


# ============================================================
# GENERATE ONE PANEL IMAGE
# ============================================================

@router.post(
    "/comics/{comic_id}/panels/{panel_number}/generate-image"
)
def generate_panel_image(
    comic_id: str,
    panel_number: int
):

    try:

        result = image_service.generate_panel_image(

            comic_id,

            panel_number
        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except Exception as error:

        print(
            "IMAGE GENERATION ERROR:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# GENERATE ALL PANEL IMAGES
# ============================================================

@router.post(
    "/comics/{comic_id}/generate-images"
)
def generate_all_images(
    comic_id: str
):

    try:

        comic = comic_service.get_comic(
            comic_id
        )

        if comic is None:

            raise ValueError(
                "Comic not found"
            )

        results = []

        for panel in comic.get(
            "panels",
            []
        ):

            panel_number = panel.get(
                "panel_number"
            )

            if panel_number is None:
                continue

            result = image_service.generate_panel_image(

                comic_id,

                panel_number
            )

            results.append(result)

        return {

            "success": True,

            "message":
                "All panel images generated successfully",

            "count":
                len(results),

            "results":
                results
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except Exception as error:

        print(
            "ALL IMAGE GENERATION ERROR:",
            repr(error)
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ============================================================
# STORY IMPROVEMENT
# ============================================================

@router.post(
    "/comics/{comic_id}/improve"
)
def improve_story(
    comic_id: str,
    data: Dict[str, Any]
):

    improvement_type = data.get(
        "type",
        "improve"
    )

    try:

        request = (
            comic_service
            .request_story_improvement(
                comic_id,
                improvement_type
            )
        )

        return {
            "success": True,
            "message":
                "Story improvement requested",
            "request":
                request
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# QUALITY CHECKER
# ============================================================

@router.post(
    "/comics/{comic_id}/quality"
)
def save_quality_report(
    comic_id: str,
    report: Dict[str, Any]
):

    try:

        result = (
            comic_service
            .save_quality_report(
                comic_id,
                report
            )
        )

        return {
            "success": True,
            "message":
                "Quality report saved",
            "quality_report":
                result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


# ============================================================
# CONTINUE STORY
# ============================================================

@router.post(
    "/comics/{comic_id}/continue"
)
def continue_story(
    comic_id: str,
    data: Dict[str, Any]
):

    try:

        request = (
            comic_service
            .continue_story(
                comic_id,
                data.get(
                    "instruction",
                    ""
                )
            )
        )

        return {
            "success": True,
            "message":
                "Story continuation requested",
            "request":
                request
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# STORY BRANCHING
# ============================================================

@router.post(
    "/comics/{comic_id}/branches"
)
def create_branch(
    comic_id: str,
    data: Dict[str, Any]
):

    try:

        branch = (
            comic_service
            .create_story_branch(

                comic_id,

                data.get(
                    "branch_title",
                    ""
                ),

                data.get(
                    "decision",
                    ""
                )
            )
        )

        return {
            "success": True,
            "message":
                "Story branch created",
            "branch":
                branch
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# COMPLETE COMIC
# ============================================================

@router.post(
    "/comics/{comic_id}/complete"
)
def complete_comic(
    comic_id: str
):

    try:

        comic = (
            comic_service
            .complete_comic(
                comic_id
            )
        )

        return {
            "success": True,
            "message":
                "Comic completed",
            "comic":
                comic
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


# ============================================================
# SAVE TO LIBRARY
# ============================================================

@router.post(
    "/library/{comic_id}"
)
def save_to_library(
    comic_id: str
):

    comic = library_service.save_comic(
        comic_id
    )

    if comic is None:

        raise HTTPException(
            status_code=404,
            detail="Comic not found"
        )

    return {
        "success": True,
        "message":
            "Comic saved to library",
        "comic":
            comic
    }


# ============================================================
# GET LIBRARY COMIC
# ============================================================

@router.get(
    "/library/{comic_id}"
)
def get_library_comic(
    comic_id: str
):

    comic = library_service.get_comic(
        comic_id
    )

    if comic is None:

        raise HTTPException(
            status_code=404,
            detail="Comic not found in library"
        )

    return {
        "success": True,
        "comic":
            comic
    }


# ============================================================
# SEARCH LIBRARY
# ============================================================

@router.get("/library")
def search_library(

    keyword: str = Query(
        "",
        max_length=100
    ),

    status: Optional[str] = Query(
        None,
        max_length=30
    ),

    genre: Optional[str] = Query(
        None,
        max_length=50
    )
):

    try:

        comics = library_service.search_library(

            keyword=keyword,

            status=status,

            genre=genre
        )

        return {

            "success": True,

            "count":
                len(comics),

            "comics":
                comics
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


# ============================================================
# VERSION HISTORY
# ============================================================

@router.get(
    "/comics/{comic_id}/versions"
)
def get_versions(
    comic_id: str
):

    try:

        versions = (
            comic_service
            .get_versions(
                comic_id
            )
        )

        return {

            "success": True,

            "versions":
                versions
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


# ============================================================
# EXPORT REGISTRATION
# ============================================================

@router.post(
    "/comics/{comic_id}/exports"
)
def register_export(
    comic_id: str,
    data: Dict[str, Any]
):

    try:

        export = (
            comic_service
            .register_export(

                comic_id,

                data.get(
                    "type",
                    ""
                ),

                data.get(
                    "file_path",
                    ""
                )
            )
        )

        return {

            "success": True,

            "message":
                "Export registered",

            "export":
                export
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )