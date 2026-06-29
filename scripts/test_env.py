# Environment Validation and Test Runner - validates environment and runs tests before starting Flask dev server
# Ensures: venv active, Python >= 3.11, requirements up-to-date, tests pass with >95% coverage
import hashlib
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


# Print colored status message
def print_status(message: str, status: str = "info") -> None:
    colors = {
        "success": GREEN,
        "error": RED,
        "warning": YELLOW,
        "info": BLUE,
    }
    color = colors.get(status, RESET)
    print(f"{color}[{status.upper()}]{RESET} {message}")


# Check if virtual environment is active
def check_venv() -> bool:
    in_venv = (
        hasattr(sys, "real_prefix")
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
    )

    if not in_venv:
        print_status(
            "Virtual environment is not active!", "error"
        )
        print_status(
            "Please activate it first:\n"
            "  Windows: venv\\Scripts\\activate\n"
            "  Linux/Mac: source venv/bin/activate",
            "info",
        )
        return False

    venv_path = sys.prefix
    print_status(f"Virtual environment active: {venv_path}", "success")
    return True


# Check if Python version is >= 3.11
def check_python_version() -> bool:
    min_major = 3
    min_minor = 11
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    if sys.version_info.major < min_major or (
        sys.version_info.major == min_major and sys.version_info.minor < min_minor
    ):
        print_status(
            f"Python version too old! Required: >= {min_major}.{min_minor}, Found: {current_version}",
            "error",
        )
        return False

    print_status(f"Python version OK: {current_version} (>= {min_major}.{min_minor})", "success")
    return True


# Calculate SHA256 hash of requirements.txt
def get_requirements_hash() -> str:
    requirements_path = Path("requirements.txt")
    if not requirements_path.exists():
        return ""

    with open(requirements_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# Get path to installed requirements hash file
def get_installed_hash_file() -> Path:
    return Path(".requirements_hash")


# Check if requirements are installed and up-to-date - returns tuple of (requirements_exist, needs_reinstall)
def check_requirements() -> Tuple[bool, bool]:
    requirements_path = Path("requirements.txt")
    if not requirements_path.exists():
        print_status("requirements.txt not found!", "error")
        return False, False

    current_hash = get_requirements_hash()
    hash_file = get_installed_hash_file()

    # Check if hash file exists and matches
    if hash_file.exists():
        stored_hash = hash_file.read_text().strip()
        if stored_hash == current_hash:
            print_status("Requirements are up-to-date", "success")
            return True, False

    # Hash mismatch or file doesn't exist - need to reinstall
    print_status("Requirements hash changed or not installed", "warning")
    print_status("Installing/updating requirements...", "info")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True,
            text=True,
        )
        print_status("Requirements installed successfully", "success")

        # Save new hash
        hash_file.write_text(current_hash)
        return True, True
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to install requirements: {e.stderr}", "error")
        return False, False


# Run pytest with coverage check - returns tuple of (tests_passed, coverage_percentage)
def run_tests() -> Tuple[bool, float]:
    print_status("Running tests with coverage...", "info")

    try:
        # Run pytest with coverage
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "--cov=app",
                "--cov-report=term-missing",
                "--cov-report=json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        # Parse coverage from JSON report
        coverage_file = Path("coverage.json")
        coverage_percent = 0.0

        if coverage_file.exists():
            import json

            with open(coverage_file) as f:
                coverage_data = json.load(f)
                coverage_percent = coverage_data.get("totals", {}).get(
                    "percent_covered", 0.0
                )

        # Print test output
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(result.stderr, file=sys.stderr)

        if result.returncode != 0:
            print_status("Tests failed!", "error")
            return False, coverage_percent

        required_coverage = 95.0
        if coverage_percent < required_coverage:
            print_status(
                f"Coverage {coverage_percent:.2f}% is below required {required_coverage}%",
                "error",
            )
            return False, coverage_percent

        print_status(
            f"All tests passed! Coverage: {coverage_percent:.2f}%", "success"
        )
        return True, coverage_percent

    except FileNotFoundError:
        print_status("pytest not found. Installing...", "warning")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "pytest", "pytest-cov"],
                check=True,
            )
            return run_tests()  # Retry
        except subprocess.CalledProcessError:
            print_status("Failed to install pytest", "error")
            return False, 0.0
    except Exception as e:
        print_status(f"Error running tests: {str(e)}", "error")
        return False, 0.0


# Start Flask development server
def start_flask_server() -> None:
    print_status("Starting Flask development server on port 5000...", "info")
    print_status("Press Ctrl+C to stop the server", "info")
    print_status("API Documentation: http://localhost:5000/apidocs", "info")

    try:
        # Set Flask environment variables
        os.environ["FLASK_APP"] = "app:create_app"
        os.environ["FLASK_ENV"] = "development"
        os.environ["FLASK_DEBUG"] = "1"

        # Start Flask dev server
        subprocess.run(
            [sys.executable, "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"],
            check=True,
        )
    except KeyboardInterrupt:
        print_status("\nServer stopped by user", "info")
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to start server: {str(e)}", "error")
        sys.exit(1)


# Main execution function
def main() -> None:
    print_status("=" * 60, "info")
    print_status("Environment Validation and Test Runner", "info")
    print_status("=" * 60, "info")
    print()

    # Step 1: Check virtual environment
    if not check_venv():
        sys.exit(1)

    # Step 2: Check Python version
    if not check_python_version():
        sys.exit(1)

    # Step 3: Check and install requirements
    reqs_ok, reinstalled = check_requirements()
    if not reqs_ok:
        sys.exit(1)

    # Step 4: Run tests with coverage
    tests_passed, coverage = run_tests()
    if not tests_passed:
        print_status("Tests failed or coverage insufficient. Aborting.", "error")
        sys.exit(1)

    # Step 5: Start Flask server
    print()
    print_status("=" * 60, "info")
    print_status("All checks passed! Starting server...", "success")
    print_status("=" * 60, "info")
    print()

    start_flask_server()


if __name__ == "__main__":
    main()

