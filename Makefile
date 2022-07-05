.PHONY: requirements.txt requirements-dev.txt

APP = sudoku
TEST = poetry run pytest -x -s -rA --durations=10 -vv --cov $(APP) $(TESTS)
TESTS = tests

all: poetry dephell install

bump-major:
	poetry run bump2version major

bump-minor:
	poetry run bump2version minor

bump-patch:
	poetry run bump2version patch

bump-reset:
	git reset HEAD~1

clean:
	find ./ -type d -name *__pycache__ -exec rm -rf {} \;
	rm .coverage coverage.xml
	rm -rf .pytest_cache htmlcov

cov-reports:
	$(TEST) --cov-report html

cover: cov-reports
	open htmlcov/index.html

cover-codacy: cov-reports
	poetry run coverage xml
	source .env && poetry run python-codacy-coverage -r coverage.xml

install:
	poetry install

lint: pre-commit

POETRY_VERSION = 1.1.8
poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/$(POETRY_VERSION)/get-poetry.py | python

pre-commit:
	poetry run pre-commit run --all-files

release:
	git push && git push --tags

requirements.txt:
	dephell deps converts --envs main --to-format=pip --to-path=$@

requirements-dev.txt:
	dephell deps converts --envs dev --to-format=pip --to-path=$@

run-debug:
	DEBUG=1 FLASK_ENV=development poetry run python $(APP)/app.py

solve:
	poetry run python solve.py

test:
	$(TEST)

vulnerability:
	poetry run safety check
