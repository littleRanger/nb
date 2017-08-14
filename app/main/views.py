#coding:UTF-8

from flask import render_template, redirect, url_for,current_app,request
from flask_login import login_required,current_user
from . import main
from ..models import BSConfig,TrxConfig,SSConfig
import json
from UDPSendRecv import *

@main.route('/', methods=['GET','POST'])
@login_required
def index():
    return render_template('index.html')
# bsdata table
@main.route('/basedata',methods=['GET', 'POST'])
@login_required
def basedata2index():
    #get basenum&its config info
    BSNUM=BSConfig.query.filter_by(active=True).count()
    u=BSConfig.query.filter_by(active=True).all()
    key = ('id','num')
    t = ((u[i].bsid,u[i].trxNum) for i in range(BSNUM))
    d = [dict(zip(key,value)) for value in t]
    print d
            
    #d= [{'num':'30','id':2},{'num':40,'id':3}]
    print d
    return json.dumps(d)

'''@main.route()'''
#base id & its data
@main.route('/home/<bsid>', methods=['GET','POST'])
@login_required
def home(bsid):
    id = int(bsid)
    '''bs = BSConfig.query.filter_by(bsid=id).first()
    if bs != None:
        d=bs.as_dict()'''
    return render_template('bs.html',bsid=id)
#ajax refresh bs data
@main.route('/home/data/<bsid>',methods = ['GET','POST'])
@login_required
def getbsdataAjax(bsid):
    id = int(bsid)
    bsconfig = BSConfig.query.filter_by(bsid=id).first()
    trxNum = TrxConfig.query.filter_by(bs_id=id).count()
    trx = TrxConfig.query.filter_by(bs_id=id).all()
    bsconfig.trxNum=trxNum
    b=bsconfig.as_dict()
    key=('trxid','ssnum')
    t = ((trx[i].trxId,trx[i].ssNum) for i in range(trxNum))
    d = [dict(zip(key,value)) for value in t]
    d.append(b)
    print d
    return json.dumps({'bsid':4,"trxNum":100})



@main.route('/home/<bsid>/<trxid>', methods=['GET','POST'])
@login_required
def home_trx(bsid,trxid):
    return render_template('trx.html',bs=int(bsid),trx=int(trxid))

#trx 
@main.route('/home/<bsid>/<trxid>', methods=['GET','POST'])
@login_required
def channelname(channelname):
    if ( int(channelname) in range(1,7) ): 
        trxconfig = TrxConfig.query.filter_by(trxId=int(channelname)).first()
        #print(type(trxconfig))
        #print(trxconfig)
        if(trxconfig!=None):
            d_trxconfig = trxconfig.as_dict()
            return render_template('channel.html',baudrate=trxconfig.BaudRate,
                modeaddr  = trxconfig.ModeAddr,
                checksum  = trxconfig.CheckSum,
                channel   = trxconfig.Channel,
                airrate   = trxconfig.AirRate,
                txpower   = trxconfig.TxPower,
                sleeptime = trxconfig.SleepTime)
        else:
            return render_template('channel.html',baudrate=0,
                modeaddr  = 0,
                checksum  = 0,
                channel   = 0,
                airrate   = 0,
                txpower   = 0,
                sleeptime = 0)

    else:
        return render_template('404.html')


#get channel config for ajax get
@main.route('/channel/gettrxconfigdata/<channelname>',methods = ['GET','POST'])
@login_required
def GetChannelConfig(channelname):
    id = int(channelname)
    db_trxconfig = TrxConfig.query.filter_by(trxId=int(channelname)).first()
    if ( id in range(1,7)):
        if 0:#ret=sendtobs()
            #
            return json.dumps({"BaudRate":1,"Channel":0})
        else:
            print("-------")
     #       print(json.dumps({"BaudRate":1,"Channel":0}))
            return json.dumps({"BaudRate":1,"Channel":0})


#config channel  for ajax get
@main.route('/config_channel/<channelname>',methods = ['GET','POST'])
@login_required
def Configchannel(channelname):
    
    id = int(channelname)
    if ( id in range(1,7)):
        #get data
        #message = json.loads(request.get_Json)
        msg = {"BaudRate":115200,"ModeAddr":111,"CheckSum":"xxx","Channel":"zzz","AirRate":777,"TxPower":999,"SleepTime":90}
        #send message using udp 
        #dictdata={"a":1,"b":2,"C":4,"d":"yy","e":6,"f":"xx"}
        k=msg.keys()
        v=msg.values()
        fmt='@'
        for value in v:
            if type(value)==int:
                fmt+='i'
            else:
                len_value=len(value)
                fmt+=str(len_value)
                fmt+='s'
    
        print('data format is:%s')%fmt
        data=struct.pack(fmt,*v)
        print msg
        ret = UDPSendtoBS(current_app.config["LOCALADDR"],current_app.config["DESADDR"],msg)
        if not ret:#send success
            data,ret = UDPRecvfromBS(current_app.config["RECVADDR"])
            if (not ret):#recv success
                recvdata=struct.unpack(fmt,data)
                for i in Rang(len(k)):
                    msg[key[i]]=recvdata[i]
                #write to db
                #####
                db_trxconfig = TrxConfig.query.filter_by(trxId=int(channelname)).first().update(msg)
        
                msg['ret']=0
                
                return json.dumps(msg)
        else:#send fail
            return json.dumps({"ret":"failed","error":1})#sending error
            

#config BS  for ajax get
@main.route('/config_Base/<basename>',methods = ['GET','POST'])
@login_required
def ConfigBS(basename):
    id = int(basename)
    db_trxconfig = TrxConfig.query.filter_by(trxId=int(basename)).first()
    return json.dumps({"BaudRate":1,"Channel":0})

@main.route('/map', methods=['GET','POST'])
@login_required
def map():
    return render_template('map.html')
