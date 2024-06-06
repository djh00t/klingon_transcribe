install:
	pip install pip-tools
	pip-compile requirements.in
	pip-sync
	pip install -e . --use-pep517

test:
	pip-sync
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
	uvicorn klingon_transcribe.main:app --host 0.0.0.0 --port 8000 --reload

docker:
	pip-compile requirements.in
	docker build -t klingon_transcribe:latest .
