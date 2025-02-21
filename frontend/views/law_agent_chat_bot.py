import streamlit as st
import requests
import mysql.connector
from dotenv import load_dotenv
import os
from backend.init_database import get_connection

# Load environment variables
load_dotenv()

API_URL = "http://127.0.0.1:8000"  # Change this for deployment

# ✅ New Authentication Method
BASE_API_URL = "http://localhost:7860"
FLOW_ID = "f215dcce-daeb-4563-b3d6-116ff05e54b3"
ENDPOINT = "law-agent-docker"  # The endpoint name of the flow

# Ensure correct agent is selected before loading MySQL messages
st.session_state.selected_agent = "Lawyer's Agent"

if "previous_agent" not in st.session_state or st.session_state.previous_agent != "Lawyer's Agent":
    st.session_state.current_session_id = None
st.session_state.previous_agent = "Lawyer's Agent"

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("Please log in to use the Chat Bot.")
    st.stop()

user_id = st.session_state.user_email  # Retrieve logged-in user email

st.info(
    "**Lawyer's Agent**\n\n"
    "- Ask questions regarding your OneDrive documents and get answers from the Lawyer's Agent.\n"
    "- Designed to assist with legal document interpretation, navigation, and guidance.\n"
    "- Here are the documents available to the agent:\n"
    "    - [Executive Employment Agreement](https://1drv.ms/b/c/8573c846dfcb547d/Ebt1k7qZ7c9Gn5_0d9XtjfYBfaIFP3BIasrhJzEuv7wFFA?e=4hZH3n)\n"
    "    - [M&A Terms Sheet](https://1drv.ms/b/c/8573c846dfcb547d/ERdjACQurWVEqPOE5Ubpt-wBeNtAXOxERWg9CfD9V22RnA?e=Tf7hQz)\n"
    "    - [Software Development Agreement](https://1drv.ms/b/c/8573c846dfcb547d/ESb9TgUwfuhNpLgjZDWuzFcB0jcPyxct-kAYsIzkLKAwTQ?e=N4St9A)\n"
    "    - [NDA](https://1drv.ms/b/c/8573c846dfcb547d/ERoEayJb8MRPvtkvw9xIGksB9aiONRZtWXkdUD4KWXPThg?e=FMOa4s)\n"
    "    - [Shareholder's Agreement](https://1drv.ms/b/c/8573c846dfcb547d/Edul37RSvmxOvaEMW_aJjJ4BFBp8XWAosYkMk2pZDXUspQ?e=DrqA3B)\n"
)

# Initialize chat session state
if "messages_law" not in st.session_state:
    st.session_state.messages_law = []

# --- Load Messages from MySQL if a session was selected ---
if "selected_session_id" in st.session_state:
    conn = get_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT role, content FROM message WHERE session_id = %s ORDER BY timestamp ASC",
                    (st.session_state.selected_session_id,),
                )
                messages = cursor.fetchall()
                st.session_state.messages_law = [{"role": row[0], "content": row[1]} for row in messages]
            del st.session_state.selected_session_id
        except mysql.connector.Error as err:
            st.error(f"Database error: {err}")
        finally:
            conn.close()

# --- Display Chat Messages ---
for message in st.session_state.messages_law:
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

# User Input Handling
if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages_law.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            with st.spinner("Law Agent is typing..."):
                response = run_flow(user_input)
            placeholder.markdown(response)
        except Exception as e:
            placeholder.markdown("There was an error processing your request.")
            response = "There was an error processing your request."

    st.session_state.messages_law.append({"role": "assistant", "content": response})

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
