from flask import Flask
from .core_routes import bp as core_bp
from .watchlist_routes import bp as watchlist_bp
from .movers_routes import bp as movers_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(core_bp)
    app.register_blueprint(watchlist_bp)
    app.register_blueprint(movers_bp)

    return app
