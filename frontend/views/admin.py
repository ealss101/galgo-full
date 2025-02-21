import streamlit as st
from frontend.services.admin_service import (
    get_pending_users,
    approve_users,
    get_all_users,
    delete_users,
    update_user_chatbots
)

st.header("Admin Panel - User Management")

# --- Approve Pending Users ---
st.subheader("Approve Pending Users")

response_data = get_pending_users()  # ✅ Fetch API response
pending_users = response_data.get("users", [])

if pending_users:
    user_mapping = {user["id"]: f"{user['full_name']} ({user['email']})" for user in pending_users}
    selected_user_ids = st.multiselect(
        "Select users to approve:",
        list(user_mapping.keys()),
        format_func=lambda user_id: user_mapping[user_id]
    )

    if st.button("Approve Selected Users") and selected_user_ids:
        if approve_users(selected_user_ids):
            st.success("✅ Approved users!")
            st.rerun()
else:
    st.info("No pending users.")

# --- Manage Users ---
st.subheader("Manage Users & Chatbot Access")

all_users = get_all_users()

if all_users:
    selected_delete_users = []  # To store users for deletion

    for user in all_users:
        with st.expander(f"🔹 {user['full_name']} ({user['email']})"):
            st.write(f"📞 **Phone:** {user['phone_number'] or 'Not Provided'}")
            st.write(f"🤖 **Allowed Chatbots:** {user['allowed_chatbots'] or 'None'}")

            # ✅ Chatbot selection for user
            available_chatbots = ["All In", "Lawyer's Agent", "Accounting Researcher"]
            selected_chatbots = st.multiselect(
                f"Modify Chatbot Access for {user['full_name']}:",
                options=available_chatbots,
                default=(user['allowed_chatbots'].split(",") if user['allowed_chatbots'] else [])
            )

            # ✅ Apply changes to chatbot access
            if st.button(f"Update Chatbots for {user['full_name']}", key=f"update_{user['id']}"):
                if update_user_chatbots(user["email"], selected_chatbots):
                    st.success(f"✅ Chatbot access updated for {user['full_name']}!")
                    st.rerun()

            # ✅ Checkbox for user deletion
            delete_checkbox = st.checkbox(f"Delete {user['full_name']}", key=f"delete_{user['id']}")
            if delete_checkbox:
                selected_delete_users.append(user["id"])

    # ✅ Delete selected users
    if selected_delete_users and st.button("Delete Selected Users", key="delete_users"):
        if delete_users(selected_delete_users):
            st.success("✅ Selected users have been deleted!")
            st.rerun()

else:
    st.info("No users found.")
