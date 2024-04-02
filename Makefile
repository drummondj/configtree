SHELL=bash

define HELP

Use make <target>, where target is one of the following:

install - install libraries and packages
test    - run unit tests
run     - run main webserver

endef

export HELP

help:
	@echo "$$HELP"

test:
	python -m coverage run --omit 'test/*' -m pytest -vv
	coverage html
	coverage-badge -o coverage.svg -f

run:
	python3 main.py

install:
	sudo apt-get install -y python3-tk
	/bin/rm -rf .venv
	python3 -m venv .venv
	cd .venv && source bin/activate
	python -m pip install --upgrade pip
	python -m pip install -r ./environment/requirements.txt

.PHONY: test run install