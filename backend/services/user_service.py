import mysql.connector
from backend.init_database import get_connection

def get_allowed_chatbots(email):
    """Retrieve allowed chatbots for a user from MySQL."""
    conn = get_connection()
    if not conn:
        return [], "Database connection failed"

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT chatbot FROM user_chatbot_access WHERE user_email = %s", (email,))
        allowed_chatbots = [row[0] for row in cursor.fetchall()]
        return allowed_chatbots, None  # ✅ Return chatbots list, no error
    except mysql.connector.Error as err:
        return [], str(err)
    finally:
        conn.close()

def get_admin_status(email):
    """Check if a user is an admin in MySQL."""
    conn = get_connection()
    if not conn:
        return False, "Database connection failed"  # ✅ Always return two values

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT is_admin FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result is None:
            return False, "User not found in database"  # ✅ Ensure 2 values returned
        
        return result.get("is_admin", False), None  # ✅ Always return 2 values

    except mysql.connector.Error as err:
        return False, str(err)  # ✅ Always return 2 values
    finally:
        conn.close()

