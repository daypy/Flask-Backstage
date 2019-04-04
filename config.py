#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: config.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/3/27 14:36
"""
import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    # DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = 'mysql://opsadmin:123456@192.168.9.215:3306/flask_admin'
    ARTICLES_PER_PAGE = 10
    COMMENTS_PER_PAGE = 6
    SECRET_KEY = 'secret key to protect from csrf'
    WTF_CSRF_SECRET_KEY = 'random key for form' # for csrf protection
    #设置session有效期7天
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    #text
    APP_STATIC_TMP = os.path.join(basedir, 'app\\tmp')
    admin_url = 'http://192.168.5.95:5000'

    @staticmethod
    def init_app(app):
        pass
