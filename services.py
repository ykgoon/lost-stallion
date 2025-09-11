import requests
from config import Config

def generate_story_with_llm(upper_hexagram, lower_hexagram, seed_words):
    """Generate a story using an LLM API."""
    # Create the prompt
    prompt = f"Generate a three-line short story. Each line makes an act of a three-act story; begin, middle and end. Each line must have exactly six words. The story should be inspired by the hexagrams '{upper_hexagram}' and '{lower_hexagram}', and the following themes: {'; '.join(seed_words)}. Do not write anything else other than the story."

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
        response = requests.post(f'{Config.OPENAI_API_BASE}/chat/completions', headers=headers, json=data)
        response.raise_for_status()

        # Extract the story from the response
        result = response.json()
        story = result['choices'][0]['message']['content'].strip()
        return story
    except Exception as e:
        return f"Error generating story: {str(e)}"