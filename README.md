# I-Ching Web Application

A simple web application for I-Ching divination using Python and HTML.

## Setup

### Local Setup
1. Install `uv` (package manager).
2. Create a virtual environment: `uv venv`.
3. Install dependencies: `uv pip install -r requirements.txt`.
4. Run the server: `python app.py`.

### Docker Setup
1. Build the image: `docker compose build`.
2. Run the service: `docker compose up`.

## Usage
- Access the app at `http://localhost:4732`.
- The root endpoint (`/`) generates a random hexagram and redirects to its details page.

## Dependencies
- Python 3.12
- `iching` package
- Docker (optional)

## Troubleshooting
- Ensure port `4732` is available.
- Check Docker logs if running in a container.
