FROM krakend:latest

# Устанавливаем рабочую директорию
WORKDIR /etc/krakend

# Копируем конфигурационный файл
COPY krakend.json .

# Открываем порт KrakenD (по умолчанию 8080)
EXPOSE 8080

# Команда запуска KrakenD
CMD ["run", "-c", "krakend.json"]
