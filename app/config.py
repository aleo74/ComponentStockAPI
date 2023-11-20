from dotenv import load_dotenv
import os
load_dotenv()

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '7soino32noonN@^#iuiuw9'

    MONGODB_CONFIG = {
        'production': {
            'MONGODB_SERVER': os.getenv('PROD_MONGODB_SERVER'),
            'MONGODB_PORT': os.getenv('PROD_MONGODB_PORT'),
            'MONGODB_DB': os.getenv('PROD_MONGODB_DB'),
            'MONGODB_USERNAME': os.getenv('PROD_MONGODB_USERNAME'),
            'MONGODB_PASSWORD': os.getenv('PROD_MONGODB_PASSWORD'),
        },
        'development': {
            'MONGODB_SERVER': os.environ.get('DEV_MONGODB_SERVER'),
            'MONGODB_PORT': os.environ.get('DEV_MONGODB_PORT'),
            'MONGODB_DB': os.environ.get('DEV_MONGODB_DB'),
            'MONGODB_USERNAME': os.environ.get('DEV_MONGODB_USERNAME'),
            'MONGODB_PASSWORD': os.environ.get('DEV_MONGODB_PASSWORD'),
        },
        'api': {
            'MONGODB_SERVER': os.environ.get('API_MONGODB_SERVER'),
            'MONGODB_PORT': os.environ.get('API_MONGODB_PORT'),
            'MONGODB_DB': os.environ.get('API_MONGODB_DB'),
            'MONGODB_USERNAME': os.environ.get('API_MONGODB_USERNAME'),
            'MONGODB_PASSWORD': os.environ.get('API_MONGODB_PASSWORD'),
        },
        'testing': {
            'MONGODB_SERVER': os.environ.get('TEST_MONGODB_SERVER'),
            'MONGODB_PORT': os.environ.get('TEST_MONGODB_PORT'),
            'MONGODB_DB': os.environ.get('TEST_MONGODB_DB'),
            'MONGODB_USERNAME': os.environ.get('TEST_MONGODB_USERNAME'),
            'MONGODB_PASSWORD': os.environ.get('TEST_MONGODB_PASSWORD'),
        }
    }

    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    WTF_CSRF_ENABLED = False

    CSRF_SESSION_KEY = os.getenv('CSRF_SESSION_KEY')

    RATE_LIMITER_OPTS = ['200 per day', '50 per hour']

    ADMINS = ['admin@gmail.com']

    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    PASSWORD_CHECKER_MIN = 2
    PASSWORD_CHECKER_MAX = 5

    @staticmethod
    def init_app(app):
        pass

    def get_mongo_uri(self, config_name):
        config = self.MONGODB_CONFIG.get(config_name)
        if config:
            return f'mongodb://{config["MONGODB_USERNAME"]}:{config["MONGODB_PASSWORD"]}@{config["MONGODB_SERVER"]}:{config["MONGODB_PORT"]}/{config["MONGODB_DB"]}'
        else:
            return None


class ProductionConfig(Config):
    MONGO_URI = Config().get_mongo_uri('production')


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = Config().get_mongo_uri('development')


class APIConfig(Config):
    WTF_CSRF_ENABLED = False
    MONGO_URI = Config().get_mongo_uri('api')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MONGO_URI = Config().get_mongo_uri('testing')


config = {
    'base': Config,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'api': APIConfig,
}
