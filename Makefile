test:
	python -m coverage run --omit 'test/*' -m pytest -vv && coverage html

run:
	python3 main.py

.PHONY: test run