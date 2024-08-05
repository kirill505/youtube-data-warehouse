from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from kafka import KafkaProducer
import json

def send_kafka_message(**kwargs):
    producer = KafkaProducer(bootstrap_servers='broker:29092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    message = {
        'action': 'get_top_videos',
        'regioncode': 'US',
        'limit': 5
    }
    producer.send('youtube_tasks', value=message)
    producer.flush()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag = DAG('daily_youtube_videos', default_args=default_args, schedule_interval='@daily')

send_kafka_message_task = PythonOperator(
    task_id='send_kafka_message',
    provide_context=True,
    python_callable=send_kafka_message,
    dag=dag,
)
