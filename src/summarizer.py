import os

from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()


# Get Gemini API key


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")



# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def summarize_email(email_text):
    """
    Send an email to Gemini and return an AI-generated analysis.
    """

    prompt = f"""
You are an email analysis assistant.

Analyze the following email.

Provide the result in the following format:

SUMMARY:
Write a short summary of the email in 2-4 sentences.

KEY POINTS:
- List the most important points.
- Keep them short and clear.

ACTION ITEMS:
- List tasks that the recipient needs to perform.
- If there are no action items, write "None".

DEADLINES:
- List any dates, times, or deadlines mentioned.
- If there are no deadlines, write "None".

PRIORITY:
Choose one:
High
Medium
Low

Explain briefly why you selected the priority.

EMAIL:
{email_text}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text