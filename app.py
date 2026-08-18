import streamlit as st

from src.email_processor import (
    process_email_text,
    process_txt_file,
    extract_eml_content
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Smart Email Summarizer",
    page_icon="📧",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📧 Smart Email Summarizer")

st.write(
    "AI-powered email summarization and analysis system"
)

st.divider()


# --------------------------------------------------
# INPUT METHOD
# --------------------------------------------------

st.subheader("📥 Email Input")

input_method = st.radio(
    "Choose how you want to provide the email:",
    ["Paste Email", "Upload File"]
)


# --------------------------------------------------
# PASTE EMAIL
# --------------------------------------------------

if input_method == "Paste Email":

    email_text = st.text_area(
        "Paste your email below:",
        height=300,
        placeholder="Paste your email here..."
    )

    if st.button("Process Email"):

        if email_text.strip():

            cleaned_email = process_email_text(email_text)

            st.success("Email processed successfully!")

            st.subheader("📝 Processed Email")

            st.text_area(
                "Cleaned email:",
                value=cleaned_email,
                height=250
            )

        else:

            st.warning(
                "Please enter an email before processing."
            )


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

else:

    uploaded_file = st.file_uploader(
        "Upload an email file:",
        type=["txt", "eml"]
    )

    if uploaded_file is not None:

        st.info(
            f"Selected file: {uploaded_file.name}"
        )

        if st.button("Process File"):

            file_bytes = uploaded_file.getvalue()

            # ------------------------------------------
            # TXT FILE
            # ------------------------------------------

            if uploaded_file.name.lower().endswith(".txt"):

                cleaned_email = process_txt_file(
                    file_bytes
                )

                st.success(
                    "TXT file processed successfully!"
                )

                st.subheader("📝 Processed Email")

                st.text_area(
                    "Cleaned email:",
                    value=cleaned_email,
                    height=300
                )

            # ------------------------------------------
            # EML FILE
            # ------------------------------------------

            elif uploaded_file.name.lower().endswith(".eml"):

                email_data = extract_eml_content(
                    file_bytes
                )

                st.success(
                    "EML file processed successfully!"
                )

                st.subheader("📧 Email Information")

                col1, col2 = st.columns(2)

                with col1:

                    st.write("**Sender:**")

                    st.write(
                        email_data["sender"]
                    )

                    st.write("**Recipient:**")

                    st.write(
                        email_data["recipient"]
                    )

                with col2:

                    st.write("**Subject:**")

                    st.write(
                        email_data["subject"]
                    )

                    st.write("**Date:**")

                    st.write(
                        email_data["date"]
                    )

                st.divider()

                st.subheader("📄 Email Body")

                st.text_area(
                    "Processed email body:",
                    value=email_data["body"],
                    height=300
                )