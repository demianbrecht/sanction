.PHONY: test, lint, example

test:
	rm -f .coverage
	nosetests -s --with-coverage --cover-package=sanction 

lint:
	pylint sanction

example:
	cd example; python server.py
