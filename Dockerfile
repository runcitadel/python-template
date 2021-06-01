FROM python:3.9-slim

RUN pip3 install googleapis-common-protos python-bitcoinrpc grpcio

WORKDIR /app

COPY . .
CMD ["python3", "-u", "main.py"]