
ALL: run
.PHONY: run update packages


run:
	bundle exec jekyll serve

update:
	bundle update

packages:
	python3 update.py > packages/index.html

