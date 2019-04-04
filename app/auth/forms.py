#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: forms.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/4/2 17:52
"""
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField(u'电子邮件', validators=[DataRequired(message=u'邮箱地址不能为空'), Length(1, 64),
                                             Email(message=u'邮箱格式不正确')])
    password = PasswordField(u'密码', validators=[DataRequired(message=u'密码不能为空')])

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'原来密码', validators=[DataRequired()])
    password = PasswordField(u'新密码', validators=[
        DataRequired(), EqualTo('password2', message=u'两次输入密码不一致！')])
    password2 = PasswordField(u'确认新密码', validators=[DataRequired()])


class EditUserInfoForm(FlaskForm):
    username = StringField(u'昵称', validators=[DataRequired()])
    #email = StringField(u'电子邮件', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(u'密码确认', validators=[DataRequired()])
