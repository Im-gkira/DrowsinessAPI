from flask import Flask
from flask_smorest import Api
from app import DrowsyBluePrint


def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "DrowsinessApi"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SECRET_KEY"] = "155045073257778953948945358657168914613"
    api = Api(app)
    api.register_blueprint(DrowsyBluePrint)
    return app


create_app()
