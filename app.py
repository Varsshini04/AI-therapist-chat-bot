# app.py

import os
import streamlit as st
from openai import OpenAI
from streamlit_chat import message

st.set_page_config(
    page_title="AI Therapist", page_icon="💬", layout="wide"
)  


hide_streamlit_style = """
<style>
    /* Hide top-right menu and header */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    /* Hide "Made with Streamlit" footer */
    footer {visibility: hidden;}
    /* Body styling */
    body {background-color: #F9FAFB;}
    /* Chat bubble fonts/colors */
    .stMarkdown p {font-family: 'Segoe UI', sans-serif;}
</style>
"""
st.markdown(
    hide_streamlit_style, unsafe_allow_html=True
) 

with st.sidebar:
    st.title("⚙ Settings")
    temperature = st.slider(
        "Temperature", 0.0, 1.0, 0.7
    )  
    max_tokens = st.slider(
        "Max Tokens", 128, 1024, 512
    )  
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": "You are talking to a compassionate AI therapist. The therapist will gently guide you through your feelings..",
            }
        ]

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are talking to a compassionate AI therapist. The therapist will gently guide you through your feelings.",
        }
    ]  
st.markdown(
    "## 🗣 AI Therapist Chat\nFeel heard and supported—your conversation is confidential."
)
for i, msg in enumerate(st.session_state.messages):
    is_user = msg["role"] == "user"
    avatar = "👤" if is_user else "🤖"
    message(
        msg["content"],
        is_user=is_user,
        key=f"msg_{i}",
        avatar_style="pixel" if is_user else "big-smile",
    )  

user_input = st.chat_input(
    "What’s on your mind today?"
)  
if user_input:
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    message(user_input, is_user=True, key=f"user_{len(st.session_state.messages)}")

    client = OpenAI(
        api_key="******", base_url="https://api.sambanova.ai/v1"
    )  

    try:
        resp = client.chat.completions.create(
            model="Meta-Llama-3.1-405B-Instruct",
            messages=st.session_state.messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        bot_text = resp.choices[0].message.content
    except Exception as e:
        bot_text = "❗ Oops, something went wrong. Please try again later."
        st.error(str(e))


    st.session_state.messages.append({"role": "assistant", "content": bot_text})
    message(bot_text, is_user=False, key=f"bot_{len(st.session_state.messages)}")