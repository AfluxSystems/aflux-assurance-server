"""
Flask settings, and other custom settings specific to the driver.
"""
import os
from pathlib import Path
# Flask Configuration
# ---------------------------------------------------------------
# NOTE: These three settings are only set in the app via runserver (local development)
#       If you want to use the HOST and PORT in prod, you need to access it in the gunicorn script
FLASK_HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
FLASK_PORT = os.environ.get('FLASK_PORT', 8000)
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', True)

# Email Settings
# -----------------------------------------
RECIPIENT_LIST = ()
ERROR_RECIPIENT_LIST = RECIPIENT_LIST

# aflux-assurance-server Settings
# ---------------------------------------------------------------
# Example:
EMPLOYMENT_FILE = os.environ.get(
    'EMPLOYMENT_FILE',
    default=os.path.join(
        Path(os.path.dirname(os.path.realpath(__file__))).parent,
        'data',
        'employement.json'
    )
)

UPLOAD_FOLDER = os.environ.get(
    'UPLOAD_FOLDER',
    default=os.path.join(
        os.path.expanduser('~'),
        'backups',
    )
)

#  Import Logging Settings
# -----------------------------------------
from .logging_settings import *

# DEPLOYMENT INFORMATION
# ------------------------------------------------------------------------------
DEPLOYED_ENVIRONMENT = os.environ.get('DEPLOYED_ENVIRONMENT', default=None)
BUILD_STABILITY = os.environ.get('BUILD_STABILITY', default=None)
BUILD_VERSION = os.environ.get('BUILD_VERSION', default=None)
BUILD_TIMESTAMP = os.environ.get('BUILD_TIMESTAMP', default=None)
BUILD_APP_UUID = os.environ.get('BUILD_APP_UUID', default=None)
