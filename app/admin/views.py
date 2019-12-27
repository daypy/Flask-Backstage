#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: views.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/4/2 18:46
"""
import time
import os
import re
import random, hashlib
import json
from flask import render_template, redirect, request, url_for, flash, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from . import admin
from app.models import User, Menu, Group, Group_access, Group_auth, Sendmail
from .forms import ChangePasswordForm, RegUserForm, SearchUseridForm, AddpermissionForm, EditpermissionForm, \
	DeletepermissionForm, AddmenuForm, DeletemenuForm, EditUserForm, RulegroupForm
from .. import db
from config import Config
from app.decorators import admin_required

@admin.route('/index')
@login_required
def index():
	'''/admin/index'''
	if not int(current_user.id) == 1:
		menu = Menu.glist_to_tree(session.get('gid'))
	else:
		menu = 	Menu.mlist_to_tree()
	mlist = Menu.form_at_tree(menu)
	session['enable_url'] = filter(None, list(set(auth['url'] for auth in mlist)))
	#处理隐藏菜单
	data = [m for m in mlist if int(m['hide']) == 0]

	return render_template('admin/index.html', list=data, username=session.get('username'))

@admin.route('/welcome')
@login_required
@admin_required
def welcome():
	'''/admin/welcome'''
	# current_user.updateTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(current_user.updateTime))

	return  render_template('admin/welcome.html')

@admin.route('/changeuser', methods=['GET', 'POST'])
@login_required
def changeuser():
	'''/admin/changeuser'''
	form = ChangePasswordForm()
	if form.validate_on_submit():
		current_user.password = form.password.data
		db.session.add(current_user)
		db.session.commit()
		return jsonify({'code':1,'msg':'修改密码成功!'})

	return render_template('auth/changeuser.html', form=form)


@admin.route('/User')
@login_required
@admin_required
def user():
	'''/admin/User'''
	form = SearchUseridForm()

	return render_template('admin/user/index.html', form=form)

@admin.route('/userpage', methods=['GET','POST'])
@login_required
@admin_required
def userpage():
	'''/admin/userpage'''
	#读取分页
	if request.method == 'POST':
		start = int(request.form.to_dict().get('start'))
		per_page = int(request.form.to_dict().get('length'))
		draw = request.args.get('draw', 1, type=int)
		if start == 0:
			page = 1
		else:
			page = int(start/per_page)
	where = ''
	if request.args.get('type') and request.args.get('keyword'):
		if int(request.args.get('type')) == 1:
			pagination = User.query.filter(User.email.like("%"+request.args.get('keyword')+"%")).order_by( \
				User.id).paginate(page=page, per_page=per_page, error_out=False)
			where =  '''User.email.like("\%{}\%")'''.format(request.args.get('keyword'))
		elif int(request.args.get('type')) == 2:
			pagination = User.query.filter(User.username.like("%" + request.args.get('keyword') + "%")).order_by( \
				User.id).paginate(page=page, per_page=per_page, error_out=False)
	if not where:
		pagination = User.query.order_by(User.id).paginate(page=page, per_page=per_page, error_out=False)

	# page = request.args.get('start', 1, type=int)
	# per_page = request.args.get('length', 10, type=int)

	#group
	ugdata = Group_access.query.all()
	gdata = Group.query.all()
	gid = {n.uid: n.groupId for n in ugdata}
	ginfo = {m.id: m.name for m in gdata}
	info = [{'id':n.id,'username':n.username,'email':n.email, 'gname':ginfo[gid[n.id]], \
			 'regTime':time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(n.regTime)), 'regIp':n.regIp, \
			 'updateTime':n.updateTime} for n in pagination.items]
	data = {
		'draw':draw,
		'recordsTotal': pagination.total,
		'recordsFiltered': pagination.total,
		'data': info
	}

	return jsonify(data)


@admin.route('/User/add', methods=['GET', 'POST'])
@login_required
@admin_required
def useradd():
	'''/admin/User/add'''
	form = RegUserForm()
	group = Group.query.order_by(Group.id).all()
	form.gid.choices = [(int(n.id), n.name) for n in group if n.status == 1]
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if not user:
			sendmail = Sendmail()
			passwd = sendmail.pass_random()
			User.insert_admin(form.email.data, form.username.data, passwd)
			uid = User.query.filter_by(email=form.email.data).first()
			Group_access.insert_gaccess(uid.id,form.gid.data)
			sendmail.mail_template(form.email.data, passwd)
			sendmail.send_mail(form.email.data)
			return jsonify({'code':1,'msg':'用户增加成功!'})
		else:
			return jsonify({'code':0,'msg':'用户已经存在!'})

	return render_template('admin/user/add.html', form=form)

@admin.route('/User/edit/<id>', methods=['GET','POST'])
@login_required
@admin_required
def useredit(id):
	'''/admin/User/edit'''
	form = EditUserForm()
	user = User.query.get_or_404(int(id))
	group = Group.query.order_by(Group.id).all()
	g_id = Group_access.query.filter_by(uid=int(id)).first()
	form.gid.choices = [(int(n.id), n.name) for n in group if n.status == 1]
	if form.validate_on_submit():
		g_id.groupId = form.gid.data
		db.session.add(g_id)
		db.session.commit()
		return jsonify({'code': 1, 'msg': '修改成功!'})

	#uinfo
	uinfo = {}
	uinfo['id'] = user.id
	uinfo['email'] = user.email
	uinfo['username'] = user.username
	form.gid.data = g_id.groupId

	return render_template('admin/user/edit.html', form=form, uinfo=uinfo)



@admin.route('/User/del', methods=['POST'])
@login_required
@admin_required
def userdel():
	'''/admin/User/del'''
	uid = request.form.get('uid')
	if int(uid) == 1:
		return jsonify({'code': 0, 'msg': '该用户不允许删除!'})
	user =  User.query.filter_by(id=uid).first()
	group = Group_access.query.filter_by(uid=uid).first()
	if user:
		db.session.delete(user)
		db.session.delete(group)
		db.session.commit()
		return jsonify({'code':1,'msg':'用户删除成功!'})
	else:
		return jsonify({'code':0,'msg':'用户不存在!'})

@admin.route('/User/reset', methods=['POST'])
@login_required
@admin_required
def userreset():
	'''/admin/User/reset'''
	uid = request.form.get('uid')
	user = User.query.filter_by(id=uid).first()
	if user:
		sendmail = Sendmail()
		passwd = sendmail.pass_random()
		user.password = passwd
		db.session.add(user)
		db.session.commit()
		sendmail.mail_template(user.email, passwd)
		sendmail.send_mail(user.email)
		return jsonify({'code': 1, 'msg': '密码已经重置!'})
	else:
		return jsonify({'code': 0, 'msg': '用户不存在!'})

@admin.route('/Permission', methods=['GET','POST'])
@login_required
@admin_required
def permission():
	'''/admin/Permission'''
	form = DeletepermissionForm()

	return render_template('admin/permission/index.html', form=form)

@admin.route('/Permission/page', methods=['GET','POST'])
def permission_page():
	if request.method == 'POST':
		start = int(request.form.to_dict().get('start'))
		per_page = int(request.form.to_dict().get('length'))
		draw = request.args.get('draw', 1, type=int)
		if start == 0:
			page = 1
		else:
			page = int(start / per_page)

	pagination = Group.query.order_by(Group.id).paginate(page=page, per_page=per_page, error_out=False)

	info = [{'id': n.id, 'name': n.name, 'description': n.description, \
			 'status': n.status} for n in pagination.items]
	data = {
		'draw': draw,
		'recordsTotal': pagination.total,
		'recordsFiltered': pagination.total,
		'data': info
	}

	return jsonify(data)

@admin.route('/Permission/add', methods=['GET','POST'])
@login_required
@admin_required
def permission_add():
	'''/admin/Permission/add'''
	form = AddpermissionForm()
	if form.validate_on_submit():
		group = Group.query.filter_by(name=form.name.data).first()
		if not group:
			Group.insert_group(form.name.data,form.description.data)
			return jsonify({'code': 1, 'msg': '添加成功!'})
		else:
			return jsonify({'code': 0, 'msg': '组名已存在!'})

	return render_template('admin/permission/add.html', form=form)

@admin.route('/Permission/edit/<id>', methods=['GET','POST'])
@login_required
@admin_required
def permission_edit(id):
	'''/admin/Permission/edit'''
	group = Group.query.get_or_404(int(id))
	form = EditpermissionForm()
	if form.validate_on_submit():
		group.description = form.description.data
		group.status = form.status.data
		db.session.add(group)
		db.session.commit()
		return jsonify({'code': 1, 'msg': '修改成功!'})

	form.description.data = group.description
	form.status.data = group.status

	return render_template('admin/permission/edit.html', form=form, group=group)


@admin.route('/Permission/del', methods=['POST'])
def permission_del():
	'''/admin/Permission/del'''
	gid = request.form.get('gid')
	if int(gid) == 1:
		return jsonify({'code': 0, 'msg': '该组不允许删除!'})
	group = Group.query.filter_by(id=gid).first()
	if group:
		db.session.delete(group)
		db.session.commit()
		return jsonify({'code': 1, 'msg': '组删除成功!'})
	else:
		return jsonify({'code': 0, 'msg': '组不存在!'})

@admin.route('/rule/<id>', methods=['GET','POST'])
@login_required
@admin_required
def rule(id):
	'''/admin/rule'''
	form = RulegroupForm()
	if form.validate_on_submit():
		mlist = filter(None, form.tree_val.data.split('|'))
		gauth = Group_auth.query.filter_by(gid=int(id)).first()
		#删除权限列表数据
		if gauth:
			Group_auth.delete_gauth(int(id))
		#插入数据
		if mlist:
			Group_auth.insert_gauth(mlist,int(id))

		return jsonify({'code': 1, 'msg': '修改成功!'})

	return render_template('admin/permission/group_auth.html', form=form, gid=id)
	#return '<span class="layui-btn">成员授权</span>'

@admin.route('/rule/json/<id>', methods=['GET','POST'])
@login_required
@admin_required
def rule_json(id):
	'''/admin/rule/json'''
	data = Menu.json_menu(id)

	return jsonify(data)

@admin.route('/Member/<id>', methods=['GET','POST'])
@login_required
@admin_required
def member(id):
	'''/admin/Member'''
	form = SearchUseridForm()
	member = Group_access.query.filter_by(groupId=id).all()
	user = [{'id':u.id,'email':u.email,'username':u.username} for u in User.query.all()]
	data = []
	if member:
		for u in user:
			for i in member:
				if int(i.uid) == int(u['id']):
					data.append(u)

	return render_template('admin/member.html', form=form, data=data)

@admin.route('/Menu')
@login_required
@admin_required
def menu():
	'''/admin/Menu'''
	data = Menu.mlist_to_tree()
	mlist = Menu.list_to_menu(data)
	form2 = DeletemenuForm()
	return render_template('admin/menu/menu.html', form2=form2, list=mlist)

@admin.route('/Menu/add', methods=['GET','POST'])
@login_required
@admin_required
def menu_add():
	'''/admin/Menu/add'''
	#生成菜单数据
	data = Menu.mlist_to_tree()
	list = Menu.form_at_tree(data)
	list.insert(0, {"id": "0", "showName": u"顶级菜单"})

	#form
	form = AddmenuForm()
	form.fid.choices = [(int(n['id']), n['showName']) for n in list]
	if form.validate_on_submit():
		Menu.insert_menu(form.name.data, form.fid.data, form.hide.data, form.url.data, form.sort.data)
		return jsonify({'code': 1, 'msg': '菜单添加成功!'})
	if form.errors:
		return jsonify({'code': 0, 'msg': '菜单添加失败!'})



	return render_template('admin/menu/add.html', form=form)

@admin.route('/Menu/edit/<id>', methods=['GET','POST'])
@login_required
@admin_required
def menu_edit(id):
	'''/admin/Menu/edit'''
	# 生成菜单数据
	data = Menu.mlist_to_tree()
	list = Menu.form_at_tree(data)
	list.insert(0, {"id": "0", "showName": u"顶级菜单"})
	menu = Menu.query.get_or_404(int(id))
	#form
	form = AddmenuForm()
	menus = [(int(n['id']), n['showName']) for n in list]
	form.fid.choices = menus

	if form.validate_on_submit():
		menu.name = form.name.data
		menu.fid = form.fid.data
		menu.hide = form.hide.data
		menu.url = form.url.data
		menu.sort = form.sort.data
		db.session.add(menu)
		db.session.commit()
		return jsonify({'code': 1, 'msg': '菜单修改成功!'})

	if form.errors:
		return jsonify({'code': 0, 'msg': '菜单修改失败!'})

	form.name.data = menu.name
	form.fid.data = menu.fid
	form.hide.data = menu.hide
	form.url.data = menu.url
	form.sort.data = menu.sort

	return render_template('admin/menu/edit.html', form=form, menu=menu)

@admin.route('/Menu/del', methods=['POST'])
@login_required
@admin_required
def menu_del():
	'''/admin/Menu/del'''
	id = request.form.get('id')
	menus = Menu.query.filter_by(fid=id).first()
	if menus:
		return jsonify({'code':0, 'msg': '请先删除子菜单!'})
	else:
		menu = Menu.query.filter_by(id=id).first()
		if menu:
			db.session.delete(menu)
			db.session.commit()
			return jsonify({'code': 1, 'msg': '菜单删除成功!'})
		else:
			return jsonify({'code': 0, 'msg': '菜单删除失败!'})
