import os
from app import create_app, db
from app.models import User, Creator, Member, Club, Activity
from flask_script import Manager, Shell

app = create_app()
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Creator=Creator, Member=Member, Club=Club, Activity=Activity)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
