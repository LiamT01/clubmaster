from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for
from functools import wraps
import random,math,datetime
from flask import render_template, session, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..club.forms import NewStoreForm
from ..models import User, Club, Activity, Message
from . import club
from ..user import user
from .forms import NewActivityForm, ClubInfo, AddMember


@club.route('/')
@club.route('/<name>/index')
@login_required
def index(name):
    session['club_name'] = name
    club = Club.query.get(name)
    session['role'] = 'creator' if club.creator.id == current_user.id else 'member'
    return redirect(url_for('club.club_info'))


@club.route('/club_info')
@login_required
def club_info():
    form = ClubInfo()
    club = Club.query.get(session['club_name'])
    form.club_name.data = club.name
    form.club_type.data = club.type
    form.club_desp.data = club.description
    session['cclubs'] = [x.name for x in current_user.created_clubs]
    return render_template('club_info.html', club=club, name=session.get('club_name'), form=form,
                           cclubs=session.get('cclubs'), mclubs=session.get('mclubs'))


@club.route('/delete_club', methods=['GET', 'POST'])
@login_required
def delete_club():
    club = Club.query.get(request.args.get('name'))
    if club:
        for member in club.members.all():
            message = Message()
            message.sender = current_user
            message.receiver = member
            message.club_name = club.name
            message.type = 'club_deletion'
            message.state = 'waiting'
            message.phase = 'reply'
            db.session.add(message)
        message = Message()
        message.sender = current_user
        message.receiver = current_user
        message.club_name = club.name
        message.type = 'club_deletion'
        message.state = 'done'
        message.phase = 'reply'
        db.session.add(message)
        for activity in club.activities.all():
            db.session.delete(activity)
        db.session.delete(club)
        db.session.commit()
        session['cclubs'].remove(club.name)
        flash('社团删除成功！')
    else:
        flash('该社团不存在！')
    return redirect(url_for('user.index'))


@club.route('/exit_club', methods=['GET', 'POST'])
@login_required
def exit_club():
    club = Club.query.get(session['club_name'])
    if club:
        message = Message()
        message.sender = current_user
        message.receiver = club.creator
        message.club_name = club.name
        message.state = 'waiting'
        message.type = 'exit_club'
        message.phase = 'reply'

        for activity in club.activities:
            if current_user in activity.members.all():
                activity.members.remove(current_user)

        club.members.remove(current_user)
        db.session.add_all([club, current_user, message])
        db.session.commit()
        flash('退出社团成功！')
    else:
        flash('该社团不存在！')
    return redirect(url_for('user.index'))


@club.route('/change_club_info', methods=['GET', 'POST'])
@login_required
def change_club_info():
    form = ClubInfo()
    club = Club.query.get(session['club_name'])
    if club:
        club.type = form.club_type.data
        club.description = form.club_desp.data
        db.session.add(club)
        db.session.commit()
        flash('社团信息更改成功！')
    else:
        flash('该社团不存在！')
    return redirect(url_for('.club_info'))


# @club.route('/personalinfoscr',methods=['POST'])
# @login_required
# def personalinfoscr():
#     return redirect(url_for('club.club_info'))


@club.route('/activity_info',methods=['GET','POST'])
@login_required
def activity_info():
    form = NewActivityForm()
    club = Club.query.get(session['club_name'])
    search_res = Activity.query.filter_by(club_name=session['club_name']).all()
    return render_template('club_templates/activity_info.html', search_res=search_res, club=club, form=form)


@club.route('/add_activity', methods=['GET', 'POST'])
@login_required
def add_activity():
    form = NewActivityForm()
    if form.validate_on_submit():
        if Activity.query.filter_by(name=form.act_name.data,
                                    club_name=session['club_name']).first():
            flash('活动名称不允许重复！')
            return redirect(url_for('club.activity_info'))
        act = Activity()
        act.club_name = session['club_name']
        act.name = form.act_name.data
        act.description = form.act_desp.data
        act.time = form.act_time.data
        act.limit_num = form.limit_num.data
        act.creator_id = current_user.id
        db.session.add(act)
        db.session.commit()
        flash('添加活动成功！')
        return redirect(url_for('club.join_activity', name=act.name))
    else:
        flash(form.errors)
        return redirect(url_for('.activity_info'))


@club.route('/remove_activity', methods=['GET', 'POST'])
@login_required
def remove_activity():
    act = Activity.query.filter_by(name=request.args.get('name'),
                                   club_name=session['club_name']).first()
    if act:
        db.session.delete(act)
        db.session.commit()
        flash('删除活动成功！')
    else:
        flash('该活动不存在！')
    return redirect(url_for('club.activity_info'))


@club.route('/join_activity', methods=['GET', 'POST'])
@login_required
def join_activity():
    act = Activity.query.filter_by(name=request.args.get('name'),
                                   club_name=session['club_name']).first()
    if act:
        if current_user in act.members.all():
            flash('您已加入该活动！')
            return redirect(url_for('club.activity_info'))
        act.members.append(current_user)
        db.session.add(act)
        db.session.commit()
        flash('加入活动成功！')
    else:
        flash('该活动不存在！')
    return redirect(url_for('club.activity_info'))


@club.route('/exit_activity', methods=['GET', 'POST'])
@login_required
def exit_activity():
    act = Activity.query.filter_by(name=request.args.get('name'),
                                   club_name=session['club_name']).first()
    if act:
        if current_user not in act.members.all():
            flash('您已退出该活动！')
            return redirect(url_for('club.activity_info'))
        act.members.remove(current_user)
        db.session.add(act)
        db.session.commit()
        flash('退出活动成功！')
    else:
        flash('该活动不存在！')
    return redirect(url_for('club.activity_info'))


@club.route('/add_member',methods=['GET', 'POST'])
@login_required
def add_members():
    form = AddMember()
    club = Club.query.get(session['club_name'])
    if request.method == "POST":
        user = User.query.get(form.stu_id.data)
        if not user:
            flash("该同学不存在!")
        elif user in club.members.all() or user == club.creator:
            flash("该同学已在社团中！")
        else:
            message_temp1 = Message.query.filter_by(sender_id=current_user.id,
                                                    receiver_id=user.id,
                                                    club_name=club.name,
                                                    type='club_invitation',
                                                    state='waiting',
                                                    phase='request').first()
            message_temp2 = Message.query.filter_by(sender_id=user.id,
                                                    receiver_id=current_user.id,
                                                    club_name=club.name,
                                                    type='club_request',
                                                    state='waiting',
                                                    phase='request').first()
            if message_temp1:
                flash('您已发送邀请，请耐心等待！')
            elif message_temp2:
                flash('该同学已向本社团发送加入申请，请前往个人主页的消息中心进行审核！')
            else:
                message = Message()
                message.sender_id = current_user.id
                message.receiver_id = user.id
                message.club_name = club.name
                message.type = 'club_invitation'
                message.state = 'waiting'
                message.phase = 'request'
                db.session.add(message)
                db.session.commit()
                flash('已发送加入邀请，请等待同学处理！')
            # club.members.append(user)
            # db.session.add(club)
            # db.session.commit()
            # flash("成员添加成功！")
        return redirect(url_for('.add_members'))
    return render_template("add_members.html", club=club, form=form)


@club.route('/remove_members',methods=['GET', 'POST'])
@login_required
def remove_member():
    user = User.query.get(request.args.get('id'))
    club = Club.query.get(session['club_name'])
    if user and club:
        message = Message()
        message.sender = current_user
        message.receiver = user
        message.club_name = club.name
        message.state = 'waiting'
        message.type = 'remove_member'
        message.phase = 'reply'

        for activity in club.activities:
            if user in activity.members.all():
                activity.members.remove(user)

        club.members.remove(user)
        db.session.add_all([message, club, user])
        db.session.commit()
        flash('删除成员成功！')
    else:
        flash('成员或社团不存在！')
    # club = Club.query.filter_by(club_name=session['club_name']).first()
    # if request.method =="POST":
    #     user = User.query.get(form.stu_id.data)
    #     if not user:
    #         flash("该学号不存在")
    #     elif user.as_member in club.members:
    #         flash("该同学已在社团中！")
    #     else:
    #         club.members.append(user.as_member)
    #         flash("成员添加成功！")
    #     return redirect(url_for('.add_members'))
    return redirect(url_for('.member_details'))


@club.route('/member_details')
@login_required
def member_details():
    club = Club.query.get(session['club_name'])
    search_res = club.members.all()
    return render_template('member_details.html', club=club, search_res=search_res)


@club.route('/MemComplaints')
@login_required
def mem_complaint_history():
    club = Club.query.get(session['club_name'])
    complaint_history = []
    return render_template('member_complaints.html', complaint_history=complaint_history, club=club)

@club.route('/ViewFeedbacks')
@login_required
def mem_feedbacks():
    club = Club.query.get(session['club_name'])
    feedbacks = []
    return render_template('manager_feedbacks.html', feedbacks=feedbacks, club=club)



