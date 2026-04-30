import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL connection string
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL environment variable not set!")

def get_connection():
    """Get PostgreSQL database connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to PostgreSQL: {str(e)}")
        raise

def get_cursor(conn):
    """Get cursor with row factory for dict-like access"""
    return conn.cursor(cursor_factory=RealDictCursor)

def init_db():
    """Initialize database with gardeners table"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create table using PostgreSQL syntax
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gardeners (
                id SERIAL PRIMARY KEY,
                date TEXT NOT NULL,
                name TEXT NOT NULL,
                task TEXT NOT NULL,
                email TEXT NOT NULL,
                mobile TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✓ Database initialized successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        raise

if __name__ == "__main__":
    init_db()

