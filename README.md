# [example-api](https://github.com/Booplicate/example-api) - an example API

The code in this repository is for educational purposes only. An example on how to create a RESTful service using `FastAPI` and `PostgreSQL`.


### Environment variables:
Optional:
- `APP_HOST` (optional if host is provided via the CLI argument)
- `APP_PORT` (optional if port is provided via the CLI argument)
Required:
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `PGHOST`
- `PGPORT`


### Tests:
- `cd` into `example_api`
- Run `python -m unittest discover -v tests --pattern "test_*.py"`


### Stack:
- `Python 3.10.4`
- `fastapi`
- `uvicorn`
- `requests`
- `sqlalchemy` (`asyncpg`)
- `passlib`
