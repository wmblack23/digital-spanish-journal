from openai import OpenAI
import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def correct_spanish_entry(text):
    response = client.chat.completions.create(
        model="gpt-4",
        temperature=0.4,
        timeout=15,
        messages=[
            {
                "role": "system",
                "content": (
                    """You are a Spanish grammar expert. A student wrote a Spanish blog. Follow these steps carefully:

                    1. Correct the blog and output only the revised version.
                    2. Always return your result as a JSON object with three keys:
                    `corrected_text`, `corrections`, `score`.
                    3. For corrections, start each correction on a new line without any leading indicator such as (1.) or (-)
                    4. Make the score out of 10 (/10)"""
                )
            },
            {
                "role": "user",
                "content": f"Please correct this Spanish journal entry and provide feedback:\n{text}"
            }
        ]
    )
    data = response.choices[0].message.content
    return json.loads(data)

