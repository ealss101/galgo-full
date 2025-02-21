import streamlit as st
import requests
import mysql.connector
from dotenv import load_dotenv
import os
from backend.init_database import get_connection

# Load environment variables
load_dotenv()

API_URL = "http://127.0.0.1:8000"  # Change this for deployment

BASE_API_URL = "http://localhost:7860"
FLOW_ID = "b5e748a9-4df3-42d3-a0ad-9002465d878f"
ENDPOINT = "accounting-research" # You can set a specific endpoint name in the flow settings

# Ensure correct agent is selected before loading MySQL messages
st.session_state.selected_agent = "Accounting Researcher"

if "previous_agent" not in st.session_state or st.session_state.previous_agent != "Accounting Researcher":
    st.session_state.current_session_id = None
st.session_state.previous_agent = "Accounting Researcher"

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("Please log in to use the Chat Bot.")
    st.stop()

user_id = st.session_state.user_email  # Retrieve logged-in user email

st.info(
    "**Accounting Researcher**\n\n"
    "- Your AI-powered guide for financial accounting research.\n"
    "- Instantly search and retrieve financial accounting papers from your OneDrive.\n"
    "- Get AI-driven insights, summaries, and explanations on complex accounting topics.\n"
    "- Here are the financial accounting papers available to the agent:\n"
    "    - [Final CHI](https://1drv.ms/b/c/8573c846dfcb547d/EUcXvX4LseZBml9oahlT9e8BaaGgfQFQcr-5KRl6Qo2UqQ?e=RdZcPy)\n"
    "    - [Philip et al. 2023](https://1drv.ms/b/c/8573c846dfcb547d/EWZdMuHOjhZMrZKYVnLBxXkBY6sAWhSWXd7oTelx4QuCMw?e=XaD4Bv)\n"
    "    - [CHS 2013 Final](https://1drv.ms/b/c/8573c846dfcb547d/EaYgLWPNEwRGkW9fCg5Gs5cB6v2aIbRJJgu0BIeg-qQmSQ?e=aolu6J)\n"
    "    - [Cassel et al. 2012](https://1drv.ms/b/c/8573c846dfcb547d/EXQfdeM3EGZAhFPpiaN8WQ4BDKUmbfMeC1bn_JcCP8o01g?e=b12CFu)\n"
    "    - [HPSS Final](https://1drv.ms/b/c/8573c846dfcb547d/Ea7sluuJfq1Fs9VdlUPtfewBzvp-BCGxP7oC8NS33pXp9w?e=gkwjxN)\n"
)


# Initialize chat session state
if "messages_research" not in st.session_state:
    st.session_state.messages_research = []

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
                st.session_state.messages_research = [{"role": row[0], "content": row[1]} for row in messages]
            del st.session_state.selected_session_id
        except mysql.connector.Error as err:
            st.error(f"Database error: {err}")
        finally:
            conn.close()

# --- Display Chat Messages ---
for message in st.session_state.messages_research:
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

# --- User Input Handling ---
if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages_research.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            with st.spinner("Accounting Researcher is typing..."):
                response = run_flow(user_input)
            placeholder.markdown(response)
        except Exception as e:
            placeholder.markdown("There was an error processing your request.")
            response = "There was an error processing your request."

    st.session_state.messages_research.append({"role": "assistant", "content": response})

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
