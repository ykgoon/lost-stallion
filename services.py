import requests
from config import Config

def generate_story_with_llm(upper_hexagram, lower_hexagram, seed_words):
    """Generate a story using an LLM API."""
    # Create the prompt
    prompt = f"""Write a three-act micro-story.
Rules:
- Three lines only.
- Each line must be exactly six words.
- The story must grow from the hexagrams '{upper_hexagram}' and '{lower_hexagram}' and the themes: {'; '.join(seed_words)}.
- All three lines must follow one concrete through-line (character, object, or question).

First, inside your private thoughts, plan:
1. Choose the single through-line.
2. Sketch three beats: introduce → complicate → resolve.
3. Compress each beat into six words.

After planning, output ONLY the three six-word lines.
Do not show headings, commentary, or scratchpad text.
Any text beyond the three lines will be treated as non-compliant.
    """

    # Check if API key is provided
    if not Config.OPENAI_API_KEY:
        return "Error: OPENAI_API_KEY not set in environment variables."

    # Prepare the API request
    headers = {
        'Authorization': f'Bearer {Config.OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': Config.OPENAI_MODEL,
        'messages': [
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 1.8,
        'max_tokens': 150,
        'stream': False
    }

    try:
        # Make the API request
        response = requests.post(
            f'{Config.OPENAI_API_BASE}/chat/completions',
            headers=headers,
            json=data)
        response.raise_for_status()

        # Extract the story from the response
        result = response.json()
        story = result['choices'][0]['message']['content'].strip()
        return story
    except Exception as e:
        return f"Error generating story: {str(e)}"
