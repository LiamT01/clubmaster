from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

admin_id = 'admin'
basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'main.login'
login_manager.login_message = u"请先登录。"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hard to guess string'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['JSON_AS_ASCII'] = False
    #app.config.from_object(config[config_name])
    #config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    # 附加路由
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .club import club as club_blueprint
    app.register_blueprint(club_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    return app
