"""
entrypoint of config
"""
import os
if os.getenv('LOCATION') == 'dev':
    from config.dev import PIPELINE
else:
    from config.prod import PIPELINE
LINE_TOKEN = os.getenv("LINE_TOKEN", "")
