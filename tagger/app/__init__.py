from config import config
from flask import Flask
from flask_bootstrap import Bootstrap

from app.util.file_manager import FileManager

bootstrap = Bootstrap()
file_manager = FileManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    file_manager.init_app(app)

    # 路由和错误页
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
