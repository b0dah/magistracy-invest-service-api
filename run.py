import connexion
from connexion import RestyResolver
from flask_cors import CORS

from config import FlaskConfig

if __name__ == "__main__":
    connex_app = connexion.FlaskApp(__name__, specification_dir='open_api/')
    connex_app.add_api(
        'openapi.yaml',
        resolver=RestyResolver('api'),
        options={"swagger_ui": FlaskConfig.SWAGGER_UI}
    )

    CORS(connex_app.app)
    connex_app.run(
        host=FlaskConfig.HOST,
        port=FlaskConfig.PORT,
        debug=FlaskConfig.DEBUG
    )
