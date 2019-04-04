#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
@Filename: manage.py
@Author: LiJie
@Mail: lijie2402@sina.cn
@Time: 2018/3/27 17:34
"""
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User, Menu, Group, Group_access, Group_auth
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)



def make_shell_context():
	return dict(db=db, User=User, Menu=Menu, Group=Group, Group_access=Group_access, Group_auth=Group_auth)

manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def deploy(deploy_type):
	db.create_all()
	# from flask_migrate import upgrade
	# from app.models import User, Menu
	# upgrade database to the latest version
	# upgrade()

	if deploy_type == 'product':
		# step_2:insert admin account
		User.insert_admin(email='admin@ops.com', username='admin', password='admin')
		# init admin menu
		Menu.init_menu(os.path.join(basedir, 'sql', 'menu'))
		# init admin group
		Group.init_group(os.path.join(basedir, 'sql', 'group'))
		# init admin group_access
		Group_access.init_gaccess(os.path.join(basedir, 'sql', 'group_access'))
		# init admin group_auth
		Group_auth.init_gauth(os.path.join(basedir, 'sql', 'group_auth'))
		print 'db create!'

if __name__ == "__main__":
	manager.run()
	# app.run(host='0.0.0.0', debug=True)
