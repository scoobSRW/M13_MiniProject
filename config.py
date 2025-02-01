from TopSecret import SECRET_KEY1, TopSecret


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://root:{TopSecret}@localhost/factory_management_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "SimpleCache"
    DEBUG = True
    SECRET_KEY = SECRET_KEY1
