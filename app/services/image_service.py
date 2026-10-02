from app.models.image_generator import generate_image
from app.services.comic_service import comic_service


class ImageService:

    def __init__(self, comic_service_instance):
        self.comic_service = comic_service_instance

    def generate_panel_image(
        self,
        comic_id: str,
        panel_number: int
    ):

        # Get comic
        comic = self.comic_service.get_comic(comic_id)

        if comic is None:
            raise ValueError("Comic not found")

        # Find panel
        panel = None

        for p in comic.get("panels", []):
            if p.get("panel_number") == panel_number:
                panel = p
                break

        if panel is None:
            raise ValueError(
                f"Panel {panel_number} not found"
            )

        # Get image prompt
        image_prompt = panel.get(
            "image_prompt",
            ""
        )

        if not image_prompt:
            image_prompt = panel.get(
                "scene_description",
                "Comic scene"
            )

        # Generate filename
        filename = (
            f"{comic_id}_"
            f"panel_{panel_number}.png"
        )

        # Generate image
        image_path = generate_image(
            prompt=image_prompt,
            filename=filename
        )

        # Get actual stored comic
        if comic_id not in self.comic_service.comics:
            raise ValueError("Comic not found in storage")

        stored_comic = self.comic_service.comics[comic_id]

        # Update the actual stored panel
        for stored_panel in stored_comic.get("panels", []):

            if stored_panel.get("panel_number") == panel_number:

                stored_panel["image_path"] = image_path
                stored_panel["status"] = "completed"

                break

        # Get the updated panel
        updated_panel = None

        for stored_panel in stored_comic.get("panels", []):

            if stored_panel.get("panel_number") == panel_number:

                updated_panel = stored_panel

                break

        # Return updated panel
        return {
            "success": True,
            "message": "Panel image generated successfully",
            "panel": updated_panel
        }


# Create service instance
image_service = ImageService(comic_service)