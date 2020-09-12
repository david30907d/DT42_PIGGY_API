"""
config of prod
"""
from kafka import KafkaProducer
import json
import os
class Pipeline():
    def __init__(self):
        self.output = [None]

    def run(self, frame, external_meta=None, benchmark=False):
        print(f'run {self.output}')
        self.output[0] = frame

PIPELINE = Pipeline()
# BUG: wait for jocelyn to fix it!
# from trainer.pipelines import pipeline as dt42pl
# PIPELINE = dt42pl.Pipeline(
#     "config/demo.config",
#     trainer_config_path="",
#     parent_result_folder="",
#     verbosity=0,
#     lab_flag=False,
# )
EMAIL_OF_SENDER = os.getenv("EMAIL_OF_SENDER", '')
EMAIL_OF_RECEIVER = os.getenv("EMAIL_OF_RECEIVER", '')
KAFKA_CONFIG = {
    "producer": KafkaProducer(bootstrap_servers=['host.docker.internal:9092', '172.17.0.1:9092'],
                         value_serializer=lambda x: 
                         json.dumps(x).encode('utf-8'))
}