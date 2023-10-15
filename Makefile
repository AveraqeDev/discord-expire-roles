POETRY_RUN=poetry run
FORMAT_FILES=discord_role_expire/

env:
	@echo "Copying .env.example to .env"
	cp .env.example .env

install: env
	poetry install

lint:
	${POETRY_RUN} flake8 ${FORMAT_FILES}

format:
	${POETRY_RUN} black ${FORMAT_FILES}

check: format lint

start:
	${POETRY_RUN} python main.py

.PHONY: install lint format check start