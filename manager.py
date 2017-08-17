#!/usr/bin/env python
#coding:UTF-8
#entrance for server to start
#by qiancheng20170714

import os 
from app import create_app
from app import db
from app.models import User,BSConfig, TRXConfig
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app=create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

if __name__ ==  '__main__':
    manager.run()
