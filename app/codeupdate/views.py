#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: views.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/8/21 14:28
"""

from flask import render_template, jsonify, request, session
from flask_login import current_user, login_required
from . import code
from .. import db
from app.decorators import admin_required


@code.route('/list')
def list():
	pass