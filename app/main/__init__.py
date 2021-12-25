from flask import Blueprint
main = Blueprint('main', __name__,
                 template_folder="../templates/main_templates",
                 static_folder="../static/main_static",
                 url_prefix='/'
                 )

from . import views  # 咱没有自定义错误页面
