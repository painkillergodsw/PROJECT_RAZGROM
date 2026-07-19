FROM python:3.13.3-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FEROXBUSTER_VERSION=2.11.0

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        netcat-openbsd wget curl ca-certificates tar \
    && pip install --upgrade pip wheel "poetry==2.1.3" \ 
    && poetry config virtualenvs.create false \
    && rm -rf /var/lib/apt/lists/*

COPY feroxbuster_service/pyproject.toml feroxbuster_service/poetry.lock ./

RUN poetry install --no-root
COPY common/ ./common/

COPY feroxbuster_service/ .

RUN wget https://github.com/epi052/feroxbuster/releases/download/v${FEROXBUSTER_VERSION}/x86_64-linux-feroxbuster.tar.gz -O /tmp/feroxbuster.tar.gz \
    && tar -xvzf /tmp/feroxbuster.tar.gz -C feroxbuster \
    && rm /tmp/feroxbuster.tar.gz \
    && chmod +x feroxbuster/feroxbuster

EXPOSE 8232

CMD ["python", "run.py"]
