import streamlit as st

st.set_page_config(
    page_title="Smart Email Summarizer",
    page_icon="📧",
    layout="wide"
)

st.title("📧 Smart Email Summarizer")

st.write(
    "AI-powered email summarization and analysis system"
)

st.divider()

st.subheader("Enter your email")

email_text = st.text_area(
    "Paste your email below:",
    height=250,
    placeholder="Paste your email here..."
)

if st.button("Analyze Email"):
    if email_text.strip():
        st.success("Email received successfully!")
    else:
        st.warning("Please enter an email first.")