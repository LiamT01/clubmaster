from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for
from functools import wraps
import random,math,datetime
from flask import render_template, session, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..manager.forms import NewStoreForm
from ..models import User, Club, Activity
from . import manager


@manager.route('/')
@manager.route('/<name>/index')
@login_required
def index(name):
    session['role'] = 'manager'
    session['club_name'] = name
    return redirect(url_for('manager.personalinfo'))



@manager.route('/personalinfo')
@login_required
def personalinfo():
    club = Club.query.filter_by(club_name=session['club_name']).first()
    return render_template('manager_personalinfo.html', club=club, name=session.get('name'),
                           cclubs=session.get('cclubs'), mclubs=session.get('mclubs'))


@manager.route('/personalinfoscr',methods=['POST'])
@login_required
def personalinfoscr():
    return redirect(url_for('manager.personalinfo'))



@manager.route('/amenities',methods=['GET','POST'])
@login_required
def amenities():
    club = Club.query.filter_by(club_name=session['club_name']).first()
    if request.method == "POST":
        if 'insert' in request.form:
            act = Activity()
            act.club_name = session['club_name']
            act.act_name = request.form.get('name')
            act.act_desp = request.form.get('description')
            db.session.add(act)
            db.session.commit()
            return redirect(url_for('manager.amenities'))
        if 'update' in request.form:
            return redirect(url_for('manager.amenities'))
        if 'delete' in request.form:
            return redirect(url_for('manager.amenities'))
    data = Activity.query.filter_by(club_name=session['club_name']).all()

    return render_template('manager_amenities.html', data=data, club=club)


############################################################## ADD & VIEW MEMBERS
@manager.route('/addmembers',methods=['GET','POST'])
@login_required
def add_members():
    club = Club.query.filter_by(club_name=session['club_name']).first()
    if request.method =="POST":
        flash("Employee Added")
        return "POST"
    membershipdata = []
    return render_template("manager_addmembers.html", membershipdata=membershipdata, club=club)


@manager.route('/memberdetails')
@login_required
def memberdetails():
    club = Club.query.filter_by(club_name=session['club_name']).first()
    MemDetail = []
    return render_template('m_member_details.html', MemDetail=MemDetail, club=club)


@manager.route('/MemComplaints')
@login_required
def mem_complaint_history():
    club = Club.query.filter_by(club_name=session['club_name']).first()
    complaint_history = []
    return render_template('member_complaints.html',complaint_history=complaint_history, club=club)

@manager.route('/ViewFeedbacks')
@login_required
def mem_feedbacks():
    club = Club.query.filter_by(club_name=session['club_name']).first()
    feedbacks = []
    return render_template('manager_feedbacks.html',feedbacks=feedbacks, club=club)



