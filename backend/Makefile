PACKAGE := todoapp
TEST_DIR := tests


test:
	uv run pytest -qq $(TEST_DIR)

spec:
	uv run pytest --spec $(TEST_DIR)

run:
	uv run uvicorn --factory $(PACKAGE).app:create_app --reload


.PHONY: test spec run
