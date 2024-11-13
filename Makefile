.PHONY: install test run clean

install:
	pip install -r requirements.txt

test:
	pytest

run:
	python quantumfuse_node_main.py

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
