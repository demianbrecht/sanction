
default: test 

test:
	nosetests -x --with-cov --cov sanction --cov-config\
		.coveragerc --pdb-failures --pdb --cov-report term-missing\
		./tests
	
clean:
	find . -name "*.pyc" | xargs rm

example:
	cd example; python server.py

.PHONY: test clean example 
