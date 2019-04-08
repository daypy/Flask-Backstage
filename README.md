# Flask-Backstage

### 简介

前端使用layui+layer框架，后端使用flask框架开发的后台。



### 安装后台所需模块

1. 先安装pip(python2.6或python2.7都行)

2. 执行下面命令安装即可(pip慢的话，切国内pip源)

   > #pip install -r requirements/common.txt

3. 安装MySQL-python模块

   > #yum install python-devel mysql-devel zlib-devel openssl-devel
   >
   > #pip install MySQL-python



### 创建数据库

1. 创建flask_admin库

   > create database flask_admin default character set utf8 collate utf8_general_ci;

2. 创建账号并赋权

   > grant all privileges on flask_admin.* to 'opsadmin'@'%' identified by '123456' with grant option;

3. 刷新

   > FLUSH PRIVILEGES;



### Admin后台配置

1. 配置config.py中连接数据库

   > SQLALCHEMY_DATABASE_URI = 'mysql://opsadmin:123456@192.168.9.215:3306/flask_admin'



### 初始化flask_admin所需表和数据

操作命令如下：

> #python manage.py deploy product



### 启动程序

启动

> #gunicorn -b 0.0.0.0:80 manage:app

登陆账号和密码

> 账号：admin@ops.com 密码：admin



### 界面

登陆

![登陆界面](https://github.com/daypy/Flask-Backstage/blob/master/images/login.png)

后台

![后台界面](https://github.com/daypy/Flask-Backstage/blob/master/images/main.png)
