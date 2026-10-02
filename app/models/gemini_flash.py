import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)


def generate_outline(
    prompt,
    character,
    setting,
    genre="Adventure",
    mood="Exciting",
    art_style="Comic",
    language="English",
    panel_count=5
):
    """
    Generate a structured comic storyboard using Gemini.
    """

    instruction = f"""
Create a {panel_count}-panel comic storyboard.

Story idea:
{prompt}

Main character:
{character}

Setting:
{setting}

Genre:
{genre}

Mood:
{mood}

Art style:
{art_style}

Language:
{language}

For each panel provide:

Panel Number:
Title:
Scene Description:
Image Prompt:

Make the story have a clear beginning, middle, and ending.
Keep the same main character throughout all panels.
Return ONLY the storyboard.
"""

    response = client.models.generate_content(
       model="gemini-3.5-flash-lite",
        contents=instruction
    )

    return response.text