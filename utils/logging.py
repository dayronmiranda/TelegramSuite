import logging
from logging.handlers import RotatingFileHandler
from app.config import settings

def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler = RotatingFileHandler(settings.LOG_FILE, maxBytes=1024 * 1024 * 5, backupCount=5)
    log_handler.setFormatter(log_formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    logger.addHandler(log_handler)
    return logger

logger = setup_logging()