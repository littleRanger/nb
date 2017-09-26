#coding:UTF-8
from flask import current_app
from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(UserMixin,db.Model):
#class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64),unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64),unique=True)
    confirmed = db.Column(db.Boolean,default=False)
     
    def is_admin(self):
        if self.email == current_app.config["NB_ADMIN"]:
            return True
        else:
            return False 
    
    def generate_confirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        print self.confirmed
        db.session.add(self)
        return True

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
        return 'Users %s'%self.username




class BSConfig(db.Model):
    __tablename__="BSConfig"
    BSID = db.Column(db.Integer,primary_key=True)
    
    bs_name = db.Column(db.String(64), unique=True) 
    active = db.Column(db.Boolean, default=True)
    BSIP1 = db.Column(db.String(64))
    BSIP2 = db.Column(db.String(64))
    BSPort1 = db.Column(db.Integer,default=8080)
    BSPort2 = db.Column(db.Integer,default=8888)
    BSGPS = db.Column(db.String(64)) 
    ulPacketTime = db.Column(db.Integer,default=400)
    ulPacketNum = db.Column(db.Integer)
    dlLogicSubFrameNum = db.Column(db.Integer, default=1)
    dlPacketTime = db.Column(db.Integer, default=300)
    
    ulCompetitionSectionTime = db.Column(db.Integer,default=100)
    sin_family = db.Column(db.Integer)
    dlLogicSubFrameIdx = db.Column(db.Integer,default=1)
    
    TRXs = db.relationship('TRXConfig',backref='bs')
   
    Throughout = db.Column(db.Integer,default=800)
    ulThroughout = db.Column(db.Integer,default=400)
    dlThroughout = db.Column(db.Integer,default=400)
    PacketMiss = db.Column(db.Float, default=0.1)
    def as_dict(self):
        d= {c.name:getattr(self,c.name) for c in self.__table__.columns 
                if c.name=="BSID" or 
                   c.name=="bs_name" or 
                   c.name=="BSPort1" or 
                   c.name=="BSIP1" or c.name=="Throughout" or c.name=="dlThroughout" or c.name=="ulThroughout" or c.name=="PacketMiss"}
        return d
    def config_as_dict(self):
        d = {c.name:getattr(self,c.name) for c in self.__table__.columns
                if c.name=="bs_name"  or 
                   c.name=="BSIP1"   or 
                   c.name=="BSPort1" or 
                   c.name=="BSIP2"   or 
                   c.name=="BSPort2" or 
                   c.name=="ulPacketTime" or 
                   c.name=="ulPacketNum"  or 
                   c.name=="dlLogicSubFrameNum"   or 
                   c.name=="dlPacketTime"         or
                   c.name=="ulCompetitionSectionTime" or
                   c.name=="sin_family"           or
                   c.name=="dlLogicSubFrameIdx"}
        return d
    def __repr__(self):
        return '<BS %s>'%self.BSID
    
class TRXConfig(db.Model):
    __tablename__="TrxConfig"
    trx_name = db.Column(db.String(64))
    TRXID = db.Column(db.Integer, primary_key=True)
    TRXIP = db.Column(db.String(64))
    TRXPort = db.Column(db.Integer,default=8000)
    TRXTxPower = db.Column(db.Integer,default=33)
    TRXDataRate = db.Column(db.Integer,default=5)
    TRXFreq = db.Column(db.Integer , default=434)
    
    BS_ID = db.Column(db.Integer,db.ForeignKey(BSConfig.BSID))
    SSs = db.relationship('SSConfig',backref='trx')
    
    def as_dict(self):
        d= {c.name:getattr(self,c.name) for c in self.__table__.columns
                if c.name=="trx_name" or
                   c.name=="TRXID" or
                   c.name=="TRXIP" or
                   c.name=="TRXPort" or
                   c.name=="TRXTxPower" or
                   c.name=="TRXDataRate" or
                   c.name=="TRXFreq" }
        return d
    def __repr__(self):
        return '<Trx %s>'%self.TRXID

class SSConfig(db.Model):
    __tablename__="SSConfig" 
    ss_name = db.Column(db.String(64))
    SSID   = db.Column(db.Integer, primary_key=True)
    SSIP   = db.Column(db.String(64))
    SSGPS = db.Column(db.String(64))
    TRX_ID = db.Column(db.Integer,db.ForeignKey(TRXConfig.TRXID))
    def __repr__(self):
        return '<SS %s>'%self.SSID
