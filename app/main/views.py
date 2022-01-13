from flask import render_template, session, redirect, url_for, flash, request
from flask_login import login_user, current_user
from . import main
from .forms import SearchClubForm, Register, Login
from .. import db
from ..models import User, Club, Admin, Activity
import wtforms


@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    login_form = Login()
    register_form = Register()
    return render_template('main_templates/homepage.html',
                           login_form=login_form,
                           register_form=register_form)


@main.route('/register', methods=['POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        if User.query.get(form.account_reg.data) or Admin.query.get(form.account_reg.data):
            flash('该学号已存在！')
        else:
            user = User()
            user.id = form.account_reg.data
            user.name = form.stu_name_reg.data
            user.password = form.password_reg.data
            db.session.add(user)
            db.session.commit()
            flash('注册成功！')
    else:
        flash(form.errors)
    return redirect(url_for('.home'))


@main.route('/login', methods=['POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(id=form.account_login.data, password=form.password_login.data).first()
        user = User.query.filter_by(id=form.account_login.data, password=form.password_login.data).first()
        if user is None and admin is None:
            flash('账号或密码错误！')
            return redirect(url_for('.home'))
        elif user is not None:
            login_user(user)
            return redirect(url_for('user.index'))
        elif admin is not None:
            login_user(admin)
            return redirect(url_for('admin.index'))


@main.route('/all_clubs', methods=['GET', 'POST'])
def all_clubs():
    form = SearchClubForm()
    if request.method == 'POST':
        return redirect(url_for('main.all_clubs', club_name=form.club_name.data, club_type=form.club_type.data))

    club_name = request.args.get('club_name', '', type=str)
    club_type = request.args.get('club_type', '全部', type=str)

    if club_name != '':
        clubs = Club.query.filter_by(name=club_name).order_by(Club.name).all()
    elif club_type != '全部':
        clubs = Club.query.filter_by(type=club_type).order_by(Club.name).all()
    else:
        clubs = Club.query.order_by(Club.name).all()

    form.club_name.data = club_name
    form.club_type.data = club_type

    return render_template('main_templates/all_clubs.html', form=form, search_res=clubs)

@main.route('/about_us')
def about_us():
    clubform = SearchClubForm()
    all_club_types = clubform.club_type.choices[1:]
    typenum = [{'name': clubtype,
                'value':len(Club.query.filter_by(type=clubtype).all())}
               for clubtype in all_club_types]
    allsum = {'users': len(User.query.all()),
              'clubs': len(Club.query.all()),
              'activities': len(Activity.query.all())}
    joinednum = [{'num': sum([1+len(club.members.all())
                              for club in Club.query.filter_by(type=clubtype).all()]),
                  'type': clubtype}
                 for clubtype in all_club_types]
    return render_template('main_templates/about_us.html',
                           charts1=typenum,
                           charts2=joinednum,
                           charts3=allsum)
