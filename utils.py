from openai import OpenAI
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def correct_spanish_entry(text):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    """You are a Spanish grammar expert. A student wrote a Spanish blog. Follow these steps carefully:

                    1. Correct the blog and output only the revised version.
                    2. Write '%!()--;kxv' to separate sections.
                    3. List each correction with a short explanation in English. Start each with a dash '-'.
                    5. Give the original entry a score out of 10 with no additional explanation."""
                )
            },
            {
                "role": "user",
                "content": f"Please correct this Spanish journal entry and provide feedback:\n\n{text}"
            }
        ]
    )
    return response.choices[0].message.content

