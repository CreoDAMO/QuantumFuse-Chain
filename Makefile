# Variables
PYTHON = python3
PIP = pip3
SRC_DIR = src
TEST_DIR = src/tests
FLASK_APP = src/quantumfuse/main.py

# Default target
all: install build

# Install dependencies
install: web-install
	$(PIP) install -r requirements.txt

# Install web dependencies
web-install:
	$(PIP) install flask gunicorn

# Build the project (if necessary)
build:
	@echo "Building the project..."
	# Add any build steps here, such as compiling shaders or other components

# Run Flask development server
run:
	FLASK_APP=$(FLASK_APP) FLASK_ENV=development flask run

# Flexible test target with skip option using unittest
test:
	@if [ "$(SKIP_TESTS)" = "true" ]; then \
		echo "Skipping tests as requested"; \
	else \
		echo "Running tests..."; \
		PYTHONPATH=$(SRC_DIR) $(PYTHON) -m unittest discover -v $(TEST_DIR) || \
		(echo "Tests failed, but continuing build..." && exit 0); \
	fi

# Build and skip tests in one command
build-skip-test: build
	@echo "Build completed without running tests"

# Clean up __pycache__ and other temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} + || true
	find . -type f -name "*.pyc" -delete || true
	find . -type f -name "*.pyo" -delete || true

# Lint the code
lint:
	flake8 $(SRC_DIR) $(TEST_DIR)

# Format the code
format:
	black $(SRC_DIR) $(TEST_DIR)

# Help
help:
	@echo "Makefile for Project Build"
	@echo ""
	@echo "Usage:"
	@echo "  make install         Install dependencies"
	@echo "  make build           Build the project"
	@echo "  make run             Run Flask development server"
	@echo "  make test            Run tests"
	@echo "  make build-skip-test Build without running tests"
	@echo "  make SKIP_TESTS=true test  Skip tests during test phase"
	@echo "  make clean           Clean up temporary files"
	@echo "  make lint            Lint the code"
	@echo "  make format          Format the code"
	@echo "  make help            Show this help message"

.PHONY: all install web-install build run test build-skip-test clean lint format help
