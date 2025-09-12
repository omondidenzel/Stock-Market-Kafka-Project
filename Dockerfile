FROM python:3

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "kafka_producer.py && kafka_consumer.py"]