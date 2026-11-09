FROM python:3.13-slim

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

# Run as non-root
RUN useradd --create-home appuser
USER appuser

CMD ["chronometer"]
