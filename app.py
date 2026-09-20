import streamlit as st
import plotly.express as px

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
    get_emails_by_priority,
    get_email_statistics,
    get_sentiment_statistics
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Email Summarizer",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 40px;
        font-weight: 700;
    }

    .subtitle {
        font-size: 18px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("📧 Smart Email Summarizer")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "✉️ Analyze Email",
        "📚 Email History",
        "ℹ️ About"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">🏠 Dashboard</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Overview of your analyzed emails and AI insights."
    )

    st.divider()

    # --------------------------------------------------------
    # GET STATISTICS
    # --------------------------------------------------------

    stats = get_email_statistics()

    # --------------------------------------------------------
    # METRIC CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📧 Total Emails",
            stats["total_emails"]
        )

    with col2:

        st.metric(
            "🚨 High Priority",
            stats["high_priority"]
        )

    with col3:

        st.metric(
            "🟡 Medium Priority",
            stats["medium_priority"]
        )

    with col4:

        st.metric(
            "🟢 Low Priority",
            stats["low_priority"]
        )

    st.divider()

    # --------------------------------------------------------
    # CHART DATA
    # --------------------------------------------------------

    priority_data = {
        "Priority": [
            "High",
            "Medium",
            "Low"
        ],
        "Count": [
            stats["high_priority"],
            stats["medium_priority"],
            stats["low_priority"]
        ]
    }

    priority_fig = px.bar(
        priority_data,
        x="Priority",
        y="Count",
        title="Email Priority Distribution"
    )

    # --------------------------------------------------------
    # SENTIMENT DATA
    # --------------------------------------------------------

    sentiment_rows = get_sentiment_statistics()

    sentiment_data = {
        "Sentiment": [
            row["sentiment"]
            for row in sentiment_rows
        ],
        "Count": [
            row["count"]
            for row in sentiment_rows
        ]
    }

    # --------------------------------------------------------
    # DISPLAY CHARTS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.plotly_chart(
            priority_fig,
            use_container_width=True
        )

    with col2:

        if sentiment_data["Sentiment"]:

            sentiment_fig = px.pie(
                sentiment_data,
                names="Sentiment",
                values="Count",
                title="Email Sentiment Distribution"
            )

            st.plotly_chart(
                sentiment_fig,
                use_container_width=True
            )

        else:

            st.info(
                "No sentiment data available yet."
            )

    st.divider()

    # --------------------------------------------------------
    # RECENT EMAILS
    # --------------------------------------------------------

    st.subheader(
        "🕐 Recently Analyzed Emails"
    )

    recent_emails = get_recent_emails(5)

    if not recent_emails:

        st.info(
            "No emails have been analyzed yet."
        )

    else:

        for email in recent_emails:

            with st.container(border=True):

                st.write(
                    f"📧 **{email['subject']}**"
                )

                st.caption(
                    f"Priority: {email['priority']} | "
                    f"Sentiment: {email['sentiment']} | "
                    f"{email['created_at']}"
                )

                st.write(
                    email["summary"]
                )


# ============================================================
# ANALYZE EMAIL
# ============================================================

elif page == "✉️ Analyze Email":

    st.markdown(
        '<div class="main-title">📧 Smart Email Summarizer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-powered email summarization and analysis system'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader(
        "Enter your email"
    )

    # --------------------------------------------------------
    # INPUT METHOD
    # --------------------------------------------------------

    input_method = st.radio(
        "Choose input method:",
        [
            "Paste Email",
            "Upload TXT File",
            "Upload EML File"
        ],
        horizontal=True
    )

    email_text = ""

    # ========================================================
    # PASTE EMAIL
    # ========================================================

    if input_method == "Paste Email":

        email_text = st.text_area(
            "Paste your email below:",
            height=250,
            placeholder=(
                "Paste your email here..."
            )
        )

        st.caption(
            f"Characters: {len(email_text)}"
        )

    # ========================================================
    # TXT FILE
    # ========================================================

    elif input_method == "Upload TXT File":

        uploaded_file = st.file_uploader(
            "Upload a TXT file",
            type=["txt"]
        )

        if uploaded_file:

            try:

                email_text = process_txt_file(
                    uploaded_file
                )

                st.success(
                    "TXT file loaded successfully!"
                )

                st.text_area(
                    "Email content:",
                    value=email_text,
                    height=250
                )

            except Exception as e:

                st.error(
                    "Unable to read the TXT file."
                )

                st.caption(
                    str(e)
                )

    # ========================================================
    # EML FILE
    # ========================================================

    elif input_method == "Upload EML File":

        uploaded_file = st.file_uploader(
            "Upload an EML file",
            type=["eml"]
        )

        if uploaded_file:

            try:

                eml_result = extract_eml_content(
                    uploaded_file
                )

                if isinstance(eml_result, tuple):

                    email_text = eml_result[0]

                else:

                    email_text = eml_result

                st.success(
                    "EML file loaded successfully!"
                )

                st.text_area(
                    "Email content:",
                    value=email_text,
                    height=250
                )

            except Exception as e:

                st.error(
                    "Unable to read the EML file."
                )

                st.caption(
                    str(e)
                )

    # --------------------------------------------------------
    # ANALYZE BUTTON
    # --------------------------------------------------------

    if st.button(
        "🤖 Analyze Email",
        type="primary"
    ):

        if not email_text.strip():

            st.warning(
                "⚠️ Please enter or upload an email first."
            )

        else:

            try:

                # --------------------------------------------
                # PROCESS EMAIL
                # --------------------------------------------

                cleaned_email = process_email_text(
                    email_text
                )

                # --------------------------------------------
                # GEMINI AI ANALYSIS
                # --------------------------------------------

                with st.spinner(
                    "🤖 AI is analyzing your email..."
                ):

                    result = analyze_email(
                        cleaned_email
                    )

                # --------------------------------------------
                # SAVE TO DATABASE
                # --------------------------------------------

                save_email(
                    subject="Manual Email",
                    sender="Unknown",
                    email_body=cleaned_email,
                    analysis=result
                )

                st.success(
                    "✅ AI analysis completed and saved!"
                )

                st.divider()

                # =================================================
                # DISPLAY SUMMARY
                # =================================================

                st.subheader(
                    "📝 Summary"
                )

                st.write(
                    result.get(
                        "summary",
                        "No summary available."
                    )
                )

                # =================================================
                # KEY POINTS
                # =================================================

                st.subheader(
                    "📌 Key Points"
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

                # =================================================
                # ACTION ITEMS
                # =================================================

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
                            f"- {item}"
                        )

                else:

                    st.write(
                        "No action items found."
                    )

                # =================================================
                # DEADLINES
                # =================================================

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

                # =================================================
                # PRIORITY + SENTIMENT
                # =================================================

                col1, col2 = st.columns(2)

                with col1:

                    st.subheader(
                        "🚨 Priority"
                    )

                    st.write(
                        result.get(
                            "priority",
                            "Unknown"
                        )
                    )

                    st.caption(
                        result.get(
                            "priority_reason",
                            ""
                        )
                    )

                with col2:

                    st.subheader(
                        "😊 Sentiment"
                    )

                    st.write(
                        result.get(
                            "sentiment",
                            "Unknown"
                        )
                    )

                    st.caption(
                        result.get(
                            "sentiment_reason",
                            ""
                        )
                    )

            except Exception as e:

                st.error(
                    "❌ Unable to generate AI analysis."
                )

                st.info(
                    "Please check your API key, "
                    "internet connection, and input."
                )

                with st.expander(
                    "Technical details"
                ):

                    st.code(
                        str(e)
                    )


# ============================================================
# EMAIL HISTORY
# ============================================================

elif page == "📚 Email History":

    st.markdown(
        '<div class="main-title">📚 Email History</div>',
        unsafe_allow_html=True
    )

    st.write(
        "View, search, and filter previously analyzed emails."
    )

    st.divider()

    # --------------------------------------------------------
    # SEARCH AND FILTER
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        search_term = st.text_input(
            "🔎 Search emails",
            placeholder=(
                "Search by subject or email content..."
            )
        )

    with col2:

        priority_filter = st.selectbox(
            "🚨 Filter by priority",
            [
                "All",
                "High",
                "Medium",
                "Low"
            ]
        )

    # --------------------------------------------------------
    # GET EMAILS
    # --------------------------------------------------------

    if priority_filter == "All":

        if search_term.strip():

            emails = search_emails(
                search_term
            )

        else:

            emails = get_all_emails()

    else:

        emails = get_emails_by_priority(
            priority_filter
        )

        # Apply search manually if needed
        if search_term.strip():

            search_lower = search_term.lower()

            emails = [
                email
                for email in emails
                if (
                    search_lower
                    in (
                        email["subject"] or ""
                    ).lower()
                    or
                    search_lower
                    in (
                        email["email_body"] or ""
                    ).lower()
                )
            ]

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    if not emails:

        st.info(
            "No emails found."
        )

    else:

        st.caption(
            f"Showing {len(emails)} email(s)"
        )

        for email in emails:

            with st.container(border=True):

                st.subheader(
                    f"📧 {email['subject']}"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"🚨 **Priority:** "
                        f"{email['priority']}"
                    )

                with col2:

                    st.write(
                        f"😊 **Sentiment:** "
                        f"{email['sentiment']}"
                    )

                with col3:

                    st.write(
                        f"🕐 **Date:** "
                        f"{email['created_at']}"
                    )

                st.write(
                    f"**Summary:** "
                    f"{email['summary']}"
                )

                with st.expander(
                    "📄 View Original Email"
                ):

                    st.write(
                        email["email_body"]
                    )


# ============================================================
# ABOUT PAGE
# ============================================================

elif page == "ℹ️ About":

    st.markdown(
        '<div class="main-title">ℹ️ About</div>',
        unsafe_allow_html=True
    )

    st.write(
        """
        Smart Email Summarizer is an AI-powered
        application that analyzes emails and
        generates concise summaries and useful
        insights.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    st.subheader(
        "🚀 Features"
    )

    st.markdown(
        """
        - 📧 AI-powered email summarization
        - 📌 Key point extraction
        - ✅ Action item detection
        - ⏰ Deadline extraction
        - 🚨 Priority classification
        - 😊 Sentiment analysis
        - 📚 Email history
        - 🔎 Email search
        - 🔽 Priority filtering
        - 📊 Analytics dashboard
        - 💾 SQLite database
        - 📁 TXT and EML file support
        """
    )

    # --------------------------------------------------------
    # TECHNOLOGIES
    # --------------------------------------------------------

    st.subheader(
        "🛠️ Technologies Used"
    )

    st.markdown(
        """
        - **Python**
        - **Streamlit**
        - **Google Gemini API**
        - **SQLite**
        - **Plotly**
        - **Pandas**
        - **BeautifulSoup**
        - **Pytest**
        - **Git & GitHub**
        """
    )

    # --------------------------------------------------------
    # ARCHITECTURE
    # --------------------------------------------------------

    st.subheader(
        "🏗️ Project Architecture"
    )

    st.code(
        """
User
  ↓
Streamlit UI
  ↓
Email Processor
  ↓
Gemini AI
  ↓
Structured Analysis
  ↓
SQLite Database
  ↓
Dashboard / History / Search
        """,
        language="text"
    )

    # --------------------------------------------------------
    # PROJECT PURPOSE
    # --------------------------------------------------------

    st.subheader(
        "🎯 Project Purpose"
    )

    st.write(
        """
        The purpose of this project is to reduce the time
        required to read and understand long emails by using
        generative AI to automatically extract the most
        important information.
        """
    )
