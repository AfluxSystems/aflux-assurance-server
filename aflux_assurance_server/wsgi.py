"""File to hook into gunicorn for production deployments."""
from aflux_assurance_server import app


if __name__ == '__main__':
    app.run()