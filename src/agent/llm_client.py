
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def get_gemini_client() -> genai.Client:
    """Create a Gemini client using the key stored in .env."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Check your project-root .env file."
        )

    return genai.Client(api_key=api_key)


def generate_text(prompt: str) -> str:
    """Send a prompt to Gemini and return its text response."""
    client = get_gemini_client()

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text.strip()


if __name__ == "__main__":
    answer = generate_text(
        "In one sentence, explain what SQL is to a beginner."
    )
    print("Gemini response:")
    print(answer)
