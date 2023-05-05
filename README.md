# karl-ki-backend

## Installation

We are using [poetry](https://python-poetry.org/) dependency management and packaging in Python. In addition, we take advantage of [uvicorn](https://www.uvicorn.org/) to implement a server. For setting up, run these commands as follows.

One time

- Install Python 3.9≤
- Install [poetry](https://python-poetry.org/docs/#installation)

Every time

```bash
  # Create a virtual environment
  $ poetry shell
  # Install all packages
  $ poetry install
  # Start API server on port = 8000
  $ poetry run uvicorn app.main:app --reload
```

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PROJECT_NAME`

## License

This project is licensed under the terms of the MIT license.
