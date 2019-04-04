#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: errors.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/4/2 16:11
"""
from flask import render_template, request, jsonify
from . import main


@main.app_errorhandler(403)
def forbidden(e):

    return render_template('manin/403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):

    return render_template('main/404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):

    return render_template('main/500.html'), 500
