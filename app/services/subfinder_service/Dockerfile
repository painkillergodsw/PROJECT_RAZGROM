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

ENV SUBFINDER_VERSION=2.8.0

RUN wget https://github.com/projectdiscovery/subfinder/releases/download/v${SUBFINDER_VERSION}/subfinder_${SUBFINDER_VERSION}_linux_amd64.zip && \
    unzip -j -o subfinder_${SUBFINDER_VERSION}_linux_amd64.zip -d /tmp && \
    mv /tmp/subfinder subfinder/ && \
    chmod +x subfinder/subfinder && \
    rm subfinder_${SUBFINDER_VERSION}_linux_amd64.zip


RUN poetry install --no-root

EXPOSE 8230

CMD ["python", "run.py"]