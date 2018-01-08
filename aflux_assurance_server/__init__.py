"""This is where all Flask blueprints are registered with the central app."""
__version__ = "0.0.1"

import os
from flask import Flask
from aflux_assurance_server.api.v1 import api as api_v1
#from aflux_assurance_server.utils.jobs import PrimaryFlaskWorker

app = Flask(__name__)

# Get location of settings file to use
aflux_assurance_server_settings = os.environ.get(
    'AFLUX_ASSURANCE_SERVER_SETTINGS',  # Environment variable
    'aflux_assurance_server.config.production'  # Default settings file to use
)

# Load settings file
app.config.from_object(aflux_assurance_server_settings)
app.logger.info("aflux-assurance-server is initializing")
app.logger.debug("aflux-assurance-server is using settings: {}".format(
    aflux_assurance_server_settings
))

# Here you can initialize any other components of your app.
# For example, a scheduler. You can even attach the object to the app instance.


# Register API blueprints
app.register_blueprint(api_v1, url_prefix='/api/v1')

# Load any remaining top-level views not under API versioning
import aflux_assurance_server.views
