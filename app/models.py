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
        if self.email==current_app.config["NB_ADMIN"]:
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
    active = db.Column(db.Boolean, default=True)
    BSID = db.Column(db.Integer,primary_key=True)
    BSIP1 = db.Column(db.String(64),unique=True)
    BSIP2 = db.Column(db.String(64),unique=True)
    
    ulPacketTime = db.Column(db.Integer,default=400)
    ulPacketNum = db.Column(db.Integer)
    dlLogicSubFrameNum = db.Column(db.Integer, default=1)
    dlPacketTime = db.Column(db.Integer, default=300)
    
    TRXNum = db.Column(db.Integer,default=8)
    BSPort1 = db.Column(db.Integer,default=8080)
    BSPort2 = db.Column(db.Integer,default=8888)
    ulCompetitionSectionTime = db.Column(db.Integer,default=100)
    sin_family = db.Column(db.Integer)
    dlLogicSubFrameIdx = db.Column(db.Integer,default=1)
    TRXs = db.relationship('TRXConfig',backref='bs')
   
    Throughout = db.Column(db.Integer,default=800)
    ulThroughout = db.Column(db.Integer,default=400)
    dlThroughout = db.Column(db.Integer,default=400)
    PacketMiss = db.Column(db.Float, default=0.1)
    def as_dict(self):
        dict= {c.name:getattr(self,c.name) for c in self.__table__.columns if c.name=="Throughout" or c.name=="dlThroughout" or c.name=="ulThroughout" or c.name=="PacketMiss"}
        return dict
    def __repr__(self):
        return '<BS %s>'%self.BSID
    
class TRXConfig(db.Model):
    __tablename__="TrxConfig" 
    TRXID = db.Column(db.Integer, primary_key=True)
    TRXIP = db.Column(db.String(64))
    SSNum = db.Column(db.Integer)
    TRXPort = db.Column(db.Integer,default=8000)
    TRXTxPower = db.Column(db.Integer,default=33)
    TRXDataRate = db.Column(db.Integer,default=5)
    TRXFreq = db.Column(db.Integer , default=434)
    BS_ID = db.Column(db.Integer,db.ForeignKey(BSConfig.BSID))
    SSs = db.relationship('SSConfig',backref='trx')
    
    BaudRate = db.Column(db.Integer , default=115200)
    ModeAddr = db.Column(db.Integer , default=4661)
    CheckSum = db.Column(db.String(64) , default="8N1")
    Channel  = db.Column(db.Integer , default=434)
    AirRate  = db.Column(db.Integer , default=19200)
    TxPower  = db.Column(db.Integer , default=30) 
    SleepTime= db.Column(db.Integer , default=250)
    def as_dict(self):
        d= {c.name:getattr(self,c.name) for c in self.__table__.columns
                if c.name=="BaudRate" or
                   c.name=="ModeAddr" or
                   c.name=="CheckSum" or
                   c.name=="Channel" or
                   c.name=="AirRate" or
                   c.name=="TxPower" or
                   c.name=="TRXId" or
                   c.name=="SSNum" or
                   c.name=="TRXPort" or
                   c.name=="SleepTime" }
        return d
    def __repr__(self):
        return '<Trx %s>'%self.TRXID

class SSConfig(db.Model):
    __tablename__="SSConfig" 
    ssID   = db.Column(db.Integer, primary_key=True)
    ssIP   = db.Column(db.String(64))
    ssTxPower = db.Column(db.Integer,default=33)
    ssDataRate = db.Column(db.Integer,default=33)
    ssFreq = db.Column(db.Float,default=33)
    TRX_ID = db.Column(db.Integer,db.ForeignKey(TRXConfig.TRXID))
    def __repr__(self):
        return '<SS %s>'%self.SSID
