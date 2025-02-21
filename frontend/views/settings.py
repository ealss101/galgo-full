import streamlit as st
import mysql.connector
import hashlib
from backend.init_database import get_connection

# Ensure User is Logged In
if "logged_in" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("Please log in to access Settings.")
    st.stop()

st.title("Settings & Profile Management")
st.markdown("Manage your account settings, security, and preferences.")

# 🔹 Function to Fetch User Details
def get_user_details(email):
    """Fetch user details from MySQL."""
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT full_name, email, phone_number, is_admin FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return None
    finally:
        conn.close()

# 🔹 Function to Update User Information
def update_user_info(email, new_email, phone_number):
    """Update user email and phone number in MySQL."""
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE users SET email = %s, phone_number = %s WHERE email = %s",
                           (new_email, phone_number, email))
            conn.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return False
    finally:
        conn.close()

# 🔹 Function to Update User Password
def update_password(email, new_password):
    """Update user password in MySQL."""
    conn = get_connection()
    if not conn:
        return False

    try:
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE users SET password_hash = %s WHERE email = %s", (hashed_password, email))
            conn.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return False
    finally:
        conn.close()

# 🔹 Function to Delete User Account
def delete_user_account(email):
    """Deletes user account from MySQL."""
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE email = %s", (email,))
            conn.commit()
        return True
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return False
    finally:
        conn.close()

# 🔹 Fetch Logged-in User's Data
user_details = get_user_details(st.session_state.user_email)
if not user_details:
    st.error("Unable to retrieve user details.")
    st.stop()

# --- SECTION 1: Personal Information ---
st.header("Personal Information")

full_name = st.text_input("Full Name", value=user_details["full_name"], help="Update your name.")
email = st.text_input("Email Address", value=user_details["email"], help="Update your registered email.")
phone_number = st.text_input("Phone Number", value=user_details["phone_number"] or "", placeholder="Enter your phone number")

if st.button("Save Personal Information"):
    if update_user_info(st.session_state.user_email, email, phone_number):
        st.session_state.user_email = email  # Update session with new email
        st.success("✅ Your personal information has been updated.")

# --- SECTION 2: Security Settings ---
st.header("Security Settings")

new_password = st.text_input("Change Password", type="password", placeholder="Enter a new password")
if st.button("Update Password"):
    if new_password:
        if update_password(st.session_state.user_email, new_password):
            st.success("✅ Password updated successfully!")
    else:
        st.error("Please enter a new password.")

enable_2fa = st.checkbox("Enable Two-Factor Authentication (2FA)", value=False)
if enable_2fa:
    st.info("2FA setup is not yet implemented.")
else:
    st.warning("Your account is less secure without 2FA.")

# --- SECTION 3: Logout ---
st.header("Logout")
if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.allowed_chatbots = []
    st.rerun()

# --- SECTION 4: Delete Account ---
st.header("Delete Account")
if st.button("Delete Account"):
    confirm_delete = st.warning("⚠️ Are you sure? This action **cannot** be undone!")
    if st.button("Yes, Delete My Account"):
        if delete_user_account(st.session_state.user_email):
            st.success("✅ Your account has been permanently deleted.")
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.rerun()
        else:
            st.error("❌ Failed to delete account. Please try again.")
