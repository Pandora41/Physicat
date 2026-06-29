# Production Server Runner - starts Flask application using Gunicorn for production use
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set environment variables
os.environ.setdefault("FLASK_APP", "app:create_app")
os.environ.setdefault("FLASK_ENV", "production")

if __name__ == "__main__":
    import subprocess

    # Get number of workers (default: 4)
    workers = os.environ.get("GUNICORN_WORKERS", "4")
    host = os.environ.get("HOST", "0.0.0.0")
    port = os.environ.get("PORT", "5000")

    # Start Gunicorn
    subprocess.run(
        [
            sys.executable,
            "-m",
            "gunicorn",
            "-w",
            workers,
            "-b",
            f"{host}:{port}",
            "--access-logfile",
            "-",
            "--error-logfile",
            "-",
            "--log-level",
            "info",
            "app:create_app()",
        ],
        check=True,
    )

