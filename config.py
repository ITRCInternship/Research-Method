import os

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET', 'change-me')
    OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/chat')
    QUESTIONS_JSON = os.getenv('QUESTIONS_JSON', 'questions.json')
    DATABASE = os.path.join(os.path.dirname(__file__), 'users.db')