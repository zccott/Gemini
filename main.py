import base64
import os
import streamlit as st
from distributed.utils_test import client
from google import genai
from dotenv import load_dotenv
from openai import OpenAI
from utils import encode_image

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

def encodeImage(content):
    base64_image = encode_image(uploaded_file)
    return clientOpenAi.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": content,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
    ).choices[0].message.content

func_map = {
    "Google Gemini": gemini,
    "OpenAI Gemini": openAiCallingGemini,
    "Image Encoding": encodeImage,
}



# Select which method to use
method = st.sidebar.selectbox("Choose API method", list(func_map.keys()))
st.title(f"🌐 Ask to {method}")
content = st.text_input("Enter a question:")
uploaded_file = None
if method == "Image Encoding":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])


if st.button("Ask"):
    if not api_key:
        st.sidebar.warning("You need to enter your API key.")
    elif method == "Image Encoding":
        if uploaded_file is None:
            st.error("❌ Please upload an image before clicking Ask.")
        else:
            with st.spinner("Thinking..."):
                summary = func_map[method](content)
                st.subheader("📄 Answer:")
                st.write(summary)
    else:
        if not content:
            st.error("❌ Please enter a question before clicking Ask.")
        else:
            with st.spinner("Thinking..."):
                summary = func_map[method](content)
                st.subheader("📄 Answer:")
                st.write(summary)
