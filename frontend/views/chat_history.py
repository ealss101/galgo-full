import streamlit as st
from frontend.services.chat_history_service import fetch_chat_sessions

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("Please log in to see Chat History.")
    st.stop()

st.title("Chat History")

# --- Define Available Chatbot Features ---
chatbot_features = {
    "All In": "frontend/views/chat_bot.py",
    "Accounting Researcher": "frontend/views/accounting_research_chat_bot.py",
    "Lawyer's Agent": "frontend/views/law_agent_chat_bot.py",
}

# --- Select a Chatbot Feature ---
selected_chatbot = st.radio("**Select your agent:**", chatbot_features.keys())

# --- Fetch Chat Sessions from API ---
session_options = {}

if selected_chatbot:
    email = st.session_state.get("user_email")  # ✅ Get email from session
    chat_sessions = fetch_chat_sessions(email, selected_chatbot)  # ✅ Fetch from FastAPI
    
    session_options = {session["session_id"]: session["summary"] for session in chat_sessions}  # ✅ Convert to dictionary

# --- Display Dropdown for Chat History ---
if selected_chatbot and session_options:
    selected_chat = st.selectbox("Choose a previous session:", list(session_options.keys()), format_func=lambda x: f"{session_options[x]}")

    if st.button("Load Chat"):
        st.session_state.selected_session_id = selected_chat
        st.session_state.messages = []  # Clear messages
        st.switch_page(chatbot_features[selected_chatbot])  # Redirect to selected chatbot
        st.rerun()

else:
    st.warning("No chat sessions found for this agent. Start a new conversation!")
