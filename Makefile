install:
	pip install -r requirements.txt

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

run:
	uvicorn klingon_transcribe.server:app --host 0.0.0.0 --port 8000 --reload