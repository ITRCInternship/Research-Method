
## Overview

This Flask application collects user inputs for a research design questionnaire, sends responses to a Qwen model via Ollama, and returns a structured research method report in Farsi. It also supports user registration and login with data stored in SQLite.

## Prerequisites

- Docker installed, or Python 3.10+ and pip
- Ollama server running and accessible (default `http://localhost:11434/api/chat`)

## Configuration

Environment variables (optional, default values shown):

- `FLASK_SECRET`: Secret key for Flask sessions (default: `change-me`)
- `OLLAMA_URL`: Ollama API endpoint (default: `http://localhost:11434/api/chat`)
- `QUESTIONS_JSON`: Path to questions JSON (default: `questions.json`)
- `FLASK_HOST`: Host to bind (default: `0.0.0.0`)
- `FLASK_PORT`: Port to bind (default: `5003`)
- `FLASK_DEBUG`: Debug mode flag (default: `True`)

## Setup and Run Without Docker

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
    ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:

   ```bash
   flask init-db
   ```
4. Run the application:

   ```bash
   python run.py
   ```
5. Open a browser and navigate to `http://localhost:5003`.

## Build and Run with Docker

1. Build the Docker image:

   ```bash
   docker build -t research-app .
   ```
2. Run a container:

   ```bash
   docker run -d --name research-app-container -p 5003:5003 research-app
   ```
3. Verify the container is running and access the app at `http://localhost:5003`.

## File Descriptions

* **app/**: Contains application modules and templates

  * `__init__.py`: App factory, database initialization
  * `routes.py`: Main routes for questionnaire and summary
  * `ollama_client.py`: Functions to build prompt and call Ollama API
  * `auth.py`: User registration, login, logout
  * **templates/**: HTML templates for pages
* `config.py`: Flask configuration class
* `questions.json`: JSON file defining the questions
* `run.py`: Entry point to start the Flask app
* `requirements.txt`: Python dependencies
* `users.db`: SQLite database file (created by `flask init-db`)

## Usage

1. Register a new user or log in with existing credentials.
2. Proceed through the questionnaire pages.
3. On completion, view the generated research method report.
4. Log out when finished.


