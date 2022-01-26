import os
import logging

if os.environ.get('VERIFY_TOKEN', None) is None or os.environ.get('PUB_PASSWORD', None) is None or os.environ.get('TOPIC',None) is None:
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.critical("Missing contents from .env file")
    raise ValueError
