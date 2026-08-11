FROM python:3.13.3-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y netcat-openbsd wget unzip curl && \
    pip install --upgrade pip wheel "poetry==2.1.3" && \
    poetry config virtualenvs.create false && \
    rm -rf /var/lib/apt/lists/*

COPY dast/httpx_service/pyproject.toml dast/httpx_service/poetry.lock ./
COPY common/ ./common/
COPY dast/httpx_service/ .

ENV HTTPX_VERSION=1.7.0

RUN wget https://github.com/projectdiscovery/httpx/releases/download/v${HTTPX_VERSION}/httpx_${HTTPX_VERSION}_linux_amd64.zip && \
    unzip -j -o httpx_${HTTPX_VERSION}_linux_amd64.zip -d /tmp && \
    mkdir -p httpx && \
    mv /tmp/httpx httpx_sdk/httpx && \
    chmod +x httpx_sdk/httpx && \
    rm httpx_${HTTPX_VERSION}_linux_amd64.zip

RUN poetry install --no-root

EXPOSE 8228

CMD ["python", "run.py"]