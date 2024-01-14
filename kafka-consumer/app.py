from kafka import KafkaConsumer
import os

consumer = KafkaConsumer(
    'flask-app',
    bootstrap_servers=['kafka-broker:9092'],
    group_id='my-group',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: x.decode('utf-8')
)

os.makedirs('/app/output', exist_ok=True)

for message in consumer:
    with open(f'/app/output/flask-app.txt', 'a') as file:
        file.write(f"{message.value}\n")