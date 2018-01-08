"""
Flask settings, and other custom settings specific to the driver.
"""
import os
# Flask Configuration
# ---------------------------------------------------------------
# NOTE: These three settings are only set in the app via runserver (local development)
#       If you want to use the HOST and PORT in prod, you need to access it in the gunicorn script
FLASK_HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
FLASK_PORT = os.environ.get('FLASK_PORT', 8000)
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', True)

# Email Settings
# -----------------------------------------
RECIPIENT_LIST = (
    'telecom.ns-oss@tdstelecom.com',
)
ERROR_RECIPIENT_LIST = RECIPIENT_LIST

# aflux-assurance-server Settings
# ---------------------------------------------------------------
# Example:
#SNAP_DRIVER_DISABLE_POLLING = os.environ.get('SNAP_DRIVER_DISABLE_POLLING', False)  # Used for satellite services only used for realtime requests

# TSDB Settings
# -----------------------------------------
# TSDB_SETTINGS = {
#     'BASE_URL': os.environ['TSDB_BASE_URL'],  # Ex: http://chewbacca.tds.local:8080
#     'USERNAME': os.environ.get('TSDB_USERNAME', None),
#     'PASSWORD': os.environ.get('TSDB_PASSWORD', None),
# }


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
