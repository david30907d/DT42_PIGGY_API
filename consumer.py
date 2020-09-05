from kafka import KafkaConsumer
import json
consumer = KafkaConsumer('camera',
    bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda x: 
                         x.decode('utf-8'))


for message in consumer:
    print(message.topic, message.key, message.value)