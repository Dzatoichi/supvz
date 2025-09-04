FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root --no-interaction --no-ansi

FROM python:3.11-slim AS runtime
WORKDIR /app

RUN useradd -m appuser

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:${PATH}"

# Копируем исходный код
COPY src /app/src
# Копируем остальные необходимые файлы
COPY migrations /app/migrations
COPY alembic.ini /app/
COPY prestart.sh /app/

# Создаем символическую ссылку для совместимости с импортами
RUN mkdir -p /app/auth_service && \
    ln -s /app/src /app/auth_service/src

RUN chmod +x /app/prestart.sh
EXPOSE 8000
USER appuser

ENTRYPOINT ["/app/prestart.sh"]
CMD ["uvicorn", "auth_service.src.main:app", "--host", "0.0.0.0", "--port", "8000"]