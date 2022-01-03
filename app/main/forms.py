from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, RadioField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length, StopValidation


class Login(FlaskForm):
    account_login = StringField(u'学号', validators=[DataRequired(message=u"学号不能为空！")])
    password_login = PasswordField(u'密码', validators=[DataRequired(message=u"密码不能为空！")])
    submit_login = SubmitField(u'登录')


class Register(FlaskForm):
    account_reg = StringField(label='学号', validators=[DataRequired(message=u"学号不能为空！")])
    stu_name_reg = StringField(label='姓名', validators=[DataRequired(message=u"姓名不能为空！")])
    password_reg = PasswordField(label='密码', validators=[DataRequired(message=u'密码不能为空！')])
    submit_reg = SubmitField(u'注册')


class SearchClubForm(FlaskForm):
    club_name = StringField(label='名称', validators=[])
    club_type = SelectField(choices=('全部', '文学类', '竞赛类', '棋牌类',
                                     '志愿类', '体育类', '音乐类', '游戏类', '语言类', '其他类'))
    submit = SubmitField(u'查找')
    join = SubmitField(u'加入')
