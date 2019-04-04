#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: __init__.py.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/4/2 18:46
"""
from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views