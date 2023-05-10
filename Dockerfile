FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root --no-dev

# Define build arguments for environment variables
ARG OPENAI_API_KEY
ARG PINECONE_API_KEY
ARG PINECONE_ENVIRONMENT
ARG PINECONE_INDEX_NAME
ARG POSTGRES_SERVER
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
ARG DATABASE_URI

# Create .env from build arguments
RUN echo OPENAI_API_KEY=$OPENAI_API_KEY >> /app/.env && \
    echo PINECONE_API_KEY=$PINECONE_API_KEY >> /app/.env && \
    echo PINECONE_ENVIRONMENT=$PINECONE_ENVIRONMENT >> /app/.env && \
    echo PINECONE_INDEX_NAME=$PINECONE_INDEX_NAME >> /app/.env && \
    echo POSTGRES_SERVER=$POSTGRES_SERVER >> /app/.env && \
    echo POSTGRES_USER=$POSTGRES_USER >> /app/.env && \
    echo POSTGRES_PASSWORD=$POSTGRES_PASSWORD >> /app/.env && \
    echo POSTGRES_DB=$POSTGRES_DB >> /app/.env && \
    echo DATABASE_URI=$DATABASE_URI >> /app/.env

COPY ./app /app
