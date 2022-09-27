"""Flask configuration."""


# from dotenv import load_dotenv


# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))

class Config:
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'development'
    SECRET_KEY = 'GDtfDCFYjDX'  # environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sql'

    TEMPLATES_FOLDER = "templates",
    STATIC_FOLDER = "static"
