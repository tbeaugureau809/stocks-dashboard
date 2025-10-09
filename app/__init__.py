from flask import Flask
import os

from app.routes.core_routes import bp as core_bp
from app.routes.watchlist_routes import bp as watchlist_bp
from app.routes.movers_routes import bp as movers_bp
from app.routes.charts_routes import bp as charts_bp

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")

    app.register_blueprint(core_bp)
    app.register_blueprint(watchlist_bp)
    app.register_blueprint(movers_bp)
    app.register_blueprint(charts_bp)


    if not app.config.get("TESTING", False):
        from app.services.scheduler_service import start_scheduler
        start_scheduler()
        return app
