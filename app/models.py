#coding:UTF-8
from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager

class User(UserMixin,db.Model):
#class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64),unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64),unique=True)
    @property
    def password(self):
        raise AttributeError('password is not a readable')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    def __repr__(self):
        return 'Users %s'%self.name




class BSConfig(db.Model):
    __tablename__="BSConfig"
    bsid = db.Column(db.Integer,primary_key=True)
    bsip1 = db.Column(db.String(64),unique=True)
    bsip2 = db.Column(db.String(64),unique=True)
    
    ulPacketTime = db.Column(db.Integer,default=400)
    ulPacketNum = db.Column(db.Integer)
    dlLogicSubFrameNum = db.Column(db.Integer, default=1)
    dlPacketTime = db.Column(db.Integer, default=300)
    
    trxNum = db.Column(db.Integer)
    bsPort1 = db.Column(db.Integer,default=8080)
    bsPort2 = db.Column(db.Integer,default=8888)
    ulCompetitionSectionTime = db.Column(db.Integer,default=100)
    sin_family = db.Column(db.Integer)
    dlLogicSubFrameIdx = db.Column(db.Integer,default=1)
    Trxs = db.relationship('TrxConfig',backref='bs')
    
    def __repr__(self):
        return '<BS %s>'%self.name
    
class TrxConfig(db.Model):
    __tablename__="TrxConfig" 
    trxId = db.Column(db.Integer, primary_key=True)
    trxIp = db.Column(db.String(64))
    ssNum = db.Column(db.Integer)
    trxPort = db.Column(db.Integer,default=8000)
    trxTxPower = db.Column(db.Integer,default=33)
    trxDataRate = db.Column(db.Integer,default=5)
    trxFreq = db.Column(db.Integer , default=434)
    bs_id = db.Column(db.Integer,db.ForeignKey(BSConfig.bsid))
    
    def __repr__(self):
        return '<Trx %s>'%self.name

#class 
