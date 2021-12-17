from flask import Blueprint
main = Blueprint('main', __name__,
                 template_folder="../templates/auth_templates",
                 static_folder="../static/auth_static",
                 url_prefix='/'
                 )

from . import views  # 咱没有自定义错误页面
