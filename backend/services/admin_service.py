from backend.init_database import get_connection
from typing import List

def get_pending_users():
    """Fetch all users with 'pending' status."""
    conn = get_connection()
    if not conn:
        print("❌ Database connection failed")
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, email, full_name, phone_number, status FROM users WHERE status = 'pending'")
        pending_users = cursor.fetchall()
        
        return pending_users

    except Exception as err:
        print(f"❌ Database error: {err}")
        return []
    finally:
        conn.close()


# 🔹 Approve Selected Users
def approve_users(user_ids: List[int]):
    """Approve selected users."""
    if not user_ids:
        return False

    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        format_strings = ', '.join(['%s'] * len(user_ids))
        sql_query = f"UPDATE users SET status = 'approved' WHERE id IN ({format_strings})"
        cursor.execute(sql_query, tuple(user_ids))
        conn.commit()
        return True
    except Exception as err:
        print(f"Database error: {err}")
        return False
    finally:
        conn.close()

# 🔹 Fetch All Users
def get_all_users():
    """Fetch all users with their details."""
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.id, u.full_name, u.email, u.phone_number, u.is_admin, GROUP_CONCAT(c.chatbot) AS allowed_chatbots
            FROM users u
            LEFT JOIN user_chatbot_access c ON u.email = c.user_email
            GROUP BY u.id
        """)
        return cursor.fetchall()
    except Exception as err:
        print(f"Database error: {err}")
        return []
    finally:
        conn.close()

# 🔹 Delete Selected Users
def delete_users(user_ids: List[int]):
    """Delete selected users."""
    if not user_ids:
        return False

    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        format_strings = ', '.join(['%s'] * len(user_ids))
        sql_query = f"DELETE FROM users WHERE id IN ({format_strings})"
        cursor.execute(sql_query, tuple(user_ids))
        conn.commit()
        return True
    except Exception as err:
        print(f"Database error: {err}")
        return False
    finally:
        conn.close()

# 🔹 Update User Chatbots
def update_user_chatbots(email: str, chatbots: List[str]):
    """Update chatbot access for a user."""
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_chatbot_access WHERE user_email = %s", (email,))
        
        if chatbots:
            for chatbot in chatbots:
                cursor.execute("INSERT INTO user_chatbot_access (user_email, chatbot) VALUES (%s, %s)", (email, chatbot))
        
        conn.commit()
        return True
    except Exception as err:
        print(f"Database error: {err}")
        return False
    finally:
        conn.close()
