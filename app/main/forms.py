from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, RadioField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length, StopValidation


class Register(FlaskForm):
    account = StringField(label='学号', validators=[DataRequired()])
    password = PasswordField(label='密码', validators=[DataRequired(message='密码不能为空.')])
    submit = SubmitField(u'注册')

class SearchClubForm(FlaskForm):
    club_name = StringField(label='名称', validators=[])
    club_type = SelectField(choices=(('全部'), ('志愿类'), ('体育类'), ('音乐类'), ('其他类')))
    submit = SubmitField(u'查找')
    join = SubmitField(u'加入')

class Login(FlaskForm):
    account = StringField(u'学号', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'登录')
