import random
import json

# Trigram symbols mapping
TRIGRAM_SYMBOLS = {
    '乾': '☰',
    '兌': '☱',
    '離': '☲',
    '震': '☳',
    '巽': '☴',
    '坎': '☵',
    '艮': '☶',
    '坤': '☷'
}

def map_trigram(digits):
    """Map a 3-digit sequence to a trigram name."""
    # Convert each digit to yin (0) or yang (1):
    # 6 = old yin, 7 = young yang, 8 = young yin, 9 = old yang
    # For trigram identification, we care about yin/yang regardless of age
    binary = ''.join(['1' if d in '79' else '0' for d in digits])

    # Map binary representation to trigram names
    trigram_map = {
        '111': '乾',  # Heaven
        '110': '兌',  # Lake
        '101': '離',  # Fire
        '100': '震',  # Thunder
        '011': '巽',  # Wind
        '010': '坎',  # Water
        '001': '艮',  # Mountain
        '000': '坤'   # Earth
    }
    return trigram_map.get(binary, '未知')

def get_random_hexagram():
    """Generate a random 6-digit hexagram number."""
    digits = []
    for _ in range(6):
        digit = random.choice(['6', '7', '8', '9'])
        digits.append(digit)
    return ''.join(digits)

def load_mythic_tables():
    """Load the Mythic GME meaning tables from JSON file."""
    try:
        with open('data/mythic_gme_tables.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return empty tables if file not found
        return {table: [] for table in [
            "Actions", "Descriptions", "Characters", "Locations",
            "Objects", "Story Tone", "Legends",
        ]}

def select_seed_words():
    """Select one word from each Mythic GME table."""
    tables = load_mythic_tables()
    seed_words = []

    for table_name, words in tables.items():
        if words:  # Only select if table has words
            word = random.choice(words)
            seed_words.append(f"{table_name}: {word}")
        else:
            seed_words.append("Unknown")

    return seed_words