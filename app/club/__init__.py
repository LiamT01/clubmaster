from flask import Blueprint

club = Blueprint('club',
                __name__,
                template_folder="../templates/club_templates",
                static_folder="../static/club_static",
                url_prefix='/club')

from . import views