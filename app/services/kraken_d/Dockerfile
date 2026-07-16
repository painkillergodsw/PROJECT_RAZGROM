FROM krakend:latest

WORKDIR /etc/krakend

COPY krakend.json .

EXPOSE 8080

CMD ["run", "-c", "krakend.json"]
