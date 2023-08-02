# NeoFacturing-backend

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

To run this project, you will need to add the following environment variables to your .env file:

`PROJECT_NAME`
`AUTH_SECRET_KEY`
`DECODING_ALGORITHM`
`ACCESS_TOKEN_EXPIRE_MINUTES`
`ENV`
`AZURE_STORAGE_CONNECTION_STRING`
`LANGCHAIN_PROJECT`
`LANGCHAIN_TRACING_V2`
`LANGCHAIN_ENDPOINT`
`LANGCHAIN_API_KEY`
`OPENAI_API_KEY`
`OPENAI_API_BASE`
`OPENAI_API_VERSION`
`NGROK_URL`

## Testing

Our git workflow assesses functions with pytest. Tests directory defines all tests by following the same structure in the app directory. Every time users merge branches, .github/workflows/ci.yml file detects errors in codes.
To run the tests execute the following command:

```bash
    poetry run pytest
```

## Docker

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed on your machine.

### Building the Docker Image

```bash
    docker-compose build
```

### Starting the Container

```bash
    docker-compose up
```

### Stopping the Container

To stop the running containers, press Ctrl+C in the terminal where the docker-compose up command is running or run the following command:

```bash
    docker-compose down
```

## License

This project is licensed under the terms of the MIT license.
