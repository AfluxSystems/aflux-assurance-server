from aflux_assurance_server import app

def main():
    app.logger.info("Starting flask application")
    app.run(
        host=app.config['FLASK_HOST'],
        port=app.config['FLASK_PORT'],
        debug=app.config['FLASK_DEBUG'],
        #use_reloader=False,
    )
    return app

if __name__ == '__main__':
    main()