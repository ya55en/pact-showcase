VENV_DIR := .venv
PROJECT := todo
TESTS_DIR := tests

venv-clean:
	@rm -rf $(VENV_DIR)

venv-sync:
	@uv venv --prompt $(PROJECT)-backend
	@uv sync

venv-reset:  venv-clean venv-sync


.PHONY: venv-clean venv-sync venv-reset


test:
	@uv run pytest -v

test.quick:
	@uv run pytest -qq $(TESTS_DIR)

test.spec:
	@uv run pytest --spec $(TESTS_DIR)

spec:  test.spec


.PHONY: test test.quick test.spec spec
