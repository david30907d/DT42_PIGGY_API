"""
config of prod
"""
from kafka import KafkaProducer
import json
from trainer.pipelines import pipeline as dt42pl
PIPELINE = dt42pl.Pipeline(
    "config/demo.config",
    trainer_config_path="",
    parent_result_folder="",
    verbosity=0,
    lab_flag=False,
)
EMAIL_OF_SENDER = ''
EMAIL_OF_RECEIVER = ''
KAFKA_CONFIG = {
    "producer": KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         json.dumps(x).encode('utf-8'))
}