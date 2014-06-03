test: clean lint
	@py.test -s --cov doubles --cov-report term-missing test

lint:
	flake8 doubles test

clean:
	find . -type f -name '*.pyc' -exec rm {} ';'

bootstrap:
	@pip install -r requirements-dev.txt
	@pip install -e .
