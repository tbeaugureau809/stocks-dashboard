from flask import Flask
from app.routes.core_routes import bp as core_bp
from app.routes.watchlist_routes import bp as watchlist_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(core_bp)
    app.register_blueprint(watchlist_bp)


    for r in app.url_map.iter_rules():
        print("ROUTE", r)

    return app
