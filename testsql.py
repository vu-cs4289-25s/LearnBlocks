import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        print("Connection successful!")
        return conn
    except psycopg2.OperationalError as e:
        print("OperationalError:", e, e.args)
        raise
    
print("Database Connected.")

def create_user(role, first_name, last_name, username, email, password_hash):
    """Create a new user and return user_id. Handles duplicate usernames/emails."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute('''
            INSERT INTO "user" (role, first_name, last_name, username, email, password_hash)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING user_id;
        ''', (role, first_name, last_name, username, email, password_hash))
        
        user_id = cur.fetchone()[0]  # Get newly created user ID
        conn.commit()
        return user_id  # Success
    
    except psycopg2.IntegrityError as e:  # Catch duplicate entry error
        conn.rollback()  # Undo any changes
        if "unique constraint" in str(e).lower():
            print("Error: Username or email already exists.")
        else:
            print("Database Error:", e)
        return None  # Indicate failure

    finally:
        cur.close()
        conn.close()  # Ensure connection is closed

test_user_id = create_user(
    role="student",
    first_name="Luca",
    last_name="Antonacci",
    username="loser",
    email="loser@loser.com",
    password_hash="hashedpassword123"
)

if test_user_id:
    print(f"User created! User ID: {test_user_id}")
else:
    print("Failed to create user.")