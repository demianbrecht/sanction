.PHONY: test, lint, example

test:
	nosetests -s --with-coverage --cover-package=sanction 

lint:
	pylint sanction

example:
	cd example; python server.py
