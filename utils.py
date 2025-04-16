from openai import OpenAI
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def correct_spanish_entry(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a Spanish grammar expert. When given a Spanish journal entry from a learner, you will return corrections and suggestions for improvement."
            },
            {
                "role": "user",
                "content": f"Please correct this Spanish journal entry and provide explanations:\n\n{text}"
            }
        ]
    )

    corrected_text = response.choices[0].message.content
    return corrected_text
