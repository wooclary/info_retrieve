import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DATA_PATH = './app/html_data/'
    DATA_EXTRA = 'html_data/'
    DATA_EXT = '.htm'
    RESULT_FILE = './app/result/tag_result.txt'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
