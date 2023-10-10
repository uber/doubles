.PHONY: test
test: clean lint
	@py.test -s -p no:dobles test

.PHONY: lint
lint:
	@flake8 dobles test

.PHONY: clean
clean:
	@find . -type f -name '*.pyc' -exec rm {} ';'

.PHONY: bootstrap
bootstrap:
	@pip install -r requirements-dev.txt
	@pip install -e .

.PHONY: docs
docs:
	@$(MAKE) -C docs html
