.PHONY: setup lint test coverage run run-script ci

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements-dev.txt

lint:
	. .venv/bin/activate && ruff check .

test:
	. .venv/bin/activate && python -m unittest discover -s tests -v

coverage:
	. .venv/bin/activate && coverage run -m unittest discover -s tests -v && coverage report -m --fail-under=85

run:
	python3 src/snake_game.py

run-script:
	python3 src/snake_game.py --moves WWAASDD --seed 42

ci: lint coverage
