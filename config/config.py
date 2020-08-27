"""
entrypoint of config
"""
import os
# Config according to location
if os.getenv('LOCATION') == 'dev':
    from config.dev import PIPELINE, EMAIL_OF_RECEIVER, EMAIL_OF_SENDER
else:
    from config.prod import PIPELINE, EMAIL_OF_RECEIVER, EMAIL_OF_SENDER

# Shared Config
LINE_TOKEN = os.getenv("LINE_TOKEN", "")
GMAIL_TOKEN = os.getenv("GMAIL_TOKEN", '')