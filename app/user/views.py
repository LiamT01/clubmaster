from flask import render_template, session, redirect, url_for, flash, request, jsonify, make_response
from flask_login import login_user, logout_user, login_required, current_user
from . import user
from .forms import SearchClubForm, Register, Login, ChangePasswordForm, NewStoreForm, EditInfoForm
from .. import db
from ..models import User, Club, Message


@user.route('/')
@user.route('/index')
@login_required
def index():
    c = current_user.created_clubs
    m = current_user.joined_clubs
    session['cclubs'] = [x.name for x in c]
    session['mclubs'] = [x.name for x in m]

    return render_template('user_templates/index.html')


@user.route('/messages')
@login_required
def messages():
    return render_template('user_templates/messages.html')


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经登出！')
    return redirect(url_for('main.home'))


@user.route('/user_info')
@login_required
def user_info():
    return render_template('user_templates/user_info.html')


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


@user.route('/create_club', methods=['GET', 'POST'])
@login_required
def create_club():
    form = NewStoreForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if Club.query.get(request.form.get('club_name')):
                flash(u'该社团名称已经存在，请重新创建！')
            else:
                club = Club()
                club.name = form.club_name.data
                club.type = form.club_type.data
                club.description = form.club_desp.data
                club.creator = current_user
                db.session.add(club)
                db.session.commit()
                flash(u'社团创建成功！')
                session['cclubs'] = [club.name for club in current_user.created_clubs.all()]
        else:
            flash(form.errors)
        return redirect(url_for('.create_club'))
    return render_template('user_templates/create_club.html', form=form)


@user.route('/<name>/join_club')
@login_required
def join_club(name):
    club = Club.query.get(name)
    if club.creator == current_user:
        flash("您是该社团的创建者，默认已加入！")
    elif current_user in club.members:
        flash("您已经加入了！")
    else:
        message_temp1 = Message.query.filter_by(sender_id=current_user.id,
                                                receiver_id=club.creator.id,
                                                club_name=club.name,
                                                state='waiting',
                                                type='club_request').first()
        message_temp2 = Message.query.filter_by(sender_id=club.creator.id,
                                                receiver_id=current_user.id,
                                                club_name=club.name,
                                                state='waiting',
                                                type='club_invitation').first()
        if message_temp1:
            flash('您已发送申请，请耐心等待！')
        elif message_temp2:
            flash('该社团社长已向您发送邀请，请前往个人主页的消息中心处理！')
        else:
            message = Message()
            message.sender_id = current_user.id
            message.receiver_id = club.creator.id
            message.club_name = club.name
            message.state = 'waiting'
            message.type = 'club_request'
            db.session.add(message)
            db.session.commit()
            flash('已发送加入申请，请等待社长审核！')
        # club.members.append(current_user)
        # m = current_user.joined_clubs.all()
        # session['mclubs'] = [x.name for x in m]
        # flash("加入成功！")
    return redirect(url_for('.search'))


@user.route('/exit_club', methods=['GET', 'POST'])
@login_required
def exit_club():
    club = Club.query.get(session['club_name'])
    if club:
        for activity in club.activities:
            if current_user in activity.members.all():
                activity.members.remove(current_user)
        club.members.remove(current_user)
        db.session.add_all([club, current_user])
        db.session.commit()
        session['mclubs'] = [x.name for x in current_user.joined_clubs.all()]
        flash('退出社团成功！')
    else:
        flash('该社团不存在！')
    return redirect(url_for('user.search'))


@user.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchClubForm()
    if request.method == 'POST':
        return redirect(url_for('.search', club_name=form.club_name.data, club_type=form.club_type.data))

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

    return render_template('user_templates/search.html', form=form, search_res=clubs)


@user.route('/change_info', methods=['GET', 'POST'])
@login_required
def change_info():
    form = EditInfoForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user.name = form.name.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'已成功修改个人信息！')
        else:
            flash(form.errors)
        return redirect(url_for('.change_info'))
    form.name.data = current_user.name
    id = current_user.id
    return render_template('user_templates/change_info.html', form=form)


@user.route('/handle_club_invitation', methods=['GET', 'POST'])
@login_required
def handle_club_invitation():
    message = Message.query.get(request.args.get('id'))
    action = request.args.get('action')
    if message:
        club = Club.query.get(message.club_name)
        receiver = message.receiver
        if action == 'accept':
            club.members.append(receiver)
            message.state = 'accepted'
            session['mclubs'] = [x.name for x in receiver.joined_clubs.all()]
        elif action == 'reject':
            message.state = 'rejected'
        db.session.add_all([club, receiver, message])
        db.session.commit()
    else:
        flash('该消息不存在！')
    return redirect(url_for('.messages'))


@user.route('/handle_club_request', methods=['GET', 'POST'])
@login_required
def handle_club_request():
    message = Message.query.get(request.args.get('id'))
    action = request.args.get('action')
    if message:
        club = Club.query.get(message.club_name)
        sender = message.sender
        if action == 'accept':
            club.members.append(sender)
            message.state = 'accepted'
        elif action == 'reject':
            message.state = 'rejected'
        db.session.add_all([club, sender, message])
        db.session.commit()
    else:
        flash('该消息不存在！')
    return redirect(url_for('.messages'))
