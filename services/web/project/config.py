import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_MASTER", "postgresql://postgres:admin@postgres:5432/games")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Add environment variables for the replica databases
    REPLICA1_DATABASE_URL = os.getenv("DATABASE_URL_MASTER", "postgresql://postgres:admin@postgres:5432/games")
    REPLICA2_DATABASE_URL = os.getenv("DATABASE_URL_MASTER", "postgresql://postgres:admin@postgres:5432/games")
