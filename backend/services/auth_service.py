import mysql.connector
from backend.init_database import get_connection
from backend.utils import hash_password

def authenticate_user(email, password):
    """Check if user exists in MySQL, validate password, and ensure they are approved."""
    conn = get_connection()
    if not conn:
        return None, "Database connection failed"

    try:
        cursor = conn.cursor(dictionary=True)
        hashed_password = hash_password(password)

        cursor.execute("SELECT * FROM users WHERE email = %s AND password_hash = %s AND status = 'approved'", 
                       (email, hashed_password))
        user = cursor.fetchone()

        if user:
            return user, "Login successful!"
        else:
            return None, "Invalid email or password"

    except mysql.connector.Error as err:
        return None, str(err)
    finally:
        conn.close()

def store_user_request(first_name, last_name, email, password, phone_number):
    """Stores the user request in the database with status 'pending'."""
    conn = get_connection()
    if not conn:
        return False, "Database connection failed"

    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        full_name = f"{first_name} {last_name}"

        cursor.execute("INSERT INTO users (email, password_hash, full_name, phone_number, status) VALUES (%s, %s, %s, %s, 'pending')",
                       (email, hashed_password, full_name, phone_number))
        conn.commit()
        return True, "Signup request submitted! Pending admin approval."

    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        conn.close()
