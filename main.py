import streamlit as st
import requests
from frontend.services.user_service import fetch_admin_status, fetch_allowed_chatbots

API_URL = "http://127.0.0.1:8000"  # Update when deploying

# --- Ensure Session State Variables Exist ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "allowed_chatbots" not in st.session_state:
    st.session_state.allowed_chatbots = []
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False  # Default to non-admin

# 🔹 Fetch Admin Status if User is Logged In
if st.session_state.logged_in and st.session_state.user_email:
    st.session_state.is_admin = fetch_admin_status(st.session_state.user_email)
    st.session_state.allowed_chatbots = fetch_allowed_chatbots(st.session_state.user_email)

# --- PAGE SETUP ---
PAGES = {
    "Login/Sign Up": st.Page("frontend/views/login_signup.py", title="Login/Sign Up", icon=":material/login:", default=True),
    "About Us": st.Page("frontend/views/about_us.py", title="About Us", icon=":material/info:"),
    "All In Chatbot": st.Page("frontend/views/chat_bot.py", title="𝐀ll 𝐈n", icon=":material/robot:"),
    "Accounting Research": st.Page("frontend/views/accounting_research_chat_bot.py", title="Accounting Researcher", icon=":material/psychology:"),
    "Lawyer's Agent": st.Page("frontend/views/law_agent_chat_bot.py", title="Lawyer's Agent", icon=":material/gavel:"),
    "Settings": st.Page("frontend/views/settings.py", title="Settings", icon=":material/settings:"),
    "Instructions": st.Page("frontend/views/instructions.py", title="How it Works", icon=":material/list:"),
    "Dashboard": st.Page("frontend/views/dashboard.py", title="Dashboard", icon=":material/analytics:"),
    "Contact Us": st.Page("frontend/views/contact_us.py", title="Contact Us", icon=":material/contact_support:"),
    "Terms & Privacy": st.Page("frontend/views/terms.py", title="Terms & Privacy", icon=":material/verified_user:"),
    "Chat History": st.Page("frontend/views/chat_history.py", title="Chat History", icon=":material/history:"),
    "Admin": st.Page("frontend/views/admin.py", title="Admin", icon=":material/shield:"),
}

# --- Dynamically Adjust Sidebar Based on Allowed Chatbots & Admin Status ---
feature_pages = []
if "All In" in st.session_state.allowed_chatbots:
    feature_pages.append(PAGES["All In Chatbot"])
if "Accounting Researcher" in st.session_state.allowed_chatbots:
    feature_pages.append(PAGES["Accounting Research"])
if "Lawyer's Agent" in st.session_state.allowed_chatbots:
    feature_pages.append(PAGES["Lawyer's Agent"])

# --- Account Pages Setup ---
account_pages = [
    PAGES["Chat History"],
    PAGES["Dashboard"],
    PAGES["Settings"],
    PAGES["Terms & Privacy"]
]

# --- Ensure Login Page is Visible When Not Logged In ---
if not st.session_state.logged_in:
    account_pages.insert(0, PAGES["Login/Sign Up"])
elif st.session_state.is_admin:
    account_pages.insert(0, PAGES["Admin"])  # Insert Admin at the top

# --- NAVIGATION SETUP ---
pg = st.navigation(
    {
        "Account": account_pages,
        "Galgo AI Features": feature_pages,
        "Info": [PAGES["About Us"], PAGES["Instructions"], PAGES["Contact Us"]],
    }
)

# --- Chatbot Access Control (Only Restrict Account & Galgo AI Features Sections) ---
restricted_sections = ["Account", "Galgo AI Features"]

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    current_page = st.session_state.get("current_page", "")
    if any(current_page.startswith(page) for page in restricted_sections):
        st.warning("Please log in to access these features.")
        st.stop()

with st.sidebar:
    if st.session_state.logged_in:
        st.markdown(f"👤 **{st.session_state.user_email}**")

# --- Sidebar Chatbot Selection ---
with st.sidebar.expander("**Start a New Chat**", expanded=False):
    for chatbot in st.session_state.allowed_chatbots:
        if st.button(chatbot, key=f"new_{chatbot}_sidebar"):
            st.session_state.messages_simple = []

            # ✅ Use explicit string paths instead of .path (which doesn't exist)
            if chatbot == "All In":
                st.switch_page("frontend/views/chat_bot.py")
            elif chatbot == "Lawyer's Agent":
                st.switch_page("frontend/views/law_agent_chat_bot.py")
            elif chatbot == "Accounting Researcher":
                st.switch_page("frontend/views/accounting_research_chat_bot.py")



# --- RUN NAVIGATION ---
pg.run()
