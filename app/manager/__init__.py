from flask import Blueprint

manager = Blueprint('manager',
                __name__,
                template_folder="../templates/manager_templates",
                static_folder="../static/manager_static",
                url_prefix='/manager')

from . import views