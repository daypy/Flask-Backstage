#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: views.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/4/2 16:12
"""
from flask import render_template, request, current_app, redirect,\
    url_for, flash, session
from . import main
from .. import db

@main.route('/')
def index():
    if session.get('username'):
        return redirect(url_for('admin.index'))
    else:
        return redirect(url_for('auth.login'))