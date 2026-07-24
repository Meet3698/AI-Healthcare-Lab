import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


api_key = os.getenv("NARA_API_KEY")

base_url = os.getenv(
    "NARA_BASE_URL",
    "https://router.bynara.id/v1",
)

model = os.getenv(
    "NARA_MODEL",
    "auto/bynara",
)


if not api_key:
    raise RuntimeError(
        "NARA_API_KEY is missing from the .env file"
    )


client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


def chat_completion(messages):
    """
    Send a basic chat completion request.

    Only model and messages are sent to maximize
    compatibility with OpenAI-compatible routers.
    """

    return client.chat.completions.create(
        model=model,
        messages=messages,
    )