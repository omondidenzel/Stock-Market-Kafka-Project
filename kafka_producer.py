from kafka import KafkaProducer
import pandas as pd
from time import sleep
from json import dumps
import logging, sys
import json

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

param = {
    'bootstrap_servers': ['localhost:9092'],
    'value_serializer': lambda x: dumps(x).encode('utf-8'),  
}

producer = KafkaProducer(
    bootstrap_servers=param['bootstrap_servers'],
    value_serializer=param['value_serializer']
)

df = pd.read_csv('Data/indexProcessed.csv')

log.info(f"DataFrame loaded with shape: {df.shape} and columns: {df.columns.tolist()} \n")

df.columns  = [x.lower() for x in df.columns]
log.info(f"Columns after lowercasing: {df.columns.tolist()}")


while True:
    dict_stocks = df.sample(1).to_dict(orient='records')[0]
    try:
        producer.send('demo_test', value=
            dict_stocks
        )
    except Exception as e:
        log.error(f"Error sending data: {e}")
    finally:
        producer.flush()

    log.info(f"Sent data: {dict_stocks}")

