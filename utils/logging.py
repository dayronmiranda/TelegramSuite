import logging
from logging.handlers import RotatingFileHandler
from config import settings

def setup_logging():
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler = RotatingFileHandler(settings.LOG_FILE, maxBytes=1024 * 1024 * 5, backupCount=5)
    log_handler.setFormatter(log_formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    logger.addHandler(log_handler)
        # Manejo de errores para registrar excepciones
    def log_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.exit(0)
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    # Establecer el manejador de excepciones
    import sys
    sys.excepthook = log_exception

    return logger

logger = setup_logging()