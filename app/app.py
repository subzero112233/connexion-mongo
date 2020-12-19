import connexion
import logging

logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__, options={"swagger_ui": False})
app.add_api('api/openapi.yaml')
application = app.app

if __name__ == '__main__':
    app.run(port=8080, server='gevent')
