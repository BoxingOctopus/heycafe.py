# heycafe SDK – image for running tests and live test scripts
# Python 3.12 (matches minimum supported 3.9; use latest for dev)
FROM python:3.12-slim

WORKDIR /app

# Copy project (pyproject.toml + package + scripts + tests)
COPY pyproject.toml ./
COPY heycafe/ heycafe/
COPY scripts/ scripts/
COPY tests/ tests/

# Install the package and dev/test deps (no editable; simpler in container)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir ".[dev]"

# Default: run live test script (pass env vars at run time)
CMD ["python", "scripts/live_test.py"]
