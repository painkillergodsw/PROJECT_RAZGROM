FROM python:3.13.3-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && \
    pip install --upgrade pip wheel "poetry==2.1.3" && \
    poetry config virtualenvs.create false && \
    apt-get install -y curl && \
    apt-get install -y netcat-openbsd

COPY pyproject.toml poetry.lock ./
COPY . .

RUN poetry install --no-root

RUN chmod +x ./migrate.sh

ENTRYPOINT ["./migrate.sh"]

CMD ["python", "run.py"]