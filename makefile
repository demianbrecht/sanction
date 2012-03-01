
default: test 

test:
	nosetests -x --with-cov --cov sanction --cov-config\
		.coveragerc --pdb-failures --pdb --cov-report term-missing\
		./tests
	
ctags:
	ctags -R --c++-kinds=+p --fields=+iaS --extra=+q --python-kinds=-i .

clean:
	find . -name "*.pyc" | xargs rm

.PHONY: test 
