import os
import socket
import logging.config
from .common import ERROR_RECIPIENT_LIST
from aflux_assurance_server import app

# This is overwritten below, but is necessary to init the logger.
# This is because Flask clears any config when it first uses app.logger, so configuration
# changes must be made after the fact.
app.logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

# Create or use an existing log directory located at ~/local/var/log
LOG_DIR = os.path.join(
    os.path.expanduser("~"),
    'local', 'var', 'log'
)
os.makedirs(str(LOG_DIR), exist_ok=True)

# Defined in DictConfig format
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(process)d %(threadName)s %(name)s %(filename)s %(lineno)d: %(message)s',
        },
        'simple': {
            'format': '%(asctime)s [%(levelname)s] %(filename)s %(lineno)d: %(message)s',
        },
    },
    'filters': {},
    'handlers': {
        'standard': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(str(LOG_DIR),"{}.log".format(__name__.split('.')[0])),
            'formatter': 'verbose',
            'maxBytes': 15000,
            'backupCount': 1
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'simple',
        },
        'email': {
            'level': 'CRITICAL',
            'class': 'logging.handlers.SMTPHandler',
            'formatter': 'verbose',
            'mailhost': os.environ.get('EMAIL_SERVER', '127.0.0.1'),
            'fromaddr': '{}@{}'.format(__name__.split('.')[0], socket.getfqdn()),
            'toaddrs': ERROR_RECIPIENT_LIST,
            'subject': 'CRITICAL ERROR - TDS SNAP Driver',
        }
    },
    'loggers': {
        __name__.split('.')[0]: {
            'handlers': ['standard','console','email'],
            'level': os.environ.get('LOG_LEVEL', 'INFO')
        }
    }
}

# Insert the new logging config
logging.config.dictConfig(LOGGING_CONFIG)
