from flask import Blueprint


main = Blueprint('main', __name__)


# 为了避免循环依赖, 必须在末尾导入
from . import views, errors
