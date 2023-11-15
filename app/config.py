import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '7soino32noonN@^#iuiuw9'

    MONGODB_CONFIG = {
        'production': {
            'MONGODB_SERVER': 'production_server',
            'MONGODB_PORT': 27017,
            'MONGODB_DB': 'production_db',
            'MONGODB_USERNAME': 'production_user',
            'MONGODB_PASSWORD': 'production_password'
        },
        'development': {
            'MONGODB_SERVER': '127.0.0.1',
            'MONGODB_PORT': 27017,
            'MONGODB_DB': 'ComponentStock',
            'MONGODB_USERNAME': 'root',
            'MONGODB_PASSWORD': 'root'
        },
        'api': {
            'MONGODB_SERVER': 'api_server',
            'MONGODB_PORT': 27017,
            'MONGODB_DB': 'api_db',
            'MONGODB_USERNAME': 'api_user',
            'MONGODB_PASSWORD': 'api_password'
        },
        'testing': {
            'MONGODB_SERVER': '127.0.0.1',
            'MONGODB_PORT': 27017,
            'MONGODB_DB': 'ComponentStockTesting',
            'MONGODB_USERNAME': 'root',
            'MONGODB_PASSWORD': 'root'
        }
    }

    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    WTF_CSRF_ENABLED = False

    CSRF_SESSION_KEY = os.getenv('CSRF_SESSION_KEY')

    RATE_LIMITER_OPTS = [ '200 per day', '50 per hour']

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
