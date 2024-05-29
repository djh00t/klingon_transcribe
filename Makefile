install:
	pip install pip-tools
	pip-compile requirements.in
	pip-sync

test:
	pip-sync
	pytest

test:
	pytest

lint:
	flake8 klingon_transcribe

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf dist

build:
	python setup.py sdist bdist_wheel

docs:
	pdoc --html --output-dir docs klingon_transcribe
