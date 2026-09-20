import streamlit as st

from src.email_processor import (
    process_email_text,
    process_txt_file,
    extract_eml_content
)

from src.summarizer import analyze_email

from src.database import (
    initialize_database,
    save_email,
    get_all_emails,
    search_emails,
    get_emails_by_priority
)


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Smart Email Summarizer",
    page_icon="📧",
    layout="wide"
)


# -------------------------------------------------
# INITIALIZE DATABASE
# -------------------------------------------------

initialize_database()


# -------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------

st.sidebar.title("📂 Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Analyze Email",
        "Email History"
    ]
)


# =================================================
# AI ANALYSIS FUNCTION
# =================================================

def show_ai_analysis(email_text):

    if not email_text.strip():

        st.warning(
            "No email content available for AI analysis."
        )

        return

    with st.spinner(
        "🤖 Gemini is analyzing the email..."
    ):

        try:

            # Run AI analysis
            result = analyze_email(
                email_text
            )

            # Save email and analysis
            save_email(
                subject="Manual Email",
                sender="Unknown",
                email_body=email_text,
                analysis=result
            )

            st.success(
                "AI analysis completed and saved!"
            )

        except Exception as e:

            st.error(
                "Unable to generate AI analysis."
            )

            st.caption(
                str(e)
            )

            return


    # -------------------------------------------------
    # AI ANALYSIS
    # -------------------------------------------------

    st.divider()

    st.header(
        "🤖 AI Email Analysis"
    )


    # -------------------------------------------------
    # SUMMARY
    # -------------------------------------------------

    st.subheader(
        "📝 Summary"
    )

    st.write(
        result.get(
            "summary",
            "No summary available."
        )
    )


    # -------------------------------------------------
    # KEY POINTS
    # -------------------------------------------------

    st.subheader(
        "🔑 Key Points"
    )

    key_points = result.get(
        "key_points",
        []
    )

    if key_points:

        for point in key_points:

            st.markdown(
                f"- {point}"
            )

    else:

        st.write(
            "No key points found."
        )


    # -------------------------------------------------
    # ACTION ITEMS
    # -------------------------------------------------

    st.subheader(
        "✅ Action Items"
    )

    action_items = result.get(
        "action_items",
        []
    )

    if action_items:

        for item in action_items:

            st.markdown(
                f"- [ ] {item}"
            )

    else:

        st.write(
            "No action items found."
        )


    # -------------------------------------------------
    # DEADLINES
    # -------------------------------------------------

    st.subheader(
        "⏰ Deadlines"
    )

    deadlines = result.get(
        "deadlines",
        []
    )

    if deadlines:

        for deadline in deadlines:

            st.markdown(
                f"- {deadline}"
            )

    else:

        st.write(
            "No deadlines found."
        )


    # -------------------------------------------------
    # PRIORITY
    # -------------------------------------------------

    st.subheader(
        "🚨 Priority"
    )

    priority = result.get(
        "priority",
        "Unknown"
    )

    priority_reason = result.get(
        "priority_reason",
        ""
    )

    st.write(
        f"**Priority:** {priority}"
    )

    if priority_reason:

        st.write(
            f"Reason: {priority_reason}"
        )


    # -------------------------------------------------
    # SENTIMENT
    # -------------------------------------------------

    st.subheader(
        "😊 Sentiment"
    )

    sentiment = result.get(
        "sentiment",
        "Unknown"
    )

    sentiment_reason = result.get(
        "sentiment_reason",
        ""
    )

    st.write(
        f"**Sentiment:** {sentiment}"
    )

    if sentiment_reason:

        st.write(
            f"Reason: {sentiment_reason}"
        )


# =================================================
# EMAIL HISTORY PAGE
# =================================================

if page == "Email History":

    st.title(
        "📚 Email History"
    )


    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------

    search_term = st.text_input(
        "🔎 Search emails",
        placeholder="Search by subject or email content..."
    )


    # -------------------------------------------------
    # PRIORITY FILTER
    # -------------------------------------------------

    priority_filter = st.selectbox(
        "🚨 Filter by priority",
        [
            "All",
            "High",
            "Medium",
            "Low"
        ]
    )


    # -------------------------------------------------
    # GET EMAILS
    # -------------------------------------------------

    if search_term.strip():

        emails = search_emails(
            search_term
        )

    else:

        emails = get_all_emails()


    # -------------------------------------------------
    # APPLY PRIORITY FILTER
    # -------------------------------------------------

    if priority_filter != "All":

        emails = [
            email
            for email in emails
            if email["priority"] == priority_filter
        ]


    # -------------------------------------------------
    # DISPLAY EMAILS
    # -------------------------------------------------

    if not emails:

        st.info(
            "No emails found."
        )

    else:

        for email in emails:

            with st.expander(
                f"📧 {email['subject']} "
                f"| 🚨 {email['priority']} "
                f"| 😊 {email['sentiment']}"
            ):

                st.write(
                    f"**Date:** "
                    f"{email['created_at']}"
                )


                # Summary
                st.subheader(
                    "📝 Summary"
                )

                st.write(
                    email["summary"]
                )


                # Original email
                st.subheader(
                    "📌 Original Email"
                )

                st.text_area(
                    "Email content",
                    value=email["email_body"],
                    height=150,
                    key=f"email_{email['id']}"
                )


# =================================================
# ANALYZE EMAIL PAGE
# =================================================

if page == "Analyze Email":

    st.title(
        "📧 Smart Email Summarizer"
    )

    st.write(
        "AI-powered email summarization and analysis system"
    )

    st.divider()


    # -------------------------------------------------
    # EMAIL INPUT
    # -------------------------------------------------

    st.header(
        "📨 Enter Your Email"
    )

    email_text = st.text_area(
        "Paste your email below:",
        height=250,
        placeholder="Paste your email here..."
    )


    # -------------------------------------------------
    # ANALYZE BUTTON
    # -------------------------------------------------

    if st.button(
        "🤖 Analyze Email"
    ):

        if email_text.strip():

            # Process email
            processed_email = process_email_text(
                email_text
            )


            # Show processed email
            with st.expander(
                "📄 View Processed Email"
            ):

                st.write(
                    processed_email
                )


            # Show AI analysis
            show_ai_analysis(
                processed_email
            )


            # Show original email
            with st.expander(
                "📄 View Original Email"
            ):

                st.write(
                    email_text
                )

        else:

            st.warning(
                "Please enter an email first."
            )
