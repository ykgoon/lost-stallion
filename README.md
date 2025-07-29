# 周易動爻

A simple web application for I-Ching divination.

## Setup

### Local Setup
1. Install `uv` (package manager).
2. Create a virtual environment: `uv venv`.
3. Install dependencies: `uv pip install -r requirements.txt`.
4. Activate virtual environment: `source .venv/bin/activate`.
4. Run the server: `python app.py`.

### Docker Setup
1. Build the image: `docker compose build`.
2. Run the service: `docker compose up -d`.

## Usage
- Access the app at `http://<ip-address>:4732`.
- The root endpoint (`/`) generates a random hexagram and redirects to its details page.

## Dependencies
- Python 3.10
- Docker (optional)

## Troubleshooting
- Ensure port `4732` is available.
- Check Docker logs if running in a container.
