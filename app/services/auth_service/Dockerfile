FROM python:3.13.3-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends openssl gcc libffi-dev netcat-openbsd && \
    pip install --upgrade pip wheel "poetry==2.1.3" && \
    poetry config virtualenvs.create false && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir certs

RUN openssl genrsa -out certs/private.pem 2048 && \
    openssl rsa -in certs/private.pem -outform PEM -pubout -out certs/public.pem

RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
COPY . .

RUN poetry install --no-root

RUN chmod +x ./migrate.sh

ENTRYPOINT ["./migrate.sh"]

CMD ["python", "run.py"]