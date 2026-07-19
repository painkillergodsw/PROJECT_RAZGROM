FROM python:3.13.3-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y netcat-openbsd wget unzip curl && \
    pip install --upgrade pip wheel "poetry==2.1.3" && \
    poetry config virtualenvs.create false && \
    rm -rf /var/lib/apt/lists/*

COPY naabu_service/pyproject.toml naabu_service/poetry.lock ./
COPY common/ ./common/
COPY naabu_service/ .


ENV NAABU_VERSION=2.6.1

RUN wget https://github.com/projectdiscovery/naabu/releases/download/v${NAABU_VERSION}/naabu_${NAABU_VERSION}_linux_amd64.zip && \
    unzip -j -o naabu_${NAABU_VERSION}_linux_amd64.zip -d /tmp && \
    mkdir -p naabu && \
    mv /tmp/naabu naabu/naabu && \
    chmod +x naabu/naabu && \
    rm naabu_${NAABU_VERSION}_linux_amd64.zip

RUN poetry install --no-root

EXPOSE 8228

CMD ["python", "run.py"]