FROM python:3.11-slim AS builder

WORKDIR /app

# Устанавливаем зависимости для сборки (poetry + компиляция)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Копируем манифесты зависимостей
COPY pyproject.toml poetry.lock* /app/

# Настраиваем poetry и ставим зависимости
RUN poetry config virtualenvs.in-project true \
    && poetry install --without dev --no-root --no-interaction --no-ansi


FROM python:3.11-slim AS runtime

WORKDIR /app

# Создаем пользователя
RUN useradd -m appuser

# Устанавливаем curl для healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем виртуальное окружение и код из builder
COPY --from=builder /app/.venv /app/.venv
COPY src /app/src

# Даем права пользователю
RUN chown -R appuser:appuser /app
USER appuser

# Указываем venv в PATH
ENV PATH="/app/.venv/bin:$PATH"

# Экспонируем порт
EXPOSE 8000

# Запускаем uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]