#coding:UTF-8

from flask import render_template, redirect, url_for,current_app,request
from flask_login import login_required
from . import main
from ..models import BSConfig,TrxConfig
from ...config import config
import json

@main.route('/', methods=['GET','POST'])
@login_required
def index():
    id =1 
    bs = BSConfig.query.filter_by(bsid=id).first()     
    return render_template('home.html')

@main.route('/home', methods=['GET','POST'])
@login_required
def home():
    return render_template('home.html')

@main.route('/home/data',methods = ['GET','POST'])
@login_required
def dataAjax():
    bsconfig = BSConfig.query.filter_by(bsid=1).first()

    #print(json.dumps(bsconfig.as_dict()))
    return json.dumps(bsconfig.as_dict())



@main.route('/channel', methods=['GET','POST'])
@login_required
def channel():
    return render_template('channel.html')

#channel 
@main.route('/channel/<channelname>', methods=['GET','POST'])
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
        if !ret:#send success
            data,ret = UDPRecvfromBS(current_app.config["RECVADDR"])
            if !ret:#recv success
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
def GetChannelConfig(basename):
    id = int(channelname)
    db_trxconfig = TrxConfig.query.filter_by(trxId=int(channelname)).first()
    if ( id in range(1,7)):
        if 0:#ret=communicateToBS()
            #
            return json.dumps({"BaudRate":1,"Channel":0})
        else:
            print("-------")
     #       print(json.dumps({"BaudRate":1,"Channel":0}))
            return json.dumps({"BaudRate":1,"Channel":0})

@main.route('/map', methods=['GET','POST'])
@login_required
def map():
    return render_template('map.html')
