FROM python:3.13-slim AS base

# Pinned uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# 1) Install dependencies only (cached layer)
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

# 2) Copy source and install the project
COPY README.md ./
COPY src ./src
RUN uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"


# Test image: `docker build --target test -t chronometer-test .`
FROM base AS test

# Add the dev dependency group (pytest, etc.)
RUN uv sync --locked
COPY tests ./tests

CMD ["pytest"]


# App image (default target; must stay the last stage)
FROM base AS app

# Run as non-root
RUN useradd --create-home appuser
USER appuser

CMD ["chronometer"]
