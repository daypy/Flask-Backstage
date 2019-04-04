#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: views.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/4/2 17:51
"""
import time
import random, hashlib
from flask import render_template, redirect, request, url_for, flash, jsonify, session
from flask_login import login_user, login_required, logout_user
from . import auth
from app.models import User, Group_access
from .forms import LoginForm, ChangePasswordForm, EditUserInfoForm
from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        challenge = request.form['geetest_challenge']
        validate = request.form['geetest_validate']
        m = hashlib.md5()
        if not challenge:
            flash(u'请先通过验证！', 'danger')
        else:
            #md5
            m.update(challenge)
            if m.hexdigest() == validate:
                user = User.query.filter_by(email=form.email.data).first()
                if user is not None and user.verify_password(form.password.data):
                    # 获取用户IP地址
                    user.regIp = request.remote_addr
                    # 生成用户登陆时间
                    user.updateTime = int(time.time())
                    # 更新数据
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    session['username'] = user.username
                    session['gid'] = Group_access.query.filter_by(uid=user.id).first().groupId
                    #flash(u'登陆成功！欢迎回来，%s!' % user.username, 'success')
                    return redirect(request.args.get('next') or url_for('admin.index'))
                else:
                    flash(u'登陆失败！用户名或密码错误，请重新登陆。', 'danger')
            else:
                flash(u'请先通过验证！', 'danger')
    if form.errors:
        flash(u'登陆失败，请尝试重新登陆.', 'danger')

    return render_template('auth/login.html', form=form)

@auth.route('/Verification/gt', methods=['POST','GET'])
def gt():
    gt_captcha_id = '9d80bd1e6eed71d51a760ade1ee54e51'
    m = hashlib.md5()
    m.update(str(random.randint(0,100)))
    rnd1 = m.hexdigest()
    m.update(str(random.randint(0,100)))
    rnd2 = m.hexdigest()
    challenge = rnd1+rnd2[0:2]
    result = {
        'success':0,
        'gt':gt_captcha_id,
        'challenge':challenge,
        'new_captcha':1
    }
    return jsonify(result)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear
    flash(u'您已退出登陆。', 'success')
    return redirect(url_for('auth.login'))