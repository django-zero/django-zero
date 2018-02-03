.PHONY: install clean

install:
	django-zero install
	yarn install

clean:
	find . -type d -name __pycache__ | xargs rm -rf
	rm -rf node_modules
	rm db.sqlite3
	rm -rf .cache

