FROM python:3.13.3-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    KATANA_VERSION=1.1.2

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    wget \
    curl \
    ca-certificates \
    unzip \
    chromium \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libx11-6 \
    libxcb1 \
    libxext6 \
    fonts-liberation \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip wheel "poetry==2.1.3" \
    && poetry config virtualenvs.create false \
    && rm -rf /var/lib/apt/lists/*

ENV ROD_BROWSER_BIN=/usr/bin/chromium

COPY katana_service/pyproject.toml katana_service/poetry.lock ./

RUN poetry install --no-root

COPY common/ ./common/
COPY katana_service/ .

RUN mkdir -p /app/katana \
    && wget https://github.com/projectdiscovery/katana/releases/download/v${KATANA_VERSION}/katana_${KATANA_VERSION}_linux_amd64.zip \
        -O /tmp/katana.zip \
    && unzip /tmp/katana.zip -d /app/katana \
    && rm /tmp/katana.zip \
    && chmod +x /app/katana/katana

ENV PATH="/app/katana:${PATH}"

EXPOSE 9002

CMD ["python", "run.py"]