import sqlite3
from pathlib import Path

# Database file path
DB_PATH = Path(__file__).parent.parent / "gardeners.db"

def get_connection():
    """Get database connection"""
    return sqlite3.connect(str(DB_PATH))

def init_db():
    """Initialize database with gardeners table"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gardeners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            name TEXT NOT NULL,
            task TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
