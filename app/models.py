from flask_login import UserMixin
from . import db, login_manager, admin_id
from datetime import datetime

users_joined_clubs = db.Table('users_joined_clubs',
                         db.Column('member_id', db.String(32), db.ForeignKey('users.id'), primary_key=True),
                         db.Column('club_id', db.String(32), db.ForeignKey('clubs.name'), primary_key=True))

users_activities = db.Table('users_activities',
                         db.Column('user_id', db.String(32), db.ForeignKey('users.id'), primary_key=True),
                         db.Column('activity_id', db.String(32), db.ForeignKey('activities.name'), primary_key=True))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(32))
    password = db.Column(db.String(24))

    created_clubs = db.relationship('Club', backref='creator', lazy='dynamic')
    joined_clubs = db.relationship('Club', secondary=users_joined_clubs, lazy='dynamic',
                                   backref=db.backref('members', lazy='dynamic'))

    created_activities = db.relationship('Activity', backref='creator', lazy='dynamic')
    joined_activities = db.relationship('Activity', secondary=users_activities,
                                        lazy='dynamic', backref=db.backref('members', lazy='dynamic'))

    sent_messages = db.relationship('Message', backref='sender', lazy='dynamic',
                                    foreign_keys='Message.sender_id')
    received_messages = db.relationship('Message', backref='receiver', lazy='dynamic',
                                        foreign_keys='Message.receiver_id')
    
    def get_id(self):
        return self.id
    
    def verify_password(self, password):
        return password == self.password


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(24))
    sent_messages = db.relationship('Message', backref='admin_sender', lazy='dynamic',
                                    foreign_keys='Message.admin_sender_id')
    received_messages = db.relationship('Message', backref='admin_receiver', lazy='dynamic',
                                        foreign_keys='Message.admin_receiver_id')

    def get_id(self):
        return self.id

    def verify_password(self, password):
        return password == self.password


class Club(db.Model):
    __tablename__ = 'clubs'
    name = db.Column(db.String(32), primary_key=True)
    type = db.Column(db.String(64))
    description = db.Column(db.String(64))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    activities = db.relationship('Activity', backref='club', lazy='dynamic')
    timestamp = db.Column(db.DateTime(), default=datetime.now)


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))
    time = db.Column(db.String(20))
    limit_num = db.Column(db.Integer)
    club_name = db.Column(db.String(32), db.ForeignKey('clubs.name'))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin_sender_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    admin_receiver_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    club_name = db.Column(db.String(32))
    club_type = db.Column(db.String(64))
    club_description = db.Column(db.String(64))
    type = db.Column(db.Enum('club_invitation', 'club_request', 'club_creation',
                             'club_deletion', 'remove_member', 'exit_club'))
    state = db.Column(db.Enum('waiting', 'done'))
    action = db.Column(db.Enum('accepted', 'rejected', 'read'))
    phase = db.Column(db.Enum('request', 'reply'))  # Request需要得到回复；reply只是告知receiver，无需对方回复
    timestamp = db.Column(db.DateTime(), default=datetime.now)


@login_manager.user_loader
def load_user(id):
    if id == admin_id:
        return Admin.query.get(id)
    return User.query.get(id)
