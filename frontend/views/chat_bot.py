import streamlit as st
import requests
import mysql.connector
from dotenv import load_dotenv
import os
from backend.init_database import get_connection

# Load environment variables
load_dotenv()

API_URL = "http://127.0.0.1:8000"  # Change this for deployment

# Authentication (Docker Version)
BASE_API_URL = "http://localhost:7860"
FLOW_ID = "e9f77126-913a-432b-9960-d43c0397a59b"
ENDPOINT = "galgo-ai-simple-docker"  # Docker Flow

# Ensure correct agent is selected before loading MySQL messages
st.session_state.selected_agent = "All In"
if "previous_agent" not in st.session_state or st.session_state.previous_agent != "All In":
    st.session_state.current_session_id = None
st.session_state.previous_agent = "All In"

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("Please log in to use the Chat Bot.")
    st.stop()

user_id = st.session_state.user_email  # Retrieve logged-in user email

st.info(
    "**All In Agent**\n\n"
    "- Go *all in* with your personal communication & knowledge assistant\n"
    "- Tools included: Gmail, Google Calendar, Google Drive, OneDrive, Yahoo Finance, Wikipedia, Reddit, Github.\n"
    "- You can save chats to Cloud for future reference.\n"
)

# Initialize chat session state
if "messages_simple" not in st.session_state:
    st.session_state.messages_simple = []

# Load Messages from MySQL if a session was selected
if "selected_session_id" in st.session_state:
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT role, content FROM message WHERE session_id = %s ORDER BY timestamp ASC", 
                               (st.session_state.selected_session_id,))
                messages = cursor.fetchall()
                st.session_state.messages_simple = [{"role": row[0], "content": row[1]} for row in messages]
            del st.session_state.selected_session_id
        except mysql.connector.Error as err:
            st.error(f"Database error: {err}")
        finally:
            conn.close()

# Display Chat Messages
for message in st.session_state.messages_simple:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def run_flow(
    message: str,
    endpoint: str = ENDPOINT,  # Default to the defined endpoint
    output_type: str = "chat",
    input_type: str = "chat"
    ) -> str:

    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None  # No headers required for Docker API

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        response_json = response.json()

        print("DEBUG: Full API Response:", response_json)  # Debugging response structure

        # Extract response text
        outputs = response_json.get("outputs", [])
        if outputs and isinstance(outputs, list):
            try:
                chatbot_response = outputs[0]["outputs"][0]["results"]["message"]["data"]["text"]
                print("DEBUG: Extracted Chatbot Response:", chatbot_response)
                return chatbot_response
            except KeyError:
                print("Error extracting text, printing full response:", response_json)
                return "Error: Unexpected response format, check logs."

        return "Error: No response received."

    except requests.exceptions.RequestException as req_err:
        print(f"Request Error: {req_err}")
        return f"Request Error: {req_err}"
    except (KeyError, IndexError, TypeError) as parse_err:
        print(f"Parsing Error: {parse_err}")
        return "Error: Unexpected API response format."

if user_input := st.chat_input("Type your message here..."):
    # ✅ Append User Message to Session State
    st.session_state.messages_simple.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            with st.spinner("Galgo AI is typing..."):
                response = run_flow(user_input)  # ✅ Now uses refactored function
            placeholder.markdown(response)

            # ✅ Append Assistant Response to Session State
            st.session_state.messages_simple.append({"role": "assistant", "content": response})

        except Exception as e:
            placeholder.markdown("There was an error processing your request.")
            st.session_state.messages_simple.append({"role": "assistant", "content": "There was an error processing your request."})

# ✅ Replace direct function call with API request
if st.button("Save Chat Session"):
    save_payload = {
        "user_id": user_id,
        "agent": st.session_state.selected_agent,
        "messages": st.session_state.messages_simple
    }
    
    response = requests.post(f"{API_URL}/chat_history/save_chat_session", json=save_payload)

    if response.status_code == 200:
        st.success(f"✅ Chat session saved for agent: {st.session_state.selected_agent}")
    else:
        st.error("❌ Failed to save chat session.")