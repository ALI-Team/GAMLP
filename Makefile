EXEC = python

build:
	cp src/*.py gamlp/

test:
	$(EXEC) test.py

clean:
	find . -type f -name '*.pyc' -delete
	rm -rf __pycache__
	rm -rf gamlp/*

