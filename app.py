from flask import Flask, render_template, request, redirect, url_for, abort
from generators import get_random_hexagram, map_trigram, select_seed_words
from services import generate_story_with_llm
from models import init_db, get_stories, get_story_by_id, delete_story, save_story

app = Flask(__name__)

@app.route('/')
def index():
    """Display a list of all stories."""
    try:
        init_db()  # Ensure database is initialized
        stories = get_stories()
        return render_template('index.html', stories=stories)
    except Exception as e:
        return f"Error loading stories: {str(e)}", 500

@app.route('/generate')
def generate():
    """Generate a new story."""
    try:
        # Generate hexagram
        hexagram = get_random_hexagram()

        # Split hexagram into upper and lower trigrams
        lower_digits = hexagram[0:3]
        upper_digits = hexagram[3:6]
        lower_trigram_name = map_trigram(lower_digits)
        upper_trigram_name = map_trigram(upper_digits)

        # Select seed words from Mythic GME tables
        seed_words = select_seed_words()

        # Generate story with LLM and verify format
        max_attempts = 5
        attempt = 0
        story_text = ""

        while attempt < max_attempts:
            # Generate story with LLM
            story_text = generate_story_with_llm(upper_trigram_name, lower_trigram_name, seed_words)

            # Verify the story format
            lines = story_text.strip().split('\n')

            # Check if story has exactly 3 lines and each line has no more than 7 words
            if (len(lines) == 3 and
                all(len(line.split()) <= 7 for line in lines)):
                break

            attempt += 1

        # If we exhausted our attempts, return an error
        if attempt >= max_attempts:
            return "Error: Could not generate a story with the correct format after multiple attempts.", 500

        # Save story to database
        story_id = save_story(story_text, upper_trigram_name, lower_trigram_name, seed_words)

        # Redirect to the story page
        return redirect(url_for('story', story_id=story_id))
    except Exception as e:
        return f"Error generating story: {str(e)}", 500

@app.route('/s/<story_id>')
def story(story_id):
    """Display a specific story."""
    try:
        story = get_story_by_id(story_id)
        if story is None:
            abort(404)
        return render_template('story.html', story=story)
    except Exception as e:
        return f"Error loading story: {str(e)}", 500


@app.route('/s/<story_id>', methods=['DELETE'])
def delete_story_route(story_id):
    """Delete a specific story."""
    try:
        success = delete_story(story_id)
        if success:
            return '', 204  # No content
        else:
            return 'Story not found', 404
    except Exception as e:
        return f"Error deleting story: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4732, debug=True)
