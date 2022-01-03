from flask import Blueprint
admin = Blueprint('admin', __name__,
                  template_folder="../templates/admin_templates",
                  static_folder="../static/admin_static",
                  url_prefix='/admin')

from . import views  # 咱没有自定义错误页面
