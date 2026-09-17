from src.email_processor import clean_text


def test_clean_text():

    text = "Hello     Team\n\n\nPlease submit the report."

    result = clean_text(text)

    assert result == (
        "Hello Team\n\n"
        "Please submit the report."
    )