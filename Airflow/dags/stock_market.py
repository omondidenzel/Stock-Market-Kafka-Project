from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'akwanybabu',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 14),
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='stock_market',
    default_args=default_args,
    description='A simple stock market DAG',
    schedule=timedelta(days=1)
    ) as dag:

    t1 = EmptyOperator(
        task_id='start'
    )

    run_server = BashOperator(
        task_id='run_server',
        bash_command = f"../../Kafka/bin/kafka-server-start.sh ../../Kafka/config/server.properties"
    )

    kafka_producer = BashOperator(
        task_id='kafka_producer',
        bash_command = f"python ../../kafka_producer.py"
    )

    kafka_consumer = BashOperator(
        task_id='kafka_consumer',
        bash_command = f"python ../../kafka_producer.py"
    )

    t2 = EmptyOperator(
        task_id='end'
    )
   
    t1 >> run_server >> kafka_consumer >> kafka_producer 
    kafka_producer >> t2

