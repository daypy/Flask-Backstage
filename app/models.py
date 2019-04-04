#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: models.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/3/14 15:28
"""
from flask_login import UserMixin
#import hashlib
import time
import os
import re
import smtplib
#from datetime import datetime
#from flask.ext.login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db,login_manager
from random import Random
from config import Config
from email.header import Header
from email.MIMEText import MIMEText
from email.mime.multipart import MIMEMultipart

class User(UserMixin, db.Model):
	__tablename__ = 'admin_user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	email = db.Column(db.String(64))
	password_hash = db.Column(db.String(128))
	regTime = db.Column(db.Integer)
	regIp = db.Column(db.String(20))
	updateTime = db.Column(db.DateTime)
	status = db.Column(db.SmallInteger)

	@staticmethod
	def insert_admin(email, username, password):
		nowtime = int(time.time())
		user = User(username=username,password=password,email=email,regIp='127.0.0.1',regTime=nowtime,status=1)
		db.session.add(user)
		db.session.commit()

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)


class Menu(db.Model):
	__tablename__ = 'admin_menu'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	fid = db.Column(db.Integer, nullable=False)
	url = db.Column(db.String(50), nullable=False)
	auth = db.Column(db.SmallInteger, nullable=False)
	sort = db.Column(db.Integer, nullable=False)
	hide = db.Column(db.SmallInteger, nullable=False)
	icon = db.Column(db.String(50), nullable=False)
	level = db.Column(db.SmallInteger, nullable=False)

	@staticmethod
	def insert_menu(name, fid, hide, url, sort=0):
		menu = Menu(name=name, fid=fid, url=url, auth=0, sort=sort, hide=hide, icon='', level=0)
		db.session.add(menu)
		db.session.commit()

	@staticmethod
	def init_menu(fname):
		with open(fname, 'r') as fsql:
			sql = fsql.readlines()
			for s in sql:
				s = eval(s.strip('\n'))
				if not s: continue
				menu = Menu(id=int(s['id']), name=s['name'], fid=int(s['fid']), url=s['url'], auth=0,
						sort=int(s['sort']), hide=int(s['hide']), icon='', level=0)
				db.session.add(menu)
			db.session.commit()

	@staticmethod
	def json_menu(gid):
		menu = Menu.query.order_by(Menu.id).all()
		gauth = Group_auth.query.filter_by(gid=gid).all()
		data = []
		if gauth:
			for m in menu:
				action = 0
				for g in gauth:
					if m.id == g.mid:
						action = 1
				if action == 1:
					data.append({"id":m.id, "name":m.name, "pId":m.fid, "url":m.url, "checked": "true"})
				else:
					data.append({"id": m.id, "name": m.name, "pId": m.fid, "url": m.url})
		else:
			for m in menu:
				data.append({"id": m.id, "name": m.name, "pId": m.fid, "url": m.url})

		return data

	@staticmethod
	def glist_to_tree(gid):
		'''
		根据用户组生成菜单列表
		:param gid:
		:return:
		'''
		tree = {}
		tid = 0
		menu =  Menu.query.order_by(Menu.sort).all()
		gauth = Group_auth.query.filter_by(gid=gid).all()
		data = []
		for m in menu:
			for g in gauth:
				if int(m.id) == int(g.mid):
					data.append(m)
				else:
					continue
		if data:
			refer = {}
			for i in data:
				refer[i.id] = {
					"id":'%s' % str(i.id),
					"name":i.name,
					"fid":'%s' % str(i.fid),
					"url":i.url,
					"auth":'%s' % str(i.auth),
					"sort":'%s' % str(i.sort),
					"hide":'%s' % str(i.hide),
					"icon":i.icon,
					"level":'%s' % str(i.level)
				}

			for i in data:
				parentId = i.fid
				if parentId == 0:
					tree[tid] = refer[i.id]
					tid += 1
				else:
					if refer.has_key(parentId):
						if not refer[parentId].has_key('_child'):
							num = 0
							refer[parentId]['_child'] = {}
						else:
							num = len(refer[parentId]['_child'])
						refer[parentId]['_child'][num] = refer[i.id]

		return tree

	@staticmethod
	def mlist_to_tree():
		'''
		生成菜单列表
		:param gid:
		:return:
		'''
		tree = {}
		tid = 0
		data =  Menu.query.order_by(Menu.sort).all()

		if data:
			refer = {}
			for i in data:
				refer[i.id] = {
					"id":'%s' % str(i.id),
					"name":i.name,
					"fid":'%s' % str(i.fid),
					"url":i.url,
					"auth":'%s' % str(i.auth),
					"sort":'%s' % str(i.sort),
					"hide":'%s' % str(i.hide),
					"icon":i.icon,
					"level":'%s' % str(i.level)
				}

			for i in data:
				parentId = i.fid
				if parentId == 0:
					tree[tid] = refer[i.id]
					tid += 1
				else:
					if refer.has_key(parentId):
						if not refer[parentId].has_key('_child'):
							num = 0
							refer[parentId]['_child'] = {}
						else:
							num = len(refer[parentId]['_child'])
						refer[parentId]['_child'][num] = refer[i.id]

		return tree

	@staticmethod
	def menu_to_list():
		mlist = []
		data = Menu.query.order_by(Menu.sort).all()

	@staticmethod
	def list_to_menu(data):
		mlist = []
		for i in data:
			if not data[i].has_key('_child'):
				mlist.append(data[i])
			else:
				child = data[i]['_child']
				data[i].pop('_child')
				data[i]['children'] = Menu.list_to_menu(child)
				mlist.append(data[i])

		return mlist

	@staticmethod
	def form_at_tree(data,lv=0):
		formattree = []
		for i in data:
			title_prefix = ''
			for n in range(0,lv):
				title_prefix += "|---"

			data[i]['lv'] = lv
			if lv == 0:
				data[i]['namePrefix'] = ''
				data[i]['showName'] = data[i]['name']
			else:
				data[i]['namePrefix'] = title_prefix
				data[i]['showName'] = title_prefix+data[i]['name']
			if not data[i].has_key('_child'):
				formattree.append(data[i])
			else:
				child = data[i]['_child']
				del data[i]['_child']
				formattree.append(data[i])
				middle = Menu.form_at_tree(child,lv+1)
				formattree = formattree + middle

		return formattree

	def __repr__(self):
		return '<Menu %r>' % self.name

class Group(db.Model):
	__tablename__ = 'admin_group'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	description = db.Column(db.String(50), nullable=False)
	status = db.Column(db.SmallInteger, nullable=False)

	@staticmethod
	def insert_group(name,description):
		group = Group(name=name, description=description, status=1)
		db.session.add(group)
		db.session.commit()

	@staticmethod
	def init_group(fname):
		with open(fname, 'r') as fsql:
			sql = fsql.readlines()
			for s in sql:
				s = eval(s.strip('\n'))
				if not s: continue
				group = Group(id=int(s['id']), name=s['name'], description=s['description'], status=int(s['status']))
				db.session.add(group)
			db.session.commit()

	def __repr__(self):
		return '<Group %r>' % self.name

class Group_access(db.Model):
	__tablename__ = 'admin_group_access'
	id = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer, unique=True, index=True, nullable=False)
	groupId = db.Column(db.Integer, nullable=False)

	@staticmethod
	def insert_gaccess(uid, gid):
		gaccess = Group_access(uid=uid, groupId=gid)
		db.session.add(gaccess)
		db.session.commit()

	@staticmethod
	def init_gaccess(fname):
		with open(fname, 'r') as fsql:
			sql = fsql.readlines()
			for s in sql:
				s = eval(s.strip('\n'))
				if not s: continue
				gaccess = Group_access(id=int(s['id']), uid=int(s['uid']), groupId=int(s['groupId']))
				db.session.add(gaccess)
			db.session.commit()

class Group_auth(db.Model):
	__tablename__ = 'admin_group_auth'
	id = db.Column(db.Integer, primary_key=True)
	mid = db.Column(db.Integer, nullable=False)
	gid = db.Column(db.Integer, nullable=False)

	@staticmethod
	def insert_gauth(mlist,gid):
		for m in mlist:
			db.session.add(Group_auth(mid=int(m), gid=gid))
		db.session.commit()

	@staticmethod
	def delete_gauth(gid):
		Group_auth.query.filter_by(gid=gid).delete()
		db.session.commit()

	@staticmethod
	def init_gauth(fname):
		with open(fname, 'r') as fsql:
			sql = fsql.readlines()
			for s in sql:
				s = eval(s.strip('\n'))
				if not s: continue
				gauth = Group_auth(id=int(s['id']), mid=int(s['mid']), gid=int(s['gid']))
				db.session.add(gauth)
			db.session.commit()

class Sendmail:
	def __init__(self):
		self.MailHost = "mail.sinashow.com"
		self.MailUser = "monitor@sinashow.com"
		self.MailPswd = "monitor"
		self.MailPostfix = "sinashow.com"

	def pass_random(self,randomlength=8):
		passwd = ''
		chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
		length = len(chars) - 1
		random = Random()
		for i in range(randomlength):
			passwd += chars[random.randint(0, length)]

		return passwd

	def mail_template(self,uemail,passwd):
		with open(os.path.join(Config.APP_STATIC_TMP, 'usermail.html')) as oldf:
			oldf = oldf.readlines()
			with open(os.path.join(Config.APP_STATIC_TMP, 'news.html'),'w+') as newsf:
				for f in oldf:
					news = f.strip('\n')
					ere = re.findall(r'u-email',news)
					if ere:
						news = re.sub(r'u-email', uemail, news)
					pre = re.findall(r'password',news)
					if pre:
						news = re.sub(r'password', passwd, news)
					ure = re.findall(r'Backstageurl',news)
					if ure:
						news = re.sub(r'Backstageurl', Config.admin_url, news)
					newsf.write(news+'\n')

	def send_mail(self, sendmail):
		sub = '运维后台账号'
		Me = self.MailUser
		msg = MIMEMultipart()
		msg['Subject'] = Header(sub, 'utf-8')
		msg['From'] = r"%s <%s>" % (Header("邮件小U", "utf-8"), Me)
		sendmaillist = sendmail.split(",")
		msg['To'] = ";".join(sendmaillist)

		# html
		html = open(os.path.join(Config.APP_STATIC_TMP, 'news.html')).read()
		html_part = MIMEText(html, 'html', 'utf-8')
		msg.attach(html_part)

		# send mail
		try:
			s = smtplib.SMTP()
			s.connect(self.MailHost)
			s.login(self.MailUser, self.MailPswd)
			s.sendmail(Me, sendmaillist, msg.as_string())
			s.close()
			return True
		except Exception, e:
			print str(e)
			return False

	def ssmain(self, email):
		passwd = self.pass_random()
		self.mail_template(email, passwd)
		sub = '运维后台账号'
		self.send_mail(email)

# callback function for flask-login extentsion
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

#premission
class Premission:
	ADMINISTRATOR =0x80


