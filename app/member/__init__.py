from flask import Blueprint

member = Blueprint('member',
                __name__,
                template_folder="../templates/member_templates",
                static_folder="../static/member_static",
                url_prefix='/member')

from . import views