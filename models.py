import sqlite3
import json
import uuid
from datetime import datetime
from config import Config

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the stories table."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id TEXT PRIMARY KEY,
            story_text TEXT NOT NULL,
            upper_hexagram TEXT NOT NULL,
            lower_hexagram TEXT NOT NULL,
            seed_words TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_story(story_text, upper_hexagram, lower_hexagram, seed_words):
    """Save a story to the database."""
    story_id = str(uuid.uuid4())
    conn = get_db_connection()

    try:
        conn.execute('''
            INSERT INTO stories (id, story_text, upper_hexagram, lower_hexagram, seed_words)
            VALUES (?, ?, ?, ?, ?)
        ''', (story_id, story_text, upper_hexagram, lower_hexagram, json.dumps(seed_words)))
        conn.commit()
        return story_id
    except Exception as e:
        raise e
    finally:
        conn.close()

def get_stories():
    """Retrieve all stories from the database, ordered by creation date (newest first)."""
    conn = get_db_connection()
    stories = conn.execute('SELECT * FROM stories ORDER BY created_at DESC').fetchall()
    conn.close()
    return stories

def get_story_by_id(story_id):
    """Retrieve a specific story by its ID."""
    conn = get_db_connection()
    story = conn.execute('SELECT * FROM stories WHERE id = ?', (story_id,)).fetchone()
    conn.close()
    return story

def delete_story(story_id):
    """Delete a story from the database by its ID."""
    conn = get_db_connection()

    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM stories WHERE id = ?', (story_id,))
        conn.commit()
        return cursor.rowcount > 0  # Returns True if a row was deleted
    except Exception as e:
        raise e
    finally:
        conn.close()