import os
import streamlit as st
from distributed.utils_test import client
from google import genai
from dotenv import load_dotenv


load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")

st.sidebar.title("🔑 API Configuration")
api_key = st.sidebar.text_input("Enter your API Key",value=gemini_api_key if gemini_api_key else "")

client = genai.Client(api_key=api_key)

st.title("🌐 Ask to Gemini")
content = st.text_input("Enter a question:")

def reply(content):
    return client.models.generate_content(
        model="gemini-2.0-flash", contents=content
    )
if st.button("Ask"):
    if not api_key:
        st.sidebar.warning("you need to enter your API key")
    else:
        with st.spinner("Thinking..."):
            summary = reply(content)
            if not content.startswith("Error"):
                st.subheader("📄 Answer:")
                st.write(summary.text)
            else:
                st.error(content)
