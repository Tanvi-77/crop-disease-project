import sqlite3

# =========================
# DATABASE NAME
# =========================

DB_NAME = "database/users.db"

# =========================
# CREATE CONNECTION
# =========================

def create_connection():

    conn = sqlite3.connect(DB_NAME)

    return conn

# =========================
# CREATE USERS TABLE
# =========================

def create_users_table():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()

    conn.close()

# =========================
# REGISTER USER
# =========================

def register_user(username, password):

    conn = create_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """,
            (username, password)
        )

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()

# =========================
# LOGIN USER
# =========================

def login_user(username, password):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=? AND password=?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user