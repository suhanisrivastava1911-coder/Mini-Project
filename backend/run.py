"""Server runner for AI Scheme Sahayak."""
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from backend.app import create_app
from backend.app.config import Config

app = create_app(Config)

if __name__ == "__main__":
    print(f"Starting AI Scheme Sahayak server at http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
