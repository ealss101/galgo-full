import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # Change this for deployment

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "full_name" not in st.session_state:
    st.session_state.full_name = ""

# --- LOGIN / SIGN-UP PAGE ---
st.header("Login or Sign Up")

# Dropdown to select between Login and Sign-Up
auth_option = st.selectbox("Choose an option:", ["Login", "Sign Up"])

# --- LOGIN FORM ---
if auth_option == "Login":
    st.subheader("Login to Your Account")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            response = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
            
            if response.status_code == 200:
                user_data = response.json()

                # ✅ Store session info
                st.session_state.logged_in = True
                st.session_state.user_email = user_data["user"]["email"]
                st.session_state.full_name = user_data["user"]["full_name"]
                st.session_state.is_admin = user_data["user"]["is_admin"]
                st.success(f"🎉 Welcome back, {st.session_state.full_name}!")
                st.rerun()  


# --- SIGN-UP FORM ---
elif auth_option == "Sign Up":
    st.subheader("Request a New Account")
    with st.form("signup_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        phone_number = st.text_input("Phone Number")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        signup_button = st.form_submit_button("Sign Up Request")

        if signup_button:
            if password != confirm_password:
                st.error("❌ Passwords do not match.")
            else:
                response = requests.post(f"{API_URL}/auth/signup", json={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone_number": phone_number,
                    "password": password
                })
                if response.status_code == 200:
                    st.success("✅ Sign-up request submitted! Pending admin approval.")
                else:
                    st.error("🚨 Error during sign-up. Try again.")

# --- Logout Option ---
if st.session_state.logged_in:
    st.success(f"Logged in as {st.session_state.user_email}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.full_name = ""
        st.rerun()
