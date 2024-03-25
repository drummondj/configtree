test:
	python -m coverage run --debug=-v -m pytest && coverage html

run:
	python3 main.py

.PHONY: test run