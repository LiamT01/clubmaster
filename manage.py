import os
from app import create_app, db
from app.models import *
from flask_script import Manager, Shell
from app.scripts.CollaborativeFiltering import ItemBasedCF
from app.scripts.simple_rec_pro import UsersRecommend

app = create_app()
manager = Manager(app)
CF = ItemBasedCF()

def make_shell_context():
    return dict(app=app, db=db, User=User, Club=Club, Activity=Activity,
                Message=Message, Admin=Admin, CF=CF, UsersRecommend=UsersRecommend)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
