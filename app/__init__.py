from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # initialise plugin
    db.init_app(app)

    with app.app_context():
        from app.routes import main_bp
        app.register_blueprint(main_bp)

        # create db schema
        db.create_all()

        return app
