from os import path


# from dotenv import load_dotenv


# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))

class Config:
    TESTING = True
    SECRET_KEY = 'GDtfDCFYjDX'  # environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sql'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TEMPLATES_FOLDER = 'templates',
    STATIC_FOLDER = 'static'

    VIDEOS_JSON_URL = 'https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1/raw/04441487d90a0a05831835413f5942d58026d321/videos.json'

    DATA_FOLDER = path.join(path.dirname(path.abspath(__file__)), 'data')
