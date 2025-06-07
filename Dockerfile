ARG PYTHON_VERSION=3.13-bookworm
FROM python:${PYTHON_VERSION} AS base

# Change to the app directory
WORKDIR /app

# Ensure Poetry installs dependencies system-wide (no venv)
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR=/app/.cache
ENV PYTHONPATH=/app

# Copy dependency files
COPY pyproject.toml poetry.lock README.md /app/

# Install Poetry
RUN pip install --no-cache-dir poetry && \
  poetry install --no-interaction \
  --no-ansi --no-root --only=main

#############################
# === Test Stage ===
#############################
FROM base AS test

# Copy app source and tests
COPY  src /app/src
COPY tests /app/tests

# Install dev dependencies for testing
RUN poetry install --no-interaction \
  --no-ansi --no-root --only=dev

#############################
# === Main Stage ===
#############################
FROM base AS main

# Copy only the app source (no tests)
COPY  src /app/src

# Command to run the main app
CMD ["python", "-m", "src.main"]
