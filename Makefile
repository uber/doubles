test: clean lint
	@py.test -s -p no:doubles test

lint:
	flake8 doubles test

clean:
	find . -type f -name '*.pyc' -exec rm {} ';'

bootstrap:
	@pip install -r requirements-dev.txt
	@pip install -e .

.PHONY: docs
docs:
	$(MAKE) -C docs html
