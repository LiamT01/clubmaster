from flask import render_template, session, redirect, url_for, flash, request
from flask_login import login_user, current_user
from . import main
from .forms import SearchClubForm, Register, Login
from .. import db
from ..models import User, Club, Member, Creator, Admin
import wtforms


@main.route('/', methods=['GET', 'POST'])
@main.route('/welcome', methods=['GET', 'POST'])
def home():
    login_form = Login()
    register_form = Register()
    return render_template('main_templates/homepage.html',
                           login_form=login_form,
                           register_form=register_form)


@main.route('/register', methods=['POST'])
def register():
    form = Register()
    # if request.method == 'GET':
    #     return render_template('main_templates/register.html', form=form)
    # else:
    #     if form.validate_on_submit():
    #         member = Member()
    #         creator = Creator()
    #         user = User(as_member=member, as_creator=creator)
    #
    #         user.stu_id = form.account_reg.data
    #         user.stu_name = 'jack'
    #         user.password = form.password_reg.data
    #         db.session.add(user)
    #         db.session.commit()
    #         flash('用户提交数据通过格式验证')
    #         return redirect(url_for('.home'))
    #     else:
    #         flash(form.errors)
    #     return render_template('main_templates/register.html', form=form)
    if form.validate_on_submit():
        member = Member()
        creator = Creator()
        user = User(as_member=member, as_creator=creator)
        if User.query.get(form.account_reg.data):
            flash('学号已存在！')
        else:
            user.stu_id = form.account_reg.data
            user.stu_name = form.stu_name_reg.data
            user.password = form.password_reg.data
            db.session.add(user)
            db.session.commit()
            flash('用户提交数据通过格式验证！')
    else:
        flash(form.errors)
    return redirect(url_for('.home'))


@main.route('/login', methods=['POST'])
def login():
    # form = Login()
    # if request.method == 'POST':
    #     if form.validate_on_submit():
    #         user = User.query.filter_by(stu_id=form.account.data, password=form.password.data).first()
    #         if user is None:
    #             flash('账号或密码错误！')
    #             return redirect(url_for('main.login'))
    #         else:
    #             login_user(user)
    #             session['stu_id'] = user.stu_id
    #             session['name'] = user.stu_name
    #             return redirect(url_for('user.index'))
    #
    # return render_template('main_templates/login.html', form=form)
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(stu_id=form.account_login.data, password=form.password_login.data).first()
        if user is None:
            flash('账号或密码错误！')
            return redirect(url_for('.home'))
        else:
            login_user(user)
            # session['stu_id'] = user.stu_id
            # session['name'] = user.stu_name
            return redirect(url_for('user.index'))
    # else:
    #     for error_msg in form.errors.values():
    #         flash(error_msg[0])
    #     return redirect(url_for('main.home'))


@main.route('/all_clubs', methods=['GET', 'POST'])
def all_clubs():
    form = SearchClubForm()
    if request.method == 'POST':
        return redirect(url_for('main.all_clubs', club_name=form.club_name.data, club_type=form.club_type.data))

    club_name = request.args.get('club_name', '', type=str)
    club_type = request.args.get('club_type', '全部', type=str)

    if club_name != '':
        clubs = Club.query.filter_by(club_name=club_name).order_by(Club.club_name).all()
    elif club_type != '全部':
        clubs = Club.query.filter_by(club_type=club_type).order_by(Club.club_name).all()
    else:
        clubs = Club.query.order_by(Club.club_name).all()

    form.club_name.data = club_name
    form.club_type.data = club_type

    return render_template('main_templates/all_clubs.html', form=form, search_res=clubs)

@main.route('/about_us')
def about_us():
    return render_template('main_templates/about_us.html')
