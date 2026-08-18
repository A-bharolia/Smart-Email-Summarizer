from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
import re


def clean_text(text):
    """
    Clean unnecessary whitespace from email text.
    """

    if not text:
        return ""

    # Replace multiple spaces/tabs with one space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove spaces at the beginning/end of each line
    text = "\n".join(line.strip() for line in text.splitlines())

    return text.strip()


def html_to_text(html):
    """
    Convert HTML email content into readable plain text.
    """

    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")

    return soup.get_text(separator="\n")


def extract_eml_content(file_bytes):
    """
    Extract sender, recipient, subject, date and body from an EML file.
    """

    msg = BytesParser(policy=policy.default).parsebytes(file_bytes)

    sender = msg.get("From", "")
    recipient = msg.get("To", "")
    subject = msg.get("Subject", "")
    date = msg.get("Date", "")

    plain_text = ""
    html_text = ""

    if msg.is_multipart():

        for part in msg.walk():

            content_type = part.get_content_type()

            if content_type == "text/plain":
                try:
                    plain_text += part.get_content()
                except Exception:
                    pass

            elif content_type == "text/html":
                try:
                    html_text += part.get_content()
                except Exception:
                    pass

    else:

        content_type = msg.get_content_type()

        if content_type == "text/plain":
            try:
                plain_text = msg.get_content()
            except Exception:
                pass

        elif content_type == "text/html":
            try:
                html_text = msg.get_content()
            except Exception:
                pass

    # Prefer plain text when available
    if plain_text.strip():
        body = plain_text
    else:
        body = html_to_text(html_text)

    body = clean_text(body)

    return {
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "date": date,
        "body": body
    }


def process_txt_file(file_bytes):
    """
    Convert uploaded TXT file into clean text.
    """

    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text = file_bytes.decode("latin-1")

    return clean_text(text)


def process_email_text(text):
    """
    Process manually pasted email text.
    """

    return clean_text(text)