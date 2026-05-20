import sqlite3

# =========================
# DATABASE NAME
# =========================

DB_NAME = "database/history.db"

# =========================
# CREATE CONNECTION
# =========================

def create_connection():

    conn = sqlite3.connect(DB_NAME)

    return conn

# =========================
# CREATE TABLE
# =========================

def create_table():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_name TEXT,
        disease TEXT,
        confidence REAL,
        solution TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    conn.close()

# =========================
# INSERT PREDICTION
# =========================

def insert_prediction(
    image_name,
    disease,
    confidence,
    solution
):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history (
        image_name,
        disease,
        confidence,
        solution
    )
    VALUES (?, ?, ?, ?)
    """, (
        image_name,
        disease,
        confidence,
        solution
    ))

    conn.commit()

    conn.close()

# =========================
# FETCH HISTORY
# =========================

def fetch_history():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM history
    ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows