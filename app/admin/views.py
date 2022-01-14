from flask import render_template, session, redirect, url_for, flash, request, jsonify, make_response
from flask_login import login_user, logout_user, login_required, current_user
from . import admin
from .forms import SearchClubForm, Register, Login, ChangePasswordForm, NewStoreForm, EditInfoForm
from .. import db
from ..models import User, Club, Message, Activity
import random, time
from collections import Counter
import numpy as np

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
        for activity in club.activities.all():
            db.session.delete(activity)
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

def timestamp2str(timestamp):
    return '{:%Y-%m-%d %H:%M}'.format(timestamp)

def pos_rd():
    return random.random() * 800 - 400

@admin.route('/data_visualization', methods=['GET', 'POST'])
@login_required
def data_visualization():
    clubform = SearchClubForm()
    all_club_types = clubform.club_type.choices[1:]
    nodes, links, categories = [], [], []
    node_member, node_club = {}, []
    ctime_club = {}
    for clubtype in all_club_types:
        categories.append({'name':clubtype})
        cate_id = len(categories) - 1
        for club in Club.query.filter_by(type=clubtype).all():
            if ctime_club.get(timestamp2str(club.timestamp)) is None:
                ctime_club[timestamp2str(club.timestamp)] = 0
            ctime_club[timestamp2str(club.timestamp)] += 1
            node_club.append({"id": club.name, "name": club.name,
                              "category": cate_id, "value": 1+len(club.members.all()),
                              "x": pos_rd(), "y": pos_rd()})
            if node_member.get(club.creator.id) is None:
                node_member[club.creator.id] = {"id": club.creator.id, "name": "user",
                                                "value": [], "x": pos_rd(), "y": pos_rd()}
            node_member[club.creator.id]["value"].append(cate_id)
            links.append({"source": club.name, "target": club.creator.id})
            for member in club.members.all():
                if node_member.get(member.id) is None:
                    node_member[member.id] = {"id": member.id, "name": "user",
                                              "value": [], "x": pos_rd(), "y": pos_rd()}
                node_member[member.id]["value"].append(cate_id)
                links.append({"source":club.name , "target": member.id})

    club_max_val = max([c['value'] for c in node_club])
    mem_max_val = []
    for memid in node_member.keys():
        node_mem = node_member[memid]
        value_count = Counter(node_mem["value"])
        node_mem["category"] = list(value_count.keys())[np.argmax(list(value_count.values()))]
        node_mem["value"] = len(node_mem["value"])
        mem_max_val.append(node_mem["value"])
    mem_max_val = max(mem_max_val)
    csym_size, msym_size = [20, 10], [1,10]
    for c in node_club:
        c["symbolSize"] = c["value"] / club_max_val * csym_size[1] + csym_size[0]
        nodes.append(c)
    for m in node_member.values():
        m["symbolSize"] = m["value"] / mem_max_val * msym_size[1] + msym_size[0]
        nodes.append(m)
    data1 = {'nodes': nodes,
            'links': links,
            'categories': categories}
    data2 = sorted([[i, ctime_club[i]] for i in ctime_club.keys()], key=lambda x:x[0])
    max_data2 = max(ctime_club.values())

    return render_template('admin_templates/data_visualization.html',
                           data1=data1, data2=data2, max_data2=max_data2)
