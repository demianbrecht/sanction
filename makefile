.PHONY: test, lint, example

test:
	nosetests -s --pdb --with-coverage --cover-package=sanction 

lint:
	pylint sanction

example:
	cd example; python server.py
