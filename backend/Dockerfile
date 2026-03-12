FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.12-slim AS runtime

RUN groupadd -r -g 9999 appuser && useradd -r -u 9999 -g appuser appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY app/ app/
COPY migrations/ migrations/
COPY alembic.ini .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

RUN mkdir -p data uploads/avatars uploads/resumes \
    && chown -R appuser:appuser /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER appuser

EXPOSE 8000

CMD ["./entrypoint.sh"]
