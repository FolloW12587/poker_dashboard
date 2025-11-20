.PHONY: test m-create m-up m-down


test:
	@PYTHONPATH=./src uv run pytest -vv

# --- migrations ---

m-create:
	@PYTHONPATH=./src uv run alembic revision --autogenerate -m $(name)

m-up:
	@PYTHONPATH=./src uv run alembic upgrade head

m-down:
	@PYTHONPATH=./src uv run alembic downgrade -1
