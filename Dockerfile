FROM python:3.9-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=$PYTHONPATH:/app/src \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.7 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base as builder
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        ffmpeg \
        libsm6 \
        libxext6 \
        libgl1 \
        libpq5 \
        libglib2.0-0 \
        libxrender1

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR $PYSETUP_PATH
COPY poetry.lock* pyproject.toml ./

ARG DEBUG=false
RUN poetry install $(test ! $DEBUG && echo "--no-dev")

FROM base as development
WORKDIR $PYSETUP_PATH

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

RUN poetry install
COPY . /app
WORKDIR /app