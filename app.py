import streamlit as st

from src.email_processor import (
    process_email_text,
    process_txt_file,
    extract_eml_content
)

from src.summarizer import analyze_email


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Smart Email Summarizer",
    page_icon="📧",
    layout="wide"
)


# -------------------------------------------------
# AI ANALYSIS FUNCTION
# -------------------------------------------------

def show_ai_analysis(email_text):

    if not email_text.strip():
        st.warning("No email content available for AI analysis.")
        return

    with st.spinner("🤖 Gemini is analyzing the email..."):

        try:
            result = analyze_email(email_text)

        except Exception as e:

            st.error("Unable to generate AI analysis.")
            st.caption(str(e))

            return

    st.divider()

    st.header("🤖 AI Email Analysis")


    # -------------------------------------------------
    # SUMMARY
    # -------------------------------------------------

    st.subheader("📝 Summary")

    st.write(
        result.get(
            "summary",
            "No summary available."
        )
    )


    # -------------------------------------------------
    # KEY POINTS
    # -------------------------------------------------

    st.subheader("🔑 Key Points")

    key_points = result.get(
        "key_points",
        []
    )

    if key_points:

        for point in key_points:
            st.markdown(f"- {point}")

    else:
        st.write("No key points found.")


    # -------------------------------------------------
    # ACTION ITEMS
    # -------------------------------------------------

    st.subheader("✅ Action Items")

    action_items = result.get(
        "action_items",
        []
    )

    if action_items:

        for item in action_items:
            st.markdown(f"- [ ] {item}")

    else:
        st.write("No action items found.")


    # -------------------------------------------------
    # DEADLINES
    # -------------------------------------------------

    st.subheader("⏰ Deadlines")

    deadlines = result.get(
        "deadlines",
        []
    )

    if deadlines:

        for deadline in deadlines:
            st.markdown(f"- {deadline}")

    else:
        st.write("No deadlines found.")


    # -------------------------------------------------
    # PRIORITY
    # -------------------------------------------------

    st.subheader("🚨 Priority")

    priority = result.get(
        "priority",
        "Unknown"
    )

    priority_reason = result.get(
        "priority_reason",
        ""
    )

    st.write(f"**Priority:** {priority}")

    if priority_reason:
        st.write(f"Reason: {priority_reason}")


    # -------------------------------------------------
    # SENTIMENT
    # -------------------------------------------------

    st.subheader("😊 Sentiment")

    sentiment = result.get(
        "sentiment",
        "Unknown"
    )

    sentiment_reason = result.get(
        "sentiment_reason",
        ""
    )

    st.write(f"**Sentiment:** {sentiment}")

    if sentiment_reason:
        st.write(
            f"Reason: {sentiment_reason}"
        )


# -------------------------------------------------
# MAIN APPLICATION
# -------------------------------------------------

st.title("📧 Smart Email Summarizer")

st.write(
    "AI-powered email summarization and analysis system"
)

st.divider()


# -------------------------------------------------
# EMAIL INPUT
# -------------------------------------------------

st.header("📨 Enter Your Email")

email_text = st.text_area(
    "Paste your email below:",
    height=250,
    placeholder="Paste your email here..."
)


# -------------------------------------------------
# ANALYZE BUTTON
# -------------------------------------------------


if st.button("🤖 Analyze Email"):

    if email_text.strip():

        # Process email
        processed_email = process_email_text(
            email_text
        )

        # Show processed email
        with st.expander("📄 View Processed Email"):
            st.write(processed_email)

        # Show AI analysis
        show_ai_analysis(
            processed_email
        )

        with st.expander("📄 View Original Email"):
            st.write(email_text)

    else:

        st.warning(
            "Please enter an email first."
        )

