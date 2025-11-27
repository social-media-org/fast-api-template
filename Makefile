.PHONY: help install run run-docker stop test format lint type-check clean

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
UVICORN := uvicorn
APP_MODULE := app.main:app

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run: ## Run the application locally
	$(UVICORN) $(APP_MODULE) --reload --host 0.0.0.0 --port 8000

run-docker: ## Run the application with Docker Compose
	docker-compose up --build

stop: ## Stop Docker containers
	docker-compose down

test: ## Run tests (placeholder)
	@echo "Tests not implemented yet. Add pytest to requirements.txt and create tests."
	# pytest tests/ -v

format: ## Format code with ruff
	$(PIP) install ruff
	ruff format app/

lint: ## Lint code with ruff
	$(PIP) install ruff
	ruff check app/

type-check: ## Type check with mypy
	$(PIP) install mypy
	mypy app/

clean: ## Clean cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

dev: install ## Setup development environment
	@echo "Development environment ready!"
	@echo "Run 'make run' to start the server"
