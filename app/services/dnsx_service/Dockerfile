FROM python:3.13.3-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && \
    pip install --upgrade pip wheel "poetry==2.1.3" && \
    poetry config virtualenvs.create false && \
    apt-get install -y netcat-openbsd wget unzip curl


COPY pyproject.toml poetry.lock ./
COPY . .

ENV DNSX_VERSION=1.2.2

RUN wget https://github.com/projectdiscovery/dnsx/releases/download/v${DNSX_VERSION}/dnsx_${DNSX_VERSION}_linux_amd64.zip && \
    unzip -j -o dnsx_${DNSX_VERSION}_linux_amd64.zip -d /tmp && \
    mv /tmp/dnsx dnsx/ && \
    chmod +x dnsx/dnsx && \
    rm dnsx_${DNSX_VERSION}_linux_amd64.zip


RUN poetry install --no-root

EXPOSE 8230

CMD ["python", "run.py"]