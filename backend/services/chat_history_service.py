import mysql.connector
from backend.init_database import get_connection

def get_chat_sessions(email: str, agent: str):
    """Fetch chat session history for a specific agent and user."""
    conn = get_connection()
    if not conn:
        return [], "Database connection failed"

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT session_id, summary FROM session WHERE user_id = %s AND agent = %s ORDER BY start_timestamp DESC LIMIT 10;",
            (email, agent),
        )
        sessions = [{"session_id": row[0], "summary": row[1]} for row in cursor.fetchall()]
        return sessions, None  # ✅ Return data, no error

    except mysql.connector.Error as err:
        return [], str(err)
    finally:
        conn.close()


def save_chat_session(user_id, messages, agent):
    """Saves a chat session with an agent type and summary in MySQL."""
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            # Extract the first user message (summary)
            first_user_message = next((msg["content"] for msg in messages if msg["role"] == "user"), "No Summary")
            summary = first_user_message[:30]  # Trim to 30 characters max

            # Check for an active session
            cursor.execute(
                "SELECT session_id FROM session WHERE user_id = %s AND agent = %s AND end_timestamp IS NULL",
                (user_id, agent),
            )
            session_result = cursor.fetchone()

            if session_result:
                session_id = session_result[0]
            else:
                # Close any old sessions before creating a new one
                cursor.execute(
                    "UPDATE session SET end_timestamp = CURRENT_TIMESTAMP WHERE user_id = %s AND agent = %s AND end_timestamp IS NULL",
                    (user_id, agent),
                )
                conn.commit()

                # Create a new session with agent name and summary
                cursor.execute(
                    "INSERT INTO session (user_id, agent, summary) VALUES (%s, %s, %s)", 
                    (user_id, agent, summary)
                )
                session_id = cursor.lastrowid

            # Insert new chat messages (skip duplicates)
            for msg in messages:
                cursor.execute(
                    "INSERT INTO message (session_id, role, content) "
                    "SELECT %s, %s, %s WHERE NOT EXISTS "
                    "(SELECT 1 FROM message WHERE session_id = %s AND role = %s AND content = %s)",
                    (session_id, msg["role"], msg["content"], session_id, msg["role"], msg["content"]),
                )

            conn.commit()
            return session_id

    except mysql.connector.Error as err:
        print(f"Error saving chat session: {err}")
        return False
    finally:
        conn.close()
