test:
	python -m coverage run --omit 'test/*' -m pytest -vv
	coverage html
	coverage-badge -o coverage.svg -f

run:
	python3 main.py

.PHONY: test run