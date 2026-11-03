import os
from pathlib import Path

def _load_env_file(filepath: Path):
    """Fallback manual .env parser if python-dotenv is not installed."""
    if not filepath.exists():
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                clean_key = key.strip()
                clean_val = val.strip().strip('"').strip("'")
                if clean_key not in os.environ:
                    os.environ[clean_key] = clean_val

# Try dotenv first, fallback to native parser
env_file = Path(__file__).resolve().parent / '.env'
try:
    from dotenv import load_dotenv
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
except ImportError:
    _load_env_file(env_file)

class Config:
    """Matrix Device Configuration Class."""
    DEVICE_IP = os.getenv('MATRIX_DEVICE_IP', '192.168.1.20')
    DEVICE_PORT = int(os.getenv('MATRIX_DEVICE_PORT', 80))
    ADMIN_PIN = os.getenv('MATRIX_ADMIN_PIN', '1234')
    USER_LEVEL = int(os.getenv('MATRIX_USER_LEVEL', 0))
    TIMEOUT = int(os.getenv('REQUEST_TIMEOUT_SECONDS', 5))
    EXPORT_DIR = os.getenv('EXPORT_DIRECTORY', './exports')

    @classmethod
    def base_url(cls) -> str:
        return f"http://{cls.DEVICE_IP}:{cls.DEVICE_PORT}"

    @classmethod
    def submit_url(cls) -> str:
        return f"{cls.base_url()}/cgi-bin/submit"
