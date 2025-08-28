# This is the corrected and secure version of your Streamlit chatbot.
# It no longer exposes your API key in the code.

import streamlit as st
import requests
import json
import time

# --- Step 1: Set up the page ---
st.set_page_config(page_title="Secure Gemini Chatbot")
st.title("A Smarter Chatbot with Gemini")
st.markdown("---")
st.info("I am a chatbot powered by the Google Gemini API. Ask me anything!")

# --- Step 2: Access your API Key securely from Streamlit Secrets ---
# Use the NAME of the secret you saved, not the key itself.
API_KEY = st.secrets["gemini_api_key"]

# The API endpoint for the Gemini model.
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

# --- Step 3: Session State for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Step 4: Display Previous Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Step 5: Handle User Input and Generate Response ---
if prompt := st.chat_input("What is on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    with st.chat_message("assistant"):
        with st.spinner("Generating a response..."):
            try:
                response = requests.post(
                    f"{API_URL}?key={API_KEY}",
                    data=json.dumps(payload),
                    headers=headers
                )

                if response.status_code == 200:
                    api_response = response.json()
                    bot_message = api_response.get("candidates")[0].get("content").get("parts")[0].get("text")
                    st.markdown(bot_message)
                    st.session_state.messages.append({"role": "assistant", "content": bot_message})
                else:
                    st.error(f"Error: Could not get a response from the API. Status code: {response.status_code}")
                    st.error(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
