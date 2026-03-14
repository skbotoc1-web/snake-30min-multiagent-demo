# Snake 30min Demo

[![CI](https://github.com/skbotoc1-web/snake-30min-multiagent-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/skbotoc1-web/snake-30min-multiagent-demo/actions/workflows/ci.yml)

Minimal Snake in pure Python (keine externen Dependencies).

## Start

```bash
python3 src/snake_game.py
```

Steuerung: `W A S D` + Enter, `q` beendet.

## Tests

```bash
python3 -m unittest discover -s tests -v
```


## Dev checks

```bash
pip install -r requirements-dev.txt
ruff check .
coverage run -m unittest discover -s tests -v
coverage report -m --fail-under=85
```

## Non-interactive Run

```bash
python3 src/snake_game.py --moves WWAASD --seed 42
```

Weitere Optionen:

```bash
python3 src/snake_game.py --help
```


## Highscore

Der beste Score kann gespeichert werden:

```bash
python3 src/snake_game.py --moves WWAASD --highscore-file .snake/highscore.txt
```

Zurücksetzen:

```bash
python3 src/snake_game.py --reset-highscore --moves DD
```


## Makefile Targets

```bash
make setup
make lint
make test
make coverage
```
