test:
	python -m coverage run -m pytest -v && coverage html

run:
	python3 main.py

.PHONY: test run