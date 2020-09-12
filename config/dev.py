"""
config of dev
"""
from kafka import KafkaProducer
import json
import os
class Pipeline():
    def __init__(self):
        self.output = [None]

    def run(self, frame, external_meta=None, benchmark=False):
        self.output[0] = frame

PIPELINE = Pipeline()
EMAIL_OF_SENDER = os.getenv("EMAIL_OF_SENDER", 'davidtnfsh.dt42@gmail.com')
EMAIL_OF_RECEIVER = os.getenv("EMAIL_OF_RECEIVER", 'davidtnfsh.dt42@gmail.com')
KAFKA_CONFIG = {
    "producer": KafkaProducer(bootstrap_servers=['host.docker.internal:9092', '172.17.0.1:9092'],
                         value_serializer=lambda x: 
                         json.dumps(x).encode('utf-8'))
}