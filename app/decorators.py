#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: decorators.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/8/15 18:08
"""
from functools import wraps
from flask import abort, request, session, redirect, url_for
from flask_login import current_user

def admin_required(func):
	@wraps(func)
	def decorated_view(*args, **kwargs):
		if not int(current_user.id) == 1:
			auth_url = session.get('enable_url')
			if not auth_url:
				return redirect(url_for('auth.login'))
			if func.func_doc not in auth_url:
				abort(403)
		return func(*args, **kwargs)
	return decorated_view