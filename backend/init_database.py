import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),  # Your Lightsail Public IP
            user=os.getenv("MYSQL_USER"),  # MySQL Username
            password=os.getenv("MYSQL_PASSWORD"),  # MySQL Password
            database=os.getenv("MYSQL_DATABASE"),  # Database Name
            port=int(os.getenv("MYSQL_PORT", 3306))  # Ensure port is an integer (default 3306)
        )
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Database Connection Error: {err}")
        return None

