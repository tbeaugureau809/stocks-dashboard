from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    # load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")

    # import and register routes
    from .routes import bp
    app.register_blueprint(bp)

    return app
