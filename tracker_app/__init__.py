from flask import Flask, redirect, url_for
from tracker_app.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


bcrypt = Bcrypt()
login_manager = LoginManager()

# Other import statements


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    bcrypt.init_app(app)
    login_manager.init_app(app)

    from tracker_app.routes import tracker
    app.register_blueprint(tracker)

    app.register_error_handler(404, page_not_found)

    return app


def page_not_found(e):
    return redirect(url_for("tracker.home"))


