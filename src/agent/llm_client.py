
import os
import time
import random
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

MODEL_NAME = "gemini-3.8-flash"
MAX_ATTEMPTS = 3


def get_gemini_client() -> genai.Client:
    """Create a Gemini client using the key stored in .env."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Check your project-root .env file."
        )

    return genai.Client(api_key=api_key)


def generate_text(prompt: str) -> str:
    """Generate text with bounded retries for temporary API failures."""
    client = get_gemini_client()

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            if not response.text:
                raise RuntimeError("Gemini returned an empty response.")

            return response.text.strip()

        except (errors.ServerError, errors.APIError) as error:
            status_code = getattr(error, "code", None)

            # Retry only temporary server errors and rate limits.
            if status_code not in (429, 500, 502, 503, 504):
                raise

            if attempt == MAX_ATTEMPTS:
                raise RuntimeError(
                    f"Gemini remained unavailable after {MAX_ATTEMPTS} attempts."
                ) from error

            delay = (2 ** (attempt - 1)) + random.uniform(0, 0.5)

            print(
                f"Temporary Gemini API error ({status_code}). "
                f"Retrying in {delay:.1f} seconds "
                f"(attempt {attempt + 1}/{MAX_ATTEMPTS})..."
            )

            time.sleep(delay)


if __name__ == "__main__":
    answer = generate_text(
        "In one sentence, explain what SQL is to a beginner."
    )

    print("Gemini response:")
    print(answer)
