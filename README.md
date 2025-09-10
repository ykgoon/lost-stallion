# Stormhaven - Generative Fiction Engine

## Overview
Stormhaven is a generative fiction tool that creates unique three-line stories inspired by I-Ching hexagrams and Mythic Game Master Emulator Meaning Tables. Each story is generated using a Large Language Model (LLM) with a creative seed derived from ancient wisdom and random elements.

## Features
- Generates unique three-line stories with exactly six words per line
- Creative seeds from I-Ching hexagrams and Mythic GME tables
- Stores generated stories in an SQLite database
- Web interface built with Flask

## Setup

### Local Setup
1. Install `uv` (package manager) if not already installed.
2. Create a virtual environment: `uv venv`
3. Install dependencies: `uv pip install -r requirements.txt`
4. Activate virtual environment: `source .venv/bin/activate`
5. Copy `.env.example` to `.env` and configure your LLM API settings:
   ```
   OPENAI_API_KEY=your_api_key_here
   OPENAI_API_BASE=https://api.openai.com/v1
   OPENAI_MODEL=gpt-3.5-turbo
   ```
6. Run the server: `uv run app.py`

### Docker Setup
1. Build the image: `docker compose build`
2. Run the service: `docker compose up -d`

## Usage
- Access the app at `http://<ip-address>:4732`
- The root endpoint (`/`) displays a list of previously generated stories
- Click "Generate New Story" to create a new story
- Each story is displayed on its own page with a unique URL

## Testing
Run the test suite with:
```
uv run tests/run_tests.py
```

## Dependencies
- Python 3.10+
- uv
- Docker

## Troubleshooting
- Ensure port `4732` is available
- Check Docker logs if running in a container
- Verify your LLM API key is correctly set in the `.env` file
