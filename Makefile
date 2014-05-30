test: lint
	@py.test -s test

lint:
	flake8 doubles test

bootstrap:
	@pip install -r requirements-dev.txt
	@pip install -e .
