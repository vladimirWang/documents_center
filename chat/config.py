import sys
from pathlib import Path

from dotenv import load_dotenv

CHAT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CHAT_DIR.parent
SERVER_DIR = PROJECT_ROOT / "server"
ENV_PATH = SERVER_DIR / ".env"


def setup() -> None:
    load_dotenv(ENV_PATH)
    server_path = str(SERVER_DIR)
    if server_path not in sys.path:
        sys.path.insert(0, server_path)


setup()
