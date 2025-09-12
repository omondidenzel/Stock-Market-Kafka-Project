from kafka import KafkaConsumer
import pandas as pd
from time import sleep
from json import dumps
import json
from s3fs import S3FileSystem
import logging, sys

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

consumer = KafkaConsumer(
    'demo_test',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

s3 = S3FileSystem(anon=False)

for count, message in enumerate(consumer):
    try:
        with s3.open('s3://kafka-stock-market-denzel/consumed_data_{}.json'.format(count), 'w') as f:
            json.dump(message.value, f)
            # f.write(dumps(message.value) + '\n')
    except Exception as e:
        log.error(f"Error writing to S3: {e}")
    finally:
        log.info(f"Written data to S3: {message.value}")


