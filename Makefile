# Variables
PYTHON = python3
PIP = pip3
SRC_DIR = src
TEST_DIR = tests
PYUTGEN = pyutgen

# Default target
all: install build test

# Install dependencies
install:
	$(PIP) install -r requirements.txt

# Build the project (if necessary)
build:
	@echo "Building the project..."
	# Add any build steps here, such as compiling shaders or other components

# Generate test code using pyutgenerator
generate-tests:
	@echo "Generating test code..."
	# Generate test code for each Python file in the source directory
	find $(SRC_DIR) -name "*.py" -exec $(PYUTGEN) {} \;

# Run tests
test: generate-tests
	PYTHONPATH=$(SRC_DIR) pytest $(TEST_DIR)

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
	@echo "Makefile for QuantumFuse Blockchain Project"
	@echo ""
	@echo "Usage:"
	@echo "  make install         Install dependencies"
	@echo "  make build           Build the project"
	@echo "  make generate-tests  Generate test code using pyutgenerator"
	@echo "  make test            Run tests"
	@echo "  make clean           Clean up temporary files"
	@echo "  make lint            Lint the code"
	@echo "  make format          Format the code"
	@echo "  make help            Show this help message"

.PHONY: all install build generate-tests test clean lint format help
