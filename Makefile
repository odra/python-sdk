all: bootstrap test install docs-html

install:
	python setup.py install

bootstrap:
	pip install -U -r requirements.txt

freeze:
	pip freeze > requirements.txt

test: bootstrap
	py.test -s

docs-html:
	cd docs && $(MAKE) html
