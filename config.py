#coding: UTF-8

import os

class Config:
    SECRET_KEY = os.environ.get('SECRT_KEY')  or 'hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[FLASKY]'
    FLASKY_MAIL_SENDER = 'FLASKY qcc <juggking@163.com>'
    LOCALADDR = ('172.16.56.18',9000) 
    DESADDR = (' 0.0.0.0',9000)
    @staticmethod
    def init_app(app):
        pass
   
class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    SQLALCHEMY_DATABASE_URI = 'mysql://root:007119@localhost:3306/database_demo'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

config={
        'development': DevelopmentConfig,
#        'testing': TestingConfig,
 #       'Production': ProductionConfig,
        'default': Config
#
       }
