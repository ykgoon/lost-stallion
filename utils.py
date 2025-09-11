import os
import json
import uuid
import sqlite3
import requests
from datetime import datetime
from dotenv import load_dotenv
from story_generator import get_random_hexagram, map_trigram, select_seed_words

# Load environment variables
load_dotenv()

def generate_story_with_llm(upper_hexagram, lower_hexagram, seed_words):
    """Generate a story using an LLM API."""
    # Create the prompt
    prompt = f"Generate a three-line short story. Each line makes an act of a three-act story; begin, middle and end. Each line must have exactly six words. The story should be inspired by the hexagrams '{upper_hexagram}' and '{lower_hexagram}', and the following themes: {'; '.join(seed_words)}. Do not write anything else other than the story."

    # Get API configuration from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    api_base = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
    model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

    # Check if API key is provided
    if not api_key:
        return "Error: OPENAI_API_KEY not set in environment variables."

    # Prepare the API request
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': model,
        'messages': [
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 1.8,
        'max_tokens': 150,
        'stream': False
    }

    try:
        # Make the API request
        response = requests.post(f'{api_base}/chat/completions', headers=headers, json=data)
        response.raise_for_status()

        # Extract the story from the response
        result = response.json()
        story = result['choices'][0]['message']['content'].strip()
        return story
    except Exception as e:
        return f"Error generating story: {str(e)}"

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect('data/db.sqlite')
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