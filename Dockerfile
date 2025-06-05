ARG PYTHON_VERSION=3.13-bookworm
FROM python:${PYTHON_VERSION} AS base

# Change to the app directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Ensure Poetry installs dependencies system-wide (no venv)
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR=/app/.cache
ENV PYTHONPATH=/app

# Copy dependency files
COPY pyproject.toml poetry.lock README.md /app/

# Install only runtime dependencies (no dev)
RUN poetry install --no-interaction --no-ansi --no-root --only=main

#############################
# === Test Stage ===
#############################
FROM base AS test

# Copy app source and tests
COPY  src /app/src
COPY tests /app/tests

# Install dev dependencies for testing
RUN poetry install --no-interaction --no-ansi --no-root

# Run pytest with coverage (you can override this in CI if needed)
CMD ["poetry", "run", "pytest", "--cov=src", "--cov-report=term"]

#############################
# === Main Stage ===
#############################
FROM base AS main

# Install Playwright browsers (Chromium only)
RUN playwright install chromium --with-deps

# Copy only the app source (no tests)
COPY  src /app/src

# Command to run the main app
CMD ["poetry", "run", "python", "-m", "src.main"]
