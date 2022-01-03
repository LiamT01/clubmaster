from flask import Blueprint
user = Blueprint('user', __name__,
                 template_folder="../templates/user_templates",
                 static_folder="../static/user_static",
                 url_prefix='/user')

from . import views  # 咱没有自定义错误页面
