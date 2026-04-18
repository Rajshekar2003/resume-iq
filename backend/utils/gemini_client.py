import json
import os
import re
from typing import Type, TypeVar

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
import google.generativeai as genai

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

T = TypeVar("T", bound=BaseModel)


def _get_client() -> genai.GenerativeModel:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_key_here":
        raise EnvironmentError(
            "GEMINI_API_KEY is not set. Add your key to backend/.env"
        )
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def generate_text(prompt: str) -> str:
    try:
        model = _get_client()
        response = model.generate_content(prompt)
        return response.text
    except EnvironmentError:
        raise
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {e}") from e


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_structured_response(
    prompt: str, schema_class: Type[T], max_retries: int = 2
) -> T:
    last_error: Exception | None = None
    current_prompt = prompt

    for attempt in range(max_retries + 1):
        try:
            raw = generate_text(current_prompt)
            cleaned = _strip_code_fences(raw)
            data = json.loads(cleaned)
            return schema_class.model_validate(data)
        except (json.JSONDecodeError, ValidationError) as e:
            last_error = e
            if attempt < max_retries:
                print(f"[gemini_client] Attempt {attempt + 1} failed: {e}. Retrying...")
                current_prompt = (
                    prompt
                    + f"\n\nYour previous response failed validation. Error: {e}. "
                    "Please return ONLY valid JSON matching the exact schema specified."
                )

    raise RuntimeError(
        f"generate_structured_response failed after {max_retries + 1} attempts. "
        f"Last error: {last_error}"
    ) from last_error
