import sqlite3
from datetime import datetime

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
            email TEXT,
            member_since TEXT
        )
    ''')
    
    # Check and add columns if missing (for existing databases)
    c.execute("PRAGMA table_info(users)")
    columns = [info[1] for info in c.fetchall()]
    if "email" not in columns:
        c.execute("ALTER TABLE users ADD COLUMN email TEXT")
    if "member_since" not in columns:
        c.execute("ALTER TABLE users ADD COLUMN member_since TEXT")
    
    conn.commit()
    conn.close()

def save_user(username, password, email):
    """Saves a new user to the database with the current date as sign-up date.
    
    Returns True if successful, or False if the username already exists.
    """
    member_since = datetime.now().strftime("%Y-%m-%d")
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, email, member_since) VALUES (?, ?, ?, ?)",
                  (username, password, email, member_since))
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

def get_member_since(username):
    """Retrieves the sign-up date for the given username."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT member_since FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None
