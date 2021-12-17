from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import main
from .forms import SearchClubForm, Register, Login, SearchBookForm, ChangePasswordForm, EditInfoForm, SearchStudentForm, NewStoreForm, StoreForm, BorrowForm
from .. import db
from ..models import User, Club, Member, Creator, Activity, Admin
import time
import datetime


@main.route('/', methods=['GET', 'POST'])
def home():
    return render_template('main/homepage.html', title='Welcome to Club Master')


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    if request.method == 'GET':
        return render_template('main/register.html', form=form)
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
        return render_template('main/register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(stu_id=form.account.data, password=form.password.data).first()
            if user is None:
                flash('账号或密码错误！')
                return redirect(url_for('.login'))
            else:
                login_user(user)
                session['stu_id'] = user.stu_id
                session['name'] = user.stu_name
                return redirect(url_for('.index'))

    return render_template('main/login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经登出！')
    return redirect(url_for('.login'))


@main.route('/index')
@login_required
def index():
    user = User.query.filter_by(stu_id=session.get('stu_id')).first()
    c = user.as_creator.created_clubs
    m = user.as_member.joined_clubs
    session['cclubs'] = [x.club_name for x in c]
    session['mclubs'] = [x.club_name for x in m]

    return render_template('main/index.html', name=session.get('name'),
                           cclubs=session.get('cclubs'),
                           mclubs=session.get('mclubs'))


@main.route('/echarts')
@login_required
def echarts():
    days = []
    num = []
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    ten_ago = int(today_stamp) - 9 * 86400
    for i in range(0, 10):
        borr = ReadBook.query.filter_by(start_date=str((ten_ago+i*86400)*1000)).count()
        retu = ReadBook.query.filter_by(end_date=str((ten_ago+i*86400)*1000)).count()
        num.append(borr + retu)
        days.append(timeStamp((ten_ago+i*86400)*1000))
    data = []
    for i in range(0, 10):
        item = {'name': days[i], 'num': num[i]}
        data.append(item)
    return jsonify(data)


@main.route('/user/<id>')
@login_required
def user_info(id):
    user = User.query.filter_by(stu_id=id).first()
    return render_template('main/user-info.html', user=user, name=session.get('name'),
                           cclubs=session.get('cclubs'), mclubs=session.get('mclubs'))


@main.route('/change_password', methods=['GET', 'POST'])
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
    return render_template("main/change-password.html", form=form)


@main.route('/change_info', methods=['GET', 'POST'])
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
    return render_template('main/change-info.html', form=form, id=id, name=session['name'],
                           cclubs=session.get('cclubs'), mclubs=session.get('mclubs'))


@main.route('/search_book', methods=['GET', 'POST'])
@login_required
def search_book():  # 这个函数里不再处理提交按钮，使用Ajax局部刷新
    form = SearchBookForm()
    return render_template('main/search-book.html', name=session.get('name'), form=form)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
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
    return render_template('main/new-store.html', name=session.get('name'), form=form,
                           cclubs=session.get('cclubs'), mclubs=session.get('mclubs'))

@main.route('/<name>/join_club')
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
    return redirect(url_for('.borrow'))

@main.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow():
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
        return redirect(url_for('main.borrow'))

    if not session.get('searched', False):
        session['search_res'] = clubs

    return render_template('main/search.html', name=session.get('name'), form=form,
                           cclubs=session.get('cclubs'), mclubs=session.get('mclubs'),
                           search_res=session['search_res'])


@main.route('/find_stu_book', methods=['GET', 'POST'])
def find_stu_book():
    # stu = Club.query.filter_by(card_id=request.form.get('club_name')).first()
    # if stu is None:
    #     return jsonify([{'stu': 0}])  # 没找到
    # clubs = db.session.query(Club).filter(Club.club_name.contains(request.form.get('club_name')),Inventory.status == 1).with_entities(Inventory.barcode,
    #                                                                                            Club.club_type,
    #                                                                                            Club.club_creator,
    #                                                                                            Club.club_desp).all()
    data = []
    # for book in clubs:
    #     item = {'barcode': book.barcode, 'isbn': book.isbn, 'book_name': book.book_name,
    #             'author': book.author, 'press': book.press}
    #     data.append(item)

    return jsonify(data)


@main.route('/out', methods=['GET', 'POST'])
@login_required
def out():
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    barcode = request.args.get('barcode')
    card = request.args.get('card')
    book_name = request.args.get('book_name')
    readbook = ReadBook()
    readbook.barcode = barcode
    readbook.card_id = card
    readbook.start_date = int(today_stamp) * 1000
    readbook.due_date = (int(today_stamp) + 40 * 86400) * 1000
    readbook.borrow_admin = current_user.admin_id
    db.session.add(readbook)
    db.session.commit()
    book = Inventory.query.filter_by(barcode=barcode).first()
    book.status = False
    db.session.add(book)
    db.session.commit()
    bks = db.session.query(Club).join(Inventory).filter(Club.book_name.contains(book_name), Inventory.status == 1). \
        with_entities(Inventory.barcode, Club.isbn, Club.book_name, Club.author, Club.press).all()
    data = []
    for bk in bks:
        item = {'barcode': bk.barcode, 'isbn': bk.isbn, 'book_name': bk.book_name,
                'author': bk.author, 'press': bk.press}
        data.append(item)
    return jsonify(data)
















@main.route('/books', methods=['POST'])
def find_book():

    def find_name():
        return Club.query.filter(Club.club_name.like('%'+request.form.get('content')+'%')).all()

    def find_type():
        return Club.query.filter(Club.club_type.contains(request.form.get('content'))).all()


    methods = {
        'club_name': find_name,
        'club_type': find_type,
    }
    books = methods[request.form.get('method')]()
    data = []
    for book in books:
        count = Inventory.query.filter_by(isbn=book.isbn).count()
        available = Inventory.query.filter_by(isbn=book.isbn, status=True).count()
        item = {'isbn': book.isbn, 'book_name': book.book_name, 'press': book.press, 'author': book.author,
                'class_name': book.class_name, 'count': count, 'available': available}
        data.append(item)
    return jsonify(data)


@main.route('/book', methods=['GET', 'POST'])
def user_book():
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
        return redirect(url_for('main.user_book'))

    if not session.get('searched', False):
        session['search_res'] = clubs

    return render_template('main/user-book.html', name=session.get('name'), form=form,
                           cclubs=session.get('cclubs'), mclubs=session.get('mclubs'),
                           search_res=session['search_res'])



@main.route('/search_student', methods=['GET', 'POST'])
@login_required
def search_student():
    form = SearchStudentForm()
    return render_template('main/search-student.html', name=session.get('name'), form=form)


def timeStamp(timeNum):
    if timeNum is None:
        return timeNum
    else:
        timeStamp = float(float(timeNum)/1000)
        timeArray = time.localtime(timeStamp)
        print(time.strftime("%Y-%m-%d", timeArray))
        return time.strftime("%Y-%m-%d", timeArray)


@main.route('/student', methods=['POST'])
def find_student():
    stu = Student.query.filter_by(card_id=request.form.get('card')).first()
    if stu is None:
        return jsonify([])
    else:
        valid_date = timeStamp(stu.valid_date)
        return jsonify([{'name': stu.student_name, 'gender': stu.sex, 'valid_date': valid_date, 'debt': stu.debt}])


@main.route('/record', methods=['POST'])
def find_record():
    records = db.session.query(ReadBook).join(Inventory).join(Club).filter(ReadBook.card_id == request.form.get('card'))\
        .with_entities(ReadBook.barcode, Inventory.isbn, Club.book_name, Club.author, ReadBook.start_date,
                       ReadBook.end_date, ReadBook.due_date).all()  # with_entities啊啊啊啊卡了好久啊
    data = []
    for record in records:
        start_date = timeStamp(record.start_date)
        due_date = timeStamp(record.due_date)
        end_date = timeStamp(record.end_date)
        if end_date is None:
            end_date = '未归还'
        item = {'barcode': record.barcode, 'book_name': record.book_name, 'author': record.author,
                'start_date': start_date, 'due_date': due_date, 'end_date': end_date}
        data.append(item)
    return jsonify(data)


@main.route('/user/student', methods=['GET', 'POST'])
def user_student():
    form = SearchStudentForm()
    return render_template('main/user-student.html', form=form)


@main.route('/storage', methods=['GET', 'POST'])
@login_required
def storage():
    form = StoreForm()
    if form.validate_on_submit():
        return redirect(url_for('.storage'))
    return render_template('main/storage.html', name=session.get('name'), form=form)


@main.route('/return', methods=['GET', 'POST'])
@login_required
def return_book():
    form = SearchStudentForm()
    return render_template('main/return.html', name=session.get('name'), form=form)


@main.route('/find_not_return_book', methods=['GET', 'POST'])
def find_not_return_book():
    data = []
    return jsonify(data)


@main.route('/in', methods=['GET', 'POST'])
@login_required
def bookin():
    data = []
    return jsonify(data)
