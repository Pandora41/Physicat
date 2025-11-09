# Makefile for Flask API project
# Provides convenient commands for common tasks

.PHONY: help venv install test run clean docker-build docker-up docker-down

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

venv: ## Create virtual environment
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  Windows: venv\\Scripts\\activate"
	@echo "  Linux/Mac: source venv/bin/activate"

install: ## Install dependencies
	pip install --upgrade pip
	pip install -r requirements.txt

test: ## Run tests with coverage
	pytest -q --cov=app --cov-report=term-missing --cov-report=html

test-env: ## Run environment validation and start server
	python scripts/test_env.py

run: ## Run production server with gunicorn
	python scripts/run.py

dev: ## Run development server
	export FLASK_APP=app:create_app && export FLASK_ENV=development && flask run

clean: ## Clean up generated files
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf coverage.json

docker-build: ## Build Docker image
	docker build -t flask-api .

docker-up: ## Start Docker containers
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f



