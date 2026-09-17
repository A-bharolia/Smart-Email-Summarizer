import os
import json

from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Please add it to your .env file."
    )


# Create Gemini client
client = genai.Client(api_key=api_key)


def analyze_email(email_text):
    """
    Analyze an email using Gemini and return structured data.
    """

    prompt = f"""
You are an intelligent email analysis assistant.

Analyze the following email carefully.

Return ONLY valid JSON.
Do not include markdown.
Do not include ```json.
Do not include any explanation outside the JSON.

Use exactly this structure:

{{
    "summary": "A short summary of the email in 2-4 sentences.",
    "key_points": [
        "Important point 1",
        "Important point 2"
    ],
    "action_items": [
        "Task the recipient needs to perform"
    ],
    "deadlines": [
        "Date, time, or deadline mentioned in the email"
    ],
    "priority": "High",
    "priority_reason": "Short explanation for the priority",
    "sentiment": "Positive",
    "sentiment_reason": "Short explanation of the sentiment"
}}

Rules:

1. summary must be short and clear.
2. key_points must contain the most important information.
3. action_items must contain tasks the recipient needs to perform.
4. If there are no action items, return an empty list.
5. deadlines must contain important dates, times, or deadlines.
6. If there are no deadlines, return an empty list.
7. priority must be exactly one of:
   High, Medium, Low
8. sentiment must be exactly one of:
   Positive, Neutral, Negative
9. Do not invent information that is not present in the email.
10. Return valid JSON only.

EMAIL:
{email_text}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    response_text = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    if response_text.startswith("```json"):
        response_text = response_text[7:]

    if response_text.startswith("```"):
        response_text = response_text[3:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    try:
        result = json.loads(response_text)

    except json.JSONDecodeError:
        raise ValueError(
            "Gemini returned an invalid JSON response."
        )

    return result