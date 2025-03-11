import sqlite3
import os

DATABASE = "users.db"

def init_db():
    """Initializes the SQLite database and creates/updates the users table."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT
        )
    ''')
    
    # Check if the email column exists; if not, add it.
    c.execute("PRAGMA table_info(users)")
    columns = [info[1] for info in c.fetchall()]
    if "email" not in columns:
        c.execute("ALTER TABLE users ADD COLUMN email TEXT")
    
    conn.commit()
    conn.close()

def save_user(username, password, email):
    """Saves a new user to the database.
    
    Returns True if successful, or False if the username already exists.
    """
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def check_credentials(username, password):
    """Checks if the given username and password match a record in the database."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def get_user_email(username):
    """Retrieves the email address for the given username."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT email FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None
