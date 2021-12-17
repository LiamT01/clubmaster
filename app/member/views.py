from flask import Flask, render_template, Blueprint, request, g, session, redirect, url_for
from functools import wraps
from flask import render_template, session, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User, Club
from . import member

@member.route('/')
@member.route('/<name>/index')
@login_required
def index(name):
    session['role'] = 'member'
    session['club_name'] = name
    return redirect(url_for('member.personalinfo'))

@member.route('/memberpersonalinfo',methods=['GET','POST'])
@login_required
def personalinfo():
    if request.method =="POST":
        bttn = request.form['bttn']
        print(bttn)
        flash("Personal Info Updated.")
        return redirect(url_for('member.personalinfo'))
    form = Club.query.filter_by(club_name=session['club_name']).first()
    return render_template('member_personalinfo.html',form=form)
    

@member.route('/Complaints')
@login_required
def complaint_history():
    complaint_hist = []
    return render_template('member_complaint.html',complaint_hist=complaint_hist)


@member.route('/addComplaint',methods=["POST"])
@login_required
def addComplaint():
    if request.method=="POST":
        MID,BID = 0, 0
        print(MID)
        return render_template('thankyou_complaint.html')

@member.route('/Feedbacks')
@login_required
def feedback_history():
    feedback_hist = []
    return render_template('member_feedback.html',feedback_hist=feedback_hist)


@member.route('/addFeedback',methods=["POST"])
@login_required
def addFeedback():
    if request.method=="POST":
        MID,BID = 0, 0
        print(MID)
        return render_template('thankyou_feedback.html')
