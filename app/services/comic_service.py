from typing import Any, Dict, List, Optional
from datetime import datetime
from copy import deepcopy
import uuid


class ComicService:
    """
    Central backend service for ComicCraft.

    Responsibilities:
    - Create and manage comics
    - Manage panels
    - Character information
    - Regeneration requests
    - Story continuation
    - Story improvement requests
    - Quality-check requests
    - Story branching
    - Version history
    - Library search/filter
    """

    MAX_PANELS = 10
    MIN_PANELS = 3

    ALLOWED_STATUS = {
        "draft",
        "generating",
        "completed",
        "failed",
        "archived"
    }

    ALLOWED_GENRES = {
        "Adventure",
        "Comedy",
        "Fantasy",
        "Science Fiction",
        "Mystery",
        "Horror",
        "Romance",
        "Superhero",
        "Drama"
    }

    ALLOWED_MOODS = {
        "Happy",
        "Exciting",
        "Funny",
        "Mysterious",
        "Dramatic",
        "Dark",
        "Romantic",
        "Inspirational"
    }

    ALLOWED_ART_STYLES = {
        "Comic",
        "Anime",
        "Manga",
        "Cartoon",
        "Watercolor",
        "Digital Art",
        "Realistic"
    }

    def __init__(self):

        # Temporary in-memory storage.
        #
        # Later this can be replaced with SQLite/PostgreSQL
        # without changing the API design.
        self.comics: Dict[str, Dict[str, Any]] = {}

    # =========================================================
    # VALIDATION
    # =========================================================

    def _validate_text(
        self,
        value: str,
        field_name: str,
        max_length: int = 2000
    ) -> str:

        if value is None:
            raise ValueError(f"{field_name} is required")

        value = str(value).strip()

        if not value:
            raise ValueError(f"{field_name} cannot be empty")

        if len(value) > max_length:
            raise ValueError(
                f"{field_name} is too long. "
                f"Maximum {max_length} characters allowed."
            )

        return value

    def _validate_options(
        self,
        genre: str,
        mood: str,
        art_style: str
    ):

        if genre not in self.ALLOWED_GENRES:
            raise ValueError(f"Unsupported genre: {genre}")

        if mood not in self.ALLOWED_MOODS:
            raise ValueError(f"Unsupported mood: {mood}")

        if art_style not in self.ALLOWED_ART_STYLES:
            raise ValueError(f"Unsupported art style: {art_style}")

    # =========================================================
    # CREATE COMIC
    # =========================================================

    def create_comic(
        self,
        prompt: str,
        character: str,
        setting: str,
        genre: str = "Adventure",
        mood: str = "Exciting",
        art_style: str = "Comic",
        language: str = "English",
        panel_count: int = 5
    ) -> Dict[str, Any]:

        prompt = self._validate_text(prompt, "Prompt", 3000)
        character = self._validate_text(character, "Character", 500)
        setting = self._validate_text(setting, "Setting", 1000)
        language = self._validate_text(language, "Language", 50)

        self._validate_options(
            genre,
            mood,
            art_style
        )

        if not (
            self.MIN_PANELS
            <= panel_count
            <= self.MAX_PANELS
        ):
            raise ValueError(
                f"Panel count must be between "
                f"{self.MIN_PANELS} and {self.MAX_PANELS}"
            )

        comic_id = str(uuid.uuid4())

        comic = {

            "id": comic_id,

            "created_at":
                datetime.now().isoformat(),

            "updated_at":
                datetime.now().isoformat(),

            "status": "draft",

            "version": 1,

            "input": {

                "prompt": prompt,

                "character": character,

                "setting": setting,

                "genre": genre,

                "mood": mood,

                "art_style": art_style,

                "language": language,

                "panel_count": panel_count
            },

            "character": {

                "name": character,

                "description": "",

                "appearance": "",

                "personality": "",

                "role": "main character"
            },

            "panels": [],

            "versions": [],

            "quality_report": None,

            "branches": [],

            "exports": []
        }

        self.comics[comic_id] = comic

        return deepcopy(comic)

    # =========================================================
    # GET COMIC
    # =========================================================

    def get_comic(
        self,
        comic_id: str
    ) -> Dict[str, Any]:

        comic = self.comics.get(comic_id)

        if comic is None:
            raise ValueError("Comic not found")

        return deepcopy(comic)

    # =========================================================
    # UPDATE COMIC SETTINGS
    # =========================================================

    def update_comic(
        self,
        comic_id: str,
        **updates
    ) -> Dict[str, Any]:

        comic = self._get_internal(comic_id)

        allowed_fields = {
            "prompt",
            "setting",
            "genre",
            "mood",
            "art_style",
            "language",
            "panel_count"
        }

        self._save_version(comic)

        for key, value in updates.items():

            if key not in allowed_fields:
                continue

            if key == "prompt":
                value = self._validate_text(
                    value,
                    "Prompt",
                    3000
                )

            elif key == "setting":
                value = self._validate_text(
                    value,
                    "Setting",
                    1000
                )

            elif key == "language":
                value = self._validate_text(
                    value,
                    "Language",
                    50
                )

            elif key == "genre":
                if value not in self.ALLOWED_GENRES:
                    raise ValueError(
                        f"Unsupported genre: {value}"
                    )

            elif key == "mood":
                if value not in self.ALLOWED_MOODS:
                    raise ValueError(
                        f"Unsupported mood: {value}"
                    )

            elif key == "art_style":
                if value not in self.ALLOWED_ART_STYLES:
                    raise ValueError(
                        f"Unsupported art style: {value}"
                    )

            elif key == "panel_count":

                if not (
                    self.MIN_PANELS
                    <= value
                    <= self.MAX_PANELS
                ):
                    raise ValueError(
                        "Invalid panel count"
                    )

            comic["input"][key] = value

        comic["version"] += 1

        self._touch(comic)

        return deepcopy(comic)

    # =========================================================
    # CHARACTER MANAGEMENT
    # =========================================================

    def update_character(
        self,
        comic_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        appearance: Optional[str] = None,
        personality: Optional[str] = None,
        role: Optional[str] = None
    ) -> Dict[str, Any]:

        comic = self._get_internal(comic_id)

        self._save_version(comic)

        character = comic["character"]

        if name is not None:
            character["name"] = self._validate_text(
                name,
                "Character name",
                100
            )

        if description is not None:
            character["description"] = self._validate_text(
                description,
                "Character description",
                1000
            )

        if appearance is not None:
            character["appearance"] = self._validate_text(
                appearance,
                "Character appearance",
                1000
            )

        if personality is not None:
            character["personality"] = self._validate_text(
                personality,
                "Character personality",
                1000
            )

        if role is not None:
            character["role"] = self._validate_text(
                role,
                "Character role",
                200
            )

        comic["version"] += 1

        self._touch(comic)

        return deepcopy(character)

    # =========================================================
    # ADD PANEL
    # =========================================================

    def add_panel(
        self,
        comic_id: str,
        panel_number: int,
        title: str,
        scene_description: str,
        narration: str = "",
        dialogue: str = "",
        image_prompt: str = "",
        image_path: Optional[str] = None
    ) -> Dict[str, Any]:

        comic = self._get_internal(comic_id)

        if len(comic["panels"]) >= self.MAX_PANELS:
            raise ValueError(
                "Maximum panel limit reached"
            )

        if panel_number < 1:
            raise ValueError(
                "Panel number must be positive"
            )

        title = self._validate_text(
            title,
            "Panel title",
            300
        )

        scene_description = self._validate_text(
            scene_description,
            "Scene description",
            2000
        )

        panel = {

            "id": str(uuid.uuid4()),

            "panel_number": panel_number,

            "title": title,

            "scene_description":
                scene_description,

            "narration":
                narration.strip(),

            "dialogue":
                dialogue.strip(),

            "image_prompt":
                image_prompt.strip(),

            "image_path":
                image_path,

            "status":
                "pending",

            "created_at":
                datetime.now().isoformat()
        }

        self._save_version(comic)

        comic["panels"].append(panel)

        comic["status"] = "generating"

        self._touch(comic)

        return deepcopy(panel)

    # =========================================================
    # UPDATE PANEL
    # =========================================================

    def update_panel(
        self,
        comic_id: str,
        panel_number: int,
        **updates
    ) -> Dict[str, Any]:

        comic = self._get_internal(comic_id)

        allowed_fields = {
            "title",
            "scene_description",
            "narration",
            "dialogue",
            "image_prompt",
            "image_path"
        }

        for panel in comic["panels"]:

            if panel["panel_number"] == panel_number:

                self._save_version(comic)

                for key, value in updates.items():

                    if key in allowed_fields:

                        if isinstance(value, str):
                            value = value.strip()

                        panel[key] = value

                panel["status"] = "edited"

                comic["version"] += 1

                self._touch(comic)

                return deepcopy(panel)

        raise ValueError("Panel not found")

    # =========================================================
    # DELETE PANEL
    # =========================================================

    def delete_panel(
        self,
        comic_id: str,
        panel_number: int
    ) -> bool:

        comic = self._get_internal(comic_id)

        self._save_version(comic)

        original_count = len(
            comic["panels"]
        )

        comic["panels"] = [
            panel
            for panel in comic["panels"]
            if panel["panel_number"] != panel_number
        ]

        if len(comic["panels"]) == original_count:
            raise ValueError(
                "Panel not found"
            )

        comic["version"] += 1

        self._touch(comic)

        return True

    # =========================================================
    # PANEL REGENERATION
    # =========================================================

    def request_panel_regeneration(
        self,
        comic_id: str,
        panel_number: int,
        reason: str = ""
    ) -> Dict[str, Any]:

        comic = self._get_internal(comic_id)

        for panel in comic["panels"]:

            if panel["panel_number"] == panel_number:

                panel["status"] = "regeneration_requested"

                panel["regeneration_reason"] = (
                    reason.strip()
                )

                self._touch(comic)

                return deepcopy(panel)

        raise ValueError("Panel not found")

    # =========================================================
    # STORY IMPROVEMENT
    # =========================================================

    def request_story_improvement(
        self,
        comic_id: str,
        improvement_type: str
    ) -> Dict[str, Any]:

        allowed = {
            "improve",
            "add_plot_twist",
            "make_funnier",
            "make_more_dramatic",
            "expand",
            "shorten"
        }

        if improvement_type not in allowed:
            raise ValueError(
                "Unsupported improvement type"
            )

        comic = self._get_internal(comic_id)

        comic["improvement_request"] = {
            "type": improvement_type,
            "requested_at":
                datetime.now().isoformat(),
            "status": "pending"
        }

        self._touch(comic)

        return deepcopy(
            comic["improvement_request"]
        )

    # =========================================================
    # QUALITY CHECKER
    # =========================================================

    def save_quality_report(
        self,
        comic_id: str,
        report: Dict[str, Any]
    ) -> Dict[str, Any]:

        comic = self._get_internal(comic_id)

        comic["quality_report"] = {

            "checked_at":
                datetime.now().isoformat(),

            "report":
                report
        }

        self._touch(comic)

        return deepcopy(
            comic["quality_report"]
        )

    # =========================================================
    # STORY BRANCHING
    # =========================================================

    def create_story_branch(
        self,
        comic_id: str,
        branch_title: str,
        decision: str
    ) -> Dict[str, Any]:

        comic = self._get_internal(comic_id)

        branch = {

            "id":
                str(uuid.uuid4()),

            "title":
                self._validate_text(
                    branch_title,
                    "Branch title",
                    200
                ),

            "decision":
                self._validate_text(
                    decision,
                    "Decision",
                    1000
                ),

            "created_at":
                datetime.now().isoformat(),

            "status":
                "pending"
        }

        comic["branches"].append(branch)

        self._touch(comic)

        return deepcopy(branch)

    # =========================================================
    # CONTINUE STORY
    # =========================================================

    def continue_story(
        self,
        comic_id: str,
        instruction: str
    ) -> Dict[str, Any]:

        comic = self._get_internal(comic_id)

        instruction = self._validate_text(
            instruction,
            "Continuation instruction",
            2000
        )

        request = {

            "id":
                str(uuid.uuid4()),

            "instruction":
                instruction,

            "requested_at":
                datetime.now().isoformat(),

            "status":
                "pending"
        }

        comic.setdefault(
            "continuation_requests",
            []
        ).append(request)

        self._touch(comic)

        return deepcopy(request)

    # =========================================================
    # COMPLETE COMIC
    # =========================================================

    def complete_comic(
        self,
        comic_id: str
    ) -> Dict[str, Any]:

        comic = self._get_internal(comic_id)

        comic["status"] = "completed"

        self._touch(comic)

        return deepcopy(comic)

    # =========================================================
    # FAIL COMIC
    # =========================================================

    def fail_comic(
        self,
        comic_id: str,
        error_message: str
    ) -> Dict[str, Any]:

        comic = self._get_internal(comic_id)

        comic["status"] = "failed"

        comic["error"] = error_message

        self._touch(comic)

        return deepcopy(comic)

    # =========================================================
    # LIBRARY SEARCH
    # =========================================================

    def search_library(
        self,
        keyword: str = "",
        status: Optional[str] = None,
        genre: Optional[str] = None
    ) -> List[Dict[str, Any]]:

        keyword = keyword.lower().strip()

        results = []

        for comic in self.comics.values():

            if status and comic["status"] != status:
                continue

            if genre and comic["input"]["genre"] != genre:
                continue

            searchable_text = " ".join([
                comic["input"]["prompt"],
                comic["input"]["character"],
                comic["input"]["setting"],
                comic["input"]["genre"]
            ]).lower()

            if keyword and keyword not in searchable_text:
                continue

            results.append(
                deepcopy(comic)
            )

        return results

    # =========================================================
    # DELETE COMIC
    # =========================================================

    def delete_comic(
        self,
        comic_id: str
    ) -> bool:

        if comic_id not in self.comics:
            return False

        del self.comics[comic_id]

        return True

    # =========================================================
    # VERSION HISTORY
    # =========================================================

    def get_versions(
        self,
        comic_id: str
    ) -> List[Dict[str, Any]]:

        comic = self._get_internal(comic_id)

        return deepcopy(
            comic["versions"]
        )

    def restore_version(
        self,
        comic_id: str,
        version_index: int
    ) -> Dict[str, Any]:

        comic = self._get_internal(comic_id)

        versions = comic["versions"]

        if not (
            0 <= version_index < len(versions)
        ):
            raise ValueError(
                "Invalid version index"
            )

        restored = deepcopy(
            versions[version_index]
        )

        current_versions = comic["versions"]

        restored["versions"] = current_versions

        self.comics[comic_id] = restored

        return deepcopy(restored)

    # =========================================================
    # EXPORT RECORD
    # =========================================================

    def register_export(
        self,
        comic_id: str,
        export_type: str,
        file_path: str
    ) -> Dict[str, Any]:

        allowed_types = {
            "pdf",
            "png",
            "jpg"
        }

        if export_type not in allowed_types:
            raise ValueError(
                "Unsupported export type"
            )

        comic = self._get_internal(comic_id)

        export = {

            "id":
                str(uuid.uuid4()),

            "type":
                export_type,

            "file_path":
                file_path,

            "created_at":
                datetime.now().isoformat()
        }

        comic["exports"].append(export)

        self._touch(comic)

        return deepcopy(export)

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================

    def _get_internal(
        self,
        comic_id: str
    ) -> Dict[str, Any]:

        if comic_id not in self.comics:
            raise ValueError(
                "Comic not found"
            )

        return self.comics[comic_id]

    def _touch(
        self,
        comic: Dict[str, Any]
    ):

        comic["updated_at"] = (
            datetime.now().isoformat()
        )

    def _save_version(
        self,
        comic: Dict[str, Any]
    ):

        snapshot = deepcopy(comic)

        snapshot.pop(
            "versions",
            None
        )

        comic["versions"].append(
            snapshot
        )

        # Keep only recent versions.
        # Prevents unlimited memory growth.
        if len(comic["versions"]) > 20:
            comic["versions"] = (
                comic["versions"][-20:]
            )


# -------------------------------------------------------------
# SINGLE SERVICE INSTANCE
# -------------------------------------------------------------

comic_service = ComicService()