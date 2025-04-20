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
                "content": "You are a Spanish grammar expert. When given a Spanish journal entry from a learner, you will return corrections and suggestions for improvement. Please double check your work before responding! This is important for student learners. Could you also return a grade? Out of 10. I know this is a bit arbitrary but just use your best judgement with the number of errors etc. Also, after the corrected version of the blog and before the list of corrections ALWAYS include '%!()--;kxv' so that the system knows where to split the text. Do not lead with this text. First return the corrected entry, then that string, and then the list of corrections."
            },
            {
                "role": "user",
                "content": f"Please correct this Spanish journal entry and provide corrections: \n\n{text}"
            }
        ]
    )

    corrected_text = response.choices[0].message.content
    return corrected_text
