FROM python:3.13.3-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y netcat-openbsd wget unzip curl && \
    pip install --upgrade pip wheel "poetry==2.1.3" && \
    poetry config virtualenvs.create false && \
    rm -rf /var/lib/apt/lists/*

COPY dast/nuclei_service/pyproject.toml dast/nuclei_service/poetry.lock ./
COPY common/ ./common/
COPY dast/nuclei_service/ .

ENV NUCLEI_VERSION=3.6.0

RUN wget https://github.com/projectdiscovery/nuclei/releases/download/v${NUCLEI_VERSION}/nuclei_${NUCLEI_VERSION}_linux_amd64.zip && \
    unzip -j -o nuclei_${NUCLEI_VERSION}_linux_amd64.zip -d /tmp && \
    mkdir -p nuclei && \
    mv /tmp/nuclei nuclei/nuclei && \
    chmod +x nuclei/nuclei && \
    rm nuclei_${NUCLEI_VERSION}_linux_amd64.zip

RUN mkdir -p nuclei/templates/base && \
    wget -q https://github.com/projectdiscovery/nuclei-templates/archive/refs/heads/main.zip \
        -O /tmp/nuclei-templates.zip && \
    unzip -q /tmp/nuclei-templates.zip -d /tmp && \
    cp -r /tmp/nuclei-templates-main/. nuclei/templates/base/ && \
    rm -rf /tmp/nuclei-templates.zip /tmp/nuclei-templates-main

RUN poetry install --no-root

EXPOSE 10013

CMD ["python", "run.py"]
