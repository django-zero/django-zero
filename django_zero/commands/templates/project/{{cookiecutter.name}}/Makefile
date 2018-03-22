### TODO: This file is overriden, move to Projectfile.

.PHONY: install clean

install:
	django-zero install
	yarn install

clean:
    # remove python bytecode
	find . -type d -name __pycache__ | xargs rm -rf

	# remove generated
	rm -rf .cache db.sqlite3 node_modules

