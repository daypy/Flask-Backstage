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
#from app.models import Menu
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo



class ChangePasswordForm(FlaskForm):
    password = PasswordField(u'新密码', validators=[
        DataRequired(), EqualTo('password2', message='密码不一致!')], render_kw={"lay-verify":"password"})
    password2 = PasswordField(u'确认新密码', validators=[DataRequired()], render_kw={"lay-verify":"password2"})

class RegUserForm(FlaskForm):
    email = StringField(u'电子邮件', validators=[DataRequired(message=''), Length(1, 64),
                                             Email(message='')], render_kw={"lay-verify":"required"})
    username = StringField(u'昵称', validators=[DataRequired()], render_kw={"lay-verify":"required"})
    gid = SelectField(u'所属组', coerce=int, validators=[DataRequired()])

class SearchUseridForm(FlaskForm):
    stype = SelectField(u'查询类型', coerce=int, validators=[DataRequired()])

class EditUserForm(FlaskForm):
    gid = SelectField(u'所属组', coerce=int, validators=[DataRequired()])

class AddpermissionForm(FlaskForm):
    name = StringField(u'组名称', validators=[DataRequired()], render_kw={"lay-verify": "required"})
    description = TextAreaField(u'描述', validators=[DataRequired()], render_kw={"lay-verify": "required"})

class EditpermissionForm(FlaskForm):
    description = TextAreaField(u'描述', validators=[DataRequired()], render_kw={"lay-verify": "required"})
    status = BooleanField(u'状态', default=True, render_kw={"lay-skin": "switch", "lay-text":"ON|OFF"})

class DeletepermissionForm(FlaskForm):
    gId = StringField(validators=[DataRequired()])

class AddmenuForm(FlaskForm):
    name = StringField(u'菜单名称', validators=[DataRequired()], render_kw={"lay-verify": "name"})
    #fid = SelectField(u'父级菜单', validators=[DataRequired()], render_kw={"lay-verify": ""})
    #fid = SelectField(u'父级菜单', coerce=int, validators=[DataRequired()])
    fid = SelectField(u'父级菜单', coerce=int)
    hide = BooleanField(u'是否隐藏', default=False, render_kw={"lay-skin": "switch", "lay-text":u"隐藏|显示"})
    url = StringField(u'URL')
    sort = IntegerField(u'菜单排序', render_kw={"lay-verify": "sort"})

class DeletemenuForm(FlaskForm):
    menuId = StringField(validators=[DataRequired()])

class RulegroupForm(FlaskForm):
    tree_val = StringField(u'权限列表',render_kw={"type": "hidden", "id": "tree_val"})




