.PHONY: build publish


dev:
	pip install .


build:
	pip install -r requirements_dev.txt
	python setup.py sdist bdist_wheel


publish:
	python -m twine upload dist/*
