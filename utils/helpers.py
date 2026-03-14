from google import genai
from utils.config import MODEL_NAME

# Create Gemini client (auto reads GEMINI_API_KEY from environment)
client = genai.Client()


def generate_content(prompt: str):

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "temperature": 0.7,
            "top_p": 0.95,
            "max_output_tokens": 2048,
        }
    )

    return response.text
