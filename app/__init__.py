#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: __init__.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/3/14 15:32
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask_moment import Moment
from config import Config

#初始化插件
db = SQLAlchemy()
#bootstrap = Bootstrap()
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_message = u'请先登陆后台!'
login_manager.login_view = 'auth.login'


def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)
	Config.init_app(app)
	CsrfProtect(app)

	db.init_app(app)
	#bootstrap.init_app(app)
	moment.init_app(app)
	login_manager.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from app.auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from .admin import admin as admin_blueprint
	app.register_blueprint(admin_blueprint, url_prefix='/admin')

	from .codeupdate import code as code_blueprint
	app.register_blueprint(code_blueprint, url_prefix='/code')




	return app