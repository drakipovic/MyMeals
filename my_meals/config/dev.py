class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'dev'
