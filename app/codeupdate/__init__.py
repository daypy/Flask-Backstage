#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: __init__.py.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/8/21 14:26
"""
from flask import Blueprint

code = Blueprint('code', __name__)

from . import views