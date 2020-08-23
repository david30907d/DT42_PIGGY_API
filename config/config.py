"""
entrypoint of config
"""
import os

from config import dev, prod

LOCATION = globals()[os.getenv("LOCATION", "dev")].LOCATION
