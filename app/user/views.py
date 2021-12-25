from flask import render_template, session, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import user
from .forms import SearchClubForm, Register, Login, ChangePasswordForm, NewStoreForm, EditInfoForm
from .. import db
from ..models import User, Club, Member, Creator, Activity, Admin

@user.route('/')
@user.route('/index')
@login_required
def index():
    user = User.query.filter_by(stu_id=session.get('stu_id')).first()
    c = user.as_creator.created_clubs
    m = user.as_member.joined_clubs
    session['cclubs'] = [x.club_name for x in c]
    session['mclubs'] = [x.club_name for x in m]

    return render_template('user_templates/index.html', name=session.get('name'),
                           cclubs=session.get('cclubs'),
                           mclubs=session.get('mclubs'))

@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经登出！')
    return redirect(url_for('main.login'))


@user.route('/user/<id>')
@login_required
def user_info(id):
    user = User.query.filter_by(stu_id=id).first()
    return render_template('user_templates/user_info.html', user=user, name=session.get('name'),
                           cclubs=session.get('cclubs'), mclubs=session.get('mclubs'))


@user.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.password2.data != form.password.data:
        flash(u'两次密码不一致！')
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'已成功修改密码！')
            return redirect(url_for('.index'))
        else:
            flash(u'原密码输入错误，修改失败！')
    return render_template("user_templates/change_password.html", form=form)


@user.route('/create_a_club', methods=['GET', 'POST'])
@login_required
def create_club():
    form = NewStoreForm()
    if form.validate_on_submit():
        exist = Club.query.filter_by(club_name=request.form.get('club_name')).first()
        if exist is not None:
            flash(u'该社团名称已经存在，请重新创建。')
        else:
            club = Club()
            club.club_name = request.form.get('club_name')
            club.club_type = request.form.get('club_type')
            club.club_desp = request.form.get('club_desp')
            user = User.query.filter_by(stu_id=current_user.stu_id).first()
            club.creator.append(user.as_creator)
            db.session.add(club)
            db.session.commit()
            flash(u'社团创建成功！')
            creator = User.query.get(current_user.stu_id).as_creator
            # session['cclubs'] = [x.club_name for x in Club.query.filter(Club.creator.id == session.get('stu_id')).all()]
            session['cclubs'] = [club.club_name for club in creator.created_clubs.all()]
    return render_template('user_templates/create_club.html', name=session.get('name'), form=form,
                           cclubs=session.get('cclubs'), mclubs=session.get('mclubs'))

@user.route('/<name>/join_club')
@login_required
def join_club(name):
    club = Club.query.filter_by(club_name=name).first()
    user = User.query.filter_by(stu_id=current_user.stu_id).first()
    if club in user.as_member.joined_clubs:
        flash("你已经加入了！")
    else:
        club.members.append(user.as_member)
        m = user.as_member.joined_clubs
        session['mclubs'] = [x.club_name for x in m]
        flash("成功加入！")
    return redirect(url_for('.search'))

@user.route('/search', methods=['GET', 'POST'])
@login_required
def search():
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
        return redirect(url_for('.search'))

    if not session.get('searched', False):
        session['search_res'] = clubs

    return render_template('user_templates/search.html', name=session.get('name'), form=form,
                           cclubs=session.get('cclubs'), mclubs=session.get('mclubs'),
                           search_res=session['search_res'])

@user.route('/change_info', methods=['GET', 'POST'])
@login_required
def change_info():
    form = EditInfoForm()
    if form.validate_on_submit():
        current_user.stu_name = form.name.data
        db.session.add(current_user)
        db.session.commit()
        session['name'] = current_user.stu_name
        flash(u'已成功修改个人信息！')
        return redirect(url_for('.user_info', id=current_user.stu_id))
    form.name.data = current_user.stu_name
    id = current_user.stu_id
    return render_template('user_templates/change_info.html', form=form, id=id, name=session['name'],
                           cclubs=session.get('cclubs'), mclubs=session.get('mclubs'))