test:
	python -m coverage run --debug=-v -m pytest && coverage html

run:
	-pkill python3
	python3 main.py &
	sleep 1
	xdg-open http://127.0.0.1:8050/editor/test/test.json

.PHONY: test run