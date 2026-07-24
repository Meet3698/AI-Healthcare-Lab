import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.getenv("NARA_API_KEY"),
    base_url=os.getenv(
        "NARA_BASE_URL",
        "https://router.bynara.id/v1"
    )
)


def ask_ai(user_message: str) -> str:

    response = client.chat.completions.create(
        model=os.getenv(
            "NARA_MODEL",
            "auto/bynara"
        ),
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return response.choices[0].message.content