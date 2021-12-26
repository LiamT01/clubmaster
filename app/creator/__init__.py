from flask import Blueprint

creator = Blueprint('creator',
                __name__,
                template_folder="../templates/creator_templates",
                static_folder="../static/creator_static",
                url_prefix='/creator')

from . import views