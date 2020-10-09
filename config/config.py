"""
entrypoint of config
"""
import os
# Config according to location
LOCATION = os.getenv('LOCATION')
if LOCATION == 'dev':
    from config.dev import PIPELINE, EMAIL_OF_RECEIVER, EMAIL_OF_SENDER, KAFKA_CONFIG
elif LOCATION == 'pytest':
    from config.pytest import PIPELINE, EMAIL_OF_RECEIVER, EMAIL_OF_SENDER, KAFKA_CONFIG
else:
    from config.prod import PIPELINE, EMAIL_OF_RECEIVER, EMAIL_OF_SENDER, KAFKA_CONFIG

# Shared Config
LINE_TOKEN = os.getenv("LINE_TOKEN", "")
GMAIL_TOKEN = os.getenv("GMAIL_TOKEN", '')
SECRET = os.getenv('SECRET', '')