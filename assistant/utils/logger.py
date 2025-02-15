import logging.config
import yaml

with open("assistant/config/logging_config.yaml", "r") as f:
    config = yaml.safe_load(f)

logging.config.dictConfig(config)
logger = logging.getLogger("assistant")