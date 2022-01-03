from flask import render_template, session, redirect, url_for, flash, request, jsonify, make_response
from flask_login import login_user, logout_user, login_required, current_user
from . import admin
from .forms import SearchClubForm, Register, Login, ChangePasswordForm, NewStoreForm, EditInfoForm
from .. import db
from ..models import User, Club, Message


@admin.route('/')
@admin.route('/index')
@login_required
def index():
    return render_template('admin_templates/index.html')


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经登出！')
    return redirect(url_for('main.home'))


@admin.route('/review_clubs')
@login_required
def review_clubs():

    return render_template('admin_templates/review_clubs.html')


@admin.route('/search', methods=['GET', 'POST'])
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

    return render_template('admin_templates/search.html', form=form, search_res=clubs)


@admin.route('/delete_club', methods=['GET', 'POST'])
@login_required
def delete_club():
    club = Club.query.get(request.args.get('name'))
    if club:
        for member in [*club.members.all(), club.creator]:
            message = Message()
            message.admin_sender = current_user
            message.receiver = member
            message.club_name = club.name
            message.type = 'club_deletion'
            message.state = 'waiting'
            message.phase = 'reply'
            db.session.add(message)
        db.session.delete(club)
        db.session.commit()
        flash('社团删除成功！')
    else:
        flash('该社团不存在！')
    return redirect(url_for('.search'))


@admin.route('/handle_club_invitation', methods=['GET', 'POST'])
@login_required
def handle_club_invitation():
    message = Message.query.get(request.args.get('id'))
    action = request.args.get('action')
    if message:
        club = Club.query.get(message.club_name)
        receiver = message.receiver

        reply_message = Message()
        reply_message.sender = message.receiver
        reply_message.receiver = message.sender
        reply_message.club_name = message.club_name
        reply_message.type = message.type
        reply_message.state = 'waiting'
        reply_message.phase = 'reply'

        if action == 'accept':
            club.members.append(receiver)
            message.state = 'done'
            reply_message.action = message.action = 'accepted'
            session['mclubs'] = [x.name for x in receiver.joined_clubs.all()]
        elif action == 'reject':
            message.state = 'done'
            reply_message.action = message.action = 'rejected'
        db.session.add_all([club, receiver, message, reply_message])
        db.session.commit()
    else:
        flash('该消息不存在！')
    return redirect(url_for('.messages'))


@admin.route('/handle_club_creation', methods=['GET', 'POST'])
@login_required
def handle_club_creation():
    message = Message.query.get(request.args.get('id'))
    action = request.args.get('action')
    if message:
        reply_message = Message()
        reply_message.admin_sender = message.admin_receiver
        reply_message.receiver = message.sender
        reply_message.type = message.type
        reply_message.club_name = message.club_name
        reply_message.state = 'waiting'
        reply_message.phase = 'reply'
        if action == 'accept':
            club = Club()
            club.name = message.club_name
            club.type = message.club_type
            club.description = message.club_description
            club.creator = message.sender
            db.session.add(club)
            message.state = 'done'
            reply_message.action = message.action = 'accepted'
        elif action == 'reject':
            message.state = 'done'
            reply_message.action = message.action = 'rejected'
        db.session.add_all([current_user, message.sender, message, reply_message])
        db.session.commit()
    else:
        flash('该消息不存在！')
    return redirect(url_for('.review_clubs'))


@admin.route('/handle_reply_message', methods=['GET', 'POST'])
@login_required
def handle_reply_message():
    message = Message.query.get(request.args.get('id'))
    if message:
        message.state = 'done'
        db.session.add(message)
        db.session.commit()
    else:
        flash('该消息不存在！')
    return redirect(url_for('.messages'))
