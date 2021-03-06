from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, RadioField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length, StopValidation


class Register(FlaskForm):
    account = StringField(label='学号', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[DataRequired(message='密码不能为空.')])
    submit = SubmitField(u'注册')

class SearchClubForm(FlaskForm):
    club_name = StringField(label='名称', validators=[])
    club_type = SelectField(choices=('全部', '文学类', '竞赛类', '棋牌类',
                                     '志愿类', '体育类', '音乐类', '游戏类', '语言类', '其他类'))
    submit = SubmitField(u'查找')
    join = SubmitField(u'加入')

class Login(FlaskForm):
    account = StringField(u'学号', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'登录')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'原密码', validators=[DataRequired()])
    password = PasswordField(u'新密码', validators=[DataRequired(), EqualTo('password2', message=u'两次密码必须一致！')])
    password2 = PasswordField(u'确认新密码', validators=[DataRequired()])
    submit = SubmitField(u'确认修改')


class EditInfoForm(FlaskForm):
    name = StringField(u'用户名', validators=[Length(1, 32)])
    submit = SubmitField(u'提交')


class NewStoreForm(FlaskForm):
    club_name = StringField(validators=[DataRequired(), Length(1, 64)])
    club_type = SelectField(choices=('文学类', '竞赛类', '棋牌类',
                                     '志愿类', '体育类', '音乐类',
                                     '游戏类', '语言类', '其他类'))
    club_desp = StringField(validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField(u'提交')


class NewActivityForm(FlaskForm):
    act_name = StringField(validators=[DataRequired()])
    act_desp = StringField(validators=[DataRequired()])
    act_time = StringField(validators=[DataRequired()])
    limit_num = IntegerField(validators=[])
    submit = SubmitField(u'提交')