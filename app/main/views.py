from flask import render_template, session, redirect, url_for, flash, request
from flask_login import login_user
from . import main
from .forms import SearchClubForm, Register, Login
from .. import db
from ..models import User, Club, Member, Creator, Admin


@main.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('main_templates/homepage.html', title='Welcome to Club Master')


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if request.method == 'GET':
        return render_template('main_templates/register.html', form=form)
    else:
        if form.validate_on_submit():
            member = Member()
            creator = Creator()
            user = User(as_member=member, as_creator=creator)

            user.stu_id = form.account.data
            user.stu_name = 'jack'
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            flash('用户提交数据通过格式验证')
            return redirect(url_for('.login'))
        else:
            flash(form.errors)
        return render_template('main_templates/register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(stu_id=form.account.data, password=form.password.data).first()
            if user is None:
                flash('账号或密码错误！')
                return redirect(url_for('user.login'))
            else:
                login_user(user)
                session['stu_id'] = user.stu_id
                session['name'] = user.stu_name
                return redirect(url_for('user.index'))

    return render_template('main_templates/login.html', form=form)


@main.route('/all_clubs', methods=['GET', 'POST'])
def all_clubs():
    form = SearchClubForm()
    clubs = Club.query.all()
    if request.method == 'POST':
        club_name = request.form.get('club_name')
        club_type = request.form.get('club_type')
        if club_name != '':
            clubs = Club.query.filter_by(club_name=club_name).all()
        elif club_type != '全部':
            clubs = Club.query.filter_by(club_type=club_type).all()

    clubs = [{'club_name': club.club_name, 'club_type': club.club_type,
              'club_desp': club.club_desp, 'club_creator_id': club.creator.first().id} for club in clubs]

    if request.method == 'POST':
        session['search_res'] = clubs
        session['searched'] = True
        return redirect(url_for('.all_clubs'))

    if not session.get('searched', False):
        session['search_res'] = clubs

    return render_template('main_templates/all_clubs.html', name=session.get('name'), form=form,
                           cclubs=session.get('cclubs'), mclubs=session.get('mclubs'),
                           search_res=session['search_res'])

