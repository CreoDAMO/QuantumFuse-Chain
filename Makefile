# Makefile for QuantumFuse Blockchain Project

# Variables
PYTHON = python3
PIP = pip3
SRC_DIR = src
TEST_DIR = tests

# Default target
all: install

# Install dependencies
install:
	$(PIP) install -r requirements.txt

# Run the QuantumFuse node
run:
	$(PYTHON) $(SRC_DIR)/quantumfuse_node.py

# Run tests
test:
	@if [ -d "$(TEST_DIR)" ]; then \
		pytest $(TEST_DIR); \
	else \
		echo "Test directory not found."; \
	fi

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
	@echo "  make install     Install dependencies"
	@echo "  make run         Run the QuantumFuse node"
	@echo "  make test        Run tests"
	@echo "  make clean       Clean up temporary files"
	@echo "  make lint        Lint the code"
	@echo "  make format      Format the code"
	@echo "  make help        Show this help message"

.PHONY: all install run test clean lint format help
