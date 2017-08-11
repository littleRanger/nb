#coding: UTF-8

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  or 'hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25 
    MAIL_USE_TLS = True 
    MAIL_USERNAME='wanghongsimit@163.com'
    MAIL_PASSWORD='python2017'
    NB_MAIL_SUBJECT_PREFIX = '[NB]'
    NB_MAIL_SENDER ='wanghongsimit@163.com'
    
    LOCALADDR = ('127.0.0.1',9000) 
    DESADDR = ('127.0.0.1',9000)
    RECVADDR = ('',9000)
    NB_ADMIN='juggking@163.com'
    @staticmethod
    def init_app(app):
        pass
   
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:007119@localhost:3306/database_demo'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

config={
        'development': DevelopmentConfig,
#        'testing': TestingConfig,
 #       'Production': ProductionConfig,
        'default': Config
#
       }
