from typing import Any, Dict, List, Optional
from copy import deepcopy


class LibraryService:
    """
    Comic Library service.

    This service works with the comic objects managed by ComicService.
    It does not create a separate comic data structure.
    """

    def __init__(self, comic_service):
        self.comic_service = comic_service

    # =========================================================
    # SAVE COMIC TO LIBRARY
    # =========================================================

    def save_comic(self, comic_id: str) -> Optional[Dict[str, Any]]:
        """
        Save an existing comic to the library.

        The comic is already stored inside ComicService.
        This method only changes its library status.
        """

        # Check whether comic exists
        if comic_id not in self.comic_service.comics:
            return None

        # Get the actual stored comic
        comic = self.comic_service.comics[comic_id]

        # Mark comic as saved in library
        comic["in_library"] = True

        # Return a safe copy
        return deepcopy(comic)

    # =========================================================
    # GET ONE LIBRARY COMIC
    # =========================================================

    def get_comic(
        self,
        comic_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve one comic from the library.
        """

        # Check whether comic exists
        if comic_id not in self.comic_service.comics:
            return None

        # Get actual stored comic
        comic = self.comic_service.comics[comic_id]

        # Check library status
        if not comic.get("in_library", False):
            return None

        # Return a copy so outside code cannot
        # accidentally modify the stored comic
        return deepcopy(comic)

    # =========================================================
    # GET ALL LIBRARY COMICS
    # =========================================================

    def get_all_comics(self) -> List[Dict[str, Any]]:
        """
        Return all comics currently saved in the library.
        """

        comics = []

        # ComicService stores comics in self.comics
        for comic in self.comic_service.comics.values():

            # Only include saved comics
            if comic.get("in_library", False):

                comics.append(
                    deepcopy(comic)
                )

        return comics

    # =========================================================
    # SEARCH LIBRARY
    # =========================================================

    def search_library(
        self,
        keyword: str = "",
        status: Optional[str] = None,
        genre: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search comics saved in the library.

        Filters:
        - keyword
        - status
        - genre
        """

        # Get only library comics
        comics = self.get_all_comics()

        results = []

        for comic in comics:

            # -------------------------------------------------
            # KEYWORD FILTER
            # -------------------------------------------------

            if keyword:

                text = (
                    str(comic.get("title", "")) + " " +
                    str(comic.get("prompt", "")) + " " +
                    str(comic.get("character", ""))
                ).lower()

                if keyword.lower() not in text:
                    continue

            # -------------------------------------------------
            # STATUS FILTER
            # -------------------------------------------------

            if status is not None:

                if comic.get("status") != status:
                    continue

            # -------------------------------------------------
            # GENRE FILTER
            # -------------------------------------------------

            if genre is not None:

                if comic.get("genre") != genre:
                    continue

            # Comic passed all filters
            results.append(comic)

        return results

    # =========================================================
    # REMOVE COMIC FROM LIBRARY
    # =========================================================

    def remove_comic(self, comic_id: str) -> bool:
        """
        Remove a comic from the library.

        The comic itself is NOT deleted from ComicService.
        Only its library status is changed.
        """

        # Check whether comic exists
        if comic_id not in self.comic_service.comics:
            return False

        # Get the actual stored comic
        comic = self.comic_service.comics[comic_id]

        # Check whether it is currently in library
        if not comic.get("in_library", False):
            return False

        # Modify the actual stored comic
        comic["in_library"] = False

        return True

    # =========================================================
    # CHECK LIBRARY STATUS
    # =========================================================

    def is_in_library(self, comic_id: str) -> bool:
        """
        Check whether a comic is currently saved in the library.
        """

        # Check whether comic exists
        if comic_id not in self.comic_service.comics:
            return False

        # Get actual stored comic
        comic = self.comic_service.comics[comic_id]

        # Return library status
        return comic.get("in_library", False)