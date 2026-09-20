import sqlite3
import json
from pathlib import Path


# -------------------------------------------------
# DATABASE LOCATION
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "smart_email.db"


# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------

def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    # Allows us to access database columns by name
    connection.row_factory = sqlite3.Row

    return connection


# -------------------------------------------------
# INITIALIZE DATABASE
# -------------------------------------------------

def initialize_database():
    """
    Create the emails table if it does not already exist.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS emails (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            subject TEXT,

            sender TEXT,

            email_body TEXT,

            summary TEXT,

            key_points TEXT,

            action_items TEXT,

            deadlines TEXT,

            priority TEXT,

            priority_reason TEXT,

            sentiment TEXT,

            sentiment_reason TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    connection.commit()

    connection.close()


# -------------------------------------------------
# SAVE EMAIL
# -------------------------------------------------

def save_email(
    subject,
    sender,
    email_body,
    analysis
):
    """
    Save email and AI analysis to the database.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO emails (
            subject,
            sender,
            email_body,
            summary,
            key_points,
            action_items,
            deadlines,
            priority,
            priority_reason,
            sentiment,
            sentiment_reason
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            subject,

            sender,

            email_body,

            analysis.get(
                "summary",
                ""
            ),

            json.dumps(
                analysis.get(
                    "key_points",
                    []
                )
            ),

            json.dumps(
                analysis.get(
                    "action_items",
                    []
                )
            ),

            json.dumps(
                analysis.get(
                    "deadlines",
                    []
                )
            ),

            analysis.get(
                "priority",
                ""
            ),

            analysis.get(
                "priority_reason",
                ""
            ),

            analysis.get(
                "sentiment",
                ""
            ),

            analysis.get(
                "sentiment_reason",
                ""
            )
        )
    )

    connection.commit()

    connection.close()


# -------------------------------------------------
# GET ALL EMAILS
# -------------------------------------------------

def get_all_emails():
    """
    Return all saved emails.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM emails
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


# -------------------------------------------------
# GET EMAIL BY ID
# -------------------------------------------------

def get_email_by_id(email_id):
    """
    Return one email using its ID.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM emails
        WHERE id = ?
        """,

        (email_id,)
    )

    row = cursor.fetchone()

    connection.close()

    return row


# -------------------------------------------------
# SEARCH EMAILS
# -------------------------------------------------

def search_emails(search_term):
    """
    Search emails by subject or email body.
    """

    connection = get_connection()

    cursor = connection.cursor()

    search_pattern = f"%{search_term}%"

    cursor.execute(
        """
        SELECT *
        FROM emails
        WHERE subject LIKE ?
           OR email_body LIKE ?

        ORDER BY created_at DESC
        """,

        (
            search_pattern,
            search_pattern
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


# -------------------------------------------------
# GET EMAILS BY PRIORITY
# -------------------------------------------------

def get_emails_by_priority(priority):
    """
    Return emails matching a priority.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM emails
        WHERE priority = ?

        ORDER BY created_at DESC
        """,

        (priority,)
    )

    rows = cursor.fetchall()

    connection.close()

    return rows
