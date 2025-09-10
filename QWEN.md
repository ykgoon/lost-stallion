# AGENTS.md

## Agent Onboarding and Operational Guide

### 1. Core Technology Stack

Before making any changes, familiarize yourself with our core technologies:

*   **Programming Language:** Python 3.10+
*   **Package and Environment Management:** `uv`. This project uses `uv` as a replacement for `pip` and `venv`. All package management and script execution should be performed via `uv`.
*   **Deployment & Containerization:** Docker. The application is containerized for consistent development and production environments. All development should be compatible with the existing `Dockerfile`.
*   **Web Framework:** Flask
*   **Database:** SQLite

### 2. Standard Development Workflow

For any given task, you are expected to follow this general workflow:

1.  **Manage Dependencies with `uv`:**
    *   **To Add a New Dependency:** Run `uv pip install <package_name>`.
    *   **To Remove a Dependency:** Run `uv pip uninstall <package_name>`.
    *   **After any change to dependencies, you MUST regenerate the requirements file:** Run `uv pip freeze > requirements.txt`. This ensures the project's dependencies are explicitly locked and reproducible. Do not edit `requirements.txt` manually.

2.  **Test with uv:**
    *   Run Python scripts with `uv run` rather than `python <script.py>`.

3.  **Verify with Docker:** The final state of the codebase must work within the provided Docker environment.
    *   **Build the image:** Use the command `docker build -t <project-name> .` to ensure all dependencies are correctly installed and the application builds successfully.
    *   **Run the container:** If a `docker-compose.yml` file exists, use `docker-compose up`. Otherwise, use the appropriate `docker run` command specified in the project's main `README.md`.

4.  **Final Review:** Before concluding your task, provide a summary of the changes you have made. List all created, modified, and deleted files.

### 3. Environment and Configuration

*   **Environment Variables:** All configuration, secrets, and API keys must be managed through a `.env` file in the project root. Do not hardcode sensitive information. The application should load these variables at runtime.
*   **Database Migrations:** If the project uses a database that requires schema migrations (e.g., PostgreSQL with Alembic), you must generate a new migration file after modifying any database models.

### 4. Coding Standards and Best Practices

*   **Code Style:** All Python code must adhere to the PEP 8 style guide. Use a linter and formatter like `Ruff` or `Black` if configured for this project.
*   **Clarity and Simplicity:** Write code that is easy to read and understand. Favor clear, straightforward logic over complex, "clever" solutions.
*   **Modularity:** Keep functions and classes focused on a single responsibility.
*   **Error Handling:** Implement robust error handling. Do not let the application crash on predictable errors (e.g., invalid user input, failed API calls, database connection issues).
*   **Logging:** Use the standard `logging` module to provide useful output for debugging and monitoring application status.
*   **Comments:** Add comments to explain complex or non-obvious parts of the code. Do not comment on obvious code.

### 5. Agent Interaction Protocol

*   **Ask for Clarification:** If a prompt is ambiguous or lacks necessary details (e.g., an API endpoint URL, a database schema detail), you must ask the user for the missing information before proceeding. This is preferable to making an incorrect assumption.
