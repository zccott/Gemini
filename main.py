import os
import streamlit as st
from distributed.utils_test import client
from google import genai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

st.sidebar.title("🔑 API Configuration")
api_key = st.sidebar.text_input("Enter your API Key", value=gemini_api_key if gemini_api_key else "")

clientGemini = genai.Client(api_key=api_key)

clientOpenAi = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def gemini(content):
    return clientGemini.models.generate_content(
        model="gemini-2.0-flash", contents=content
    ).text


def openAiCallingGemini(content):
    return clientOpenAi.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": content
            }
        ]
    ).choices[0].message.content

func_map = {
    "Google Gemini": gemini,
    "OpenAI Gemini": openAiCallingGemini,
}

# Select which method to use
method = st.sidebar.selectbox("Choose API method", list(func_map.keys()))
st.title(f"🌐 Ask to {method}")
content = st.text_input("Enter a question:")

if st.button("Ask"):
    if not api_key:
        st.sidebar.warning("you need to enter your API key")
    else:
        with st.spinner("Thinking..."):
            summary = func_map[method](content)
            if not content.startswith("Error"):
                st.subheader("📄 Answer:")
                st.write(summary)
            else:
                st.error(content)
