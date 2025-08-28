# This is a complete and corrected Streamlit chatbot that uses the Gemini API.
# It includes the necessary API key integration and corrects the `st.st` typo.

import streamlit as st
import requests
import json
import os
import time

# --- Step 1: Set up the page and your API Key ---
st.set_page_config(page_title="Gemini Chatbot")
st.title("A Smarter Chatbot with Gemini")
st.markdown("---")
st.info("I am a chatbot powered by the Google Gemini API. Ask me anything!")

# Correctly place your API key here.
# Replace "YOUR_API_KEY_HERE" with your actual, unique key.
API_KEY = "AIzaSyApEIiJ1uHu4Wc418Be80d-yOuaKHwmcfA"

# The API endpoint for the Gemini model. We'll use gemini-2.5-flash-preview-05-20.
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

# --- Step 2: Session State for Chat History ---
# We use session state to remember the conversation between user and bot.
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Step 3: Display Previous Messages ---
# Loop through the message history and display each one.
# The `st.chat_message` function automatically handles the avatars.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Step 4: Handle User Input and Generate Response ---
# Check for new user input from the chat widget.
if prompt := st.chat_input("What is on your mind?"):
    # Append the user's message to the chat history.
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display the user's message in the chat container.
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the payload for the Gemini API.
    # The 'contents' field holds the conversation history.
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    }

    # Set up the headers for the API request.
    headers = {
        "Content-Type": "application/json"
    }

    # Display a loading spinner while waiting for the AI response.
    with st.chat_message("assistant"):
        with st.spinner("Generating a response..."):
            try:
                # Make the POST request to the Gemini API.
                response = requests.post(
                    f"{API_URL}?key={API_KEY}",
                    data=json.dumps(payload),
                    headers=headers
                )

                # Check for a successful response and parse the JSON.
                if response.status_code == 200:
                    api_response = response.json()
                    # Extract the text from the API response.
                    bot_message = api_response.get("candidates")[0].get("content").get("parts")[0].get("text")
                    st.markdown(bot_message)
                    # Add the bot's message to the chat history.
                    st.session_state.messages.append({"role": "assistant", "content": bot_message})
                else:
                    st.error(f"Error: Could not get a response from the API. Status code: {response.status_code}")
                    st.error(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
