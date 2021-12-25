from flask_login import UserMixin
from . import db, login_manager

creator_clubs = db.Table('creator_clubs',
                         db.Column('creator_id', db.Integer, db.ForeignKey('creators.id'), primary_key=True),
                         db.Column('club_id', db.Integer, db.ForeignKey('clubs.club_name'), primary_key=True)
                         )

members_clubs = db.Table('members_clubs',
                         db.Column('member_id', db.Integer, db.ForeignKey('members.id'), primary_key=True),
                         db.Column('club_id', db.Integer, db.ForeignKey('clubs.club_name'), primary_key=True)
                         )

members_activities = db.Table('members_activities',
                         db.Column('member_id', db.Integer, db.ForeignKey('members.id'), primary_key=True),
                         db.Column('activity_id', db.Integer, db.ForeignKey('activities.act_name'), primary_key=True)
                         )


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    stu_id = db.Column(db.String(32), primary_key=True)
    creator_id = db.Column(db.String(32), db.ForeignKey('creators.id'))
    member_id = db.Column(db.String(32), db.ForeignKey('members.id'))
    stu_name = db.Column(db.String(32))
    password = db.Column(db.String(24))
    
    def get_id(self):
        return self.stu_id
    
    def verify_password(self, password):
        return password == self.password
    
    def __repr__(self):
        return '<users %r>' % self.stu_name


class Admin(UserMixin, db.Model):
    _tablename__ = 'admins'
    admin_id = db.Column(db.String(32), primary_key=True)


class Creator(db.Model):
    __tablename__ = 'creators'
    id = db.Column(db.Integer, primary_key=True)
    as_user = db.relationship('User', backref='as_creator', lazy=True, uselist=False)
    created_activities = db.relationship('Activity', backref='creator', lazy='dynamic')


class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    as_user = db.relationship('User', backref='as_member', lazy=True, uselist=False)


class Club(db.Model):
    __tablename__ = 'clubs'
    club_name = db.Column(db.String(32), primary_key=True)
    creator = db.relationship('Creator', secondary=creator_clubs, lazy='dynamic', backref=db.backref('created_clubs', lazy='dynamic'))
    members = db.relationship('Member', secondary=members_clubs, lazy='dynamic', backref=db.backref('joined_clubs', lazy='dynamic'))
    club_type = db.Column(db.String(64))
    club_desp = db.Column(db.String(64))
    # club_creator = db.Column(db.String(64))
    activities = db.relationship('Activity', backref='club', lazy='dynamic')

    def __repr__(self):
        return '<Club %r>' % self.club_name


class Activity(db.Model):
    __tablename__ = 'activities'
    act_name = db.Column(db.String(32), primary_key=True)
    act_desp = db.Column(db.String(64))
    act_time = db.Column(db.String(20))
    limit_num = db.Column(db.Integer())
    members = db.relationship('Member', secondary=members_activities, lazy='dynamic', backref=db.backref('joined_activities', lazy='dynamic'))
    club_name = db.Column(db.String(32), db.ForeignKey('clubs.club_name'))
    creator_id = db.Column(db.Integer, db.ForeignKey('creators.id'))


@login_manager.user_loader
def load_user(stu_id):
    return User.query.get(stu_id)