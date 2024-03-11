import logging
import sys
from logtail import LogtailHandler

from src.ctrm.config.settings import settings

logger = logging.getLogger()

formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")

stream_handler = logging.StreamHandler(sys.stdout)
logtail = LogtailHandler(source_token=settings.LOGGER_TOKEN)

stream_handler.setFormatter(formatter)

logger.handlers = [stream_handler, logtail]

logger.setLevel(logging.INFO)
