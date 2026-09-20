import os

from dotenv import load_dotenv
from openai import OpenAI


class AIService:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-4.1-mini",
        )

        self.client = OpenAI(
            api_key=api_key,
            timeout=30.0,
            max_retries=1,
        )

    def generate_response(self, user_message: str) -> str:
        if not user_message.strip():
            raise ValueError(
                "The user message cannot be empty."
            )

        response = self.client.responses.create(
            model=self.model,
            instructions=(
                "You are ECLIPSE, a voice-first AI assistant "
                "integrated into augmented reality glasses. "
                "Provide helpful, accurate, and concise answers "
                "suitable for a small monocular HUD. "
                "Use natural conversational language. "
                "Do not claim to have performed device actions "
                "unless their execution has been confirmed."
            ),
            input=user_message,
            max_output_tokens=300,
        )

        return response.output_text