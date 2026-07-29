FROM python:3.13.3-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
        netcat-openbsd \
        curl && \
    pip install --upgrade pip wheel "poetry==2.1.3" && \
    poetry config virtualenvs.create false && \
    rm -rf /var/lib/apt/lists/*


COPY screenshoot_service/pyproject.toml screenshoot_service/poetry.lock ./

COPY common/ ./common/

COPY screenshoot_service/ ./


RUN poetry install --no-root

RUN playwright install --with-deps chromium


EXPOSE 10000

CMD ["python", "run.py"]