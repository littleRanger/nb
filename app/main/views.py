#coding:UTF-8

from flask import render_template, redirect, url_for
from flask_login import login_required
from . import main
from ..models import BSConfig,TrxConfig
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
    print bsconfig.as_dict()
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
        d_trxconfig = trxconfig.as_dict()
        return render_template('channel.html',baudrate=trxconfig.BaudRate,
            modeaddr  = trxconfig.ModeAddr,
            checksum  = trxconfig.CheckSum,
            channel   = trxconfig.Channel,
            airrate   = trxconfig.AirRate,
            txpower   = trxconfig.TxPower,
            sleeptime = trxconfig.SleepTime)
    else:
        return render_template('404.html')

#get channel config for ajax get
@main.route('/channel/gettrxconfigdata/<channelname>',methods = ['GET','POST'])
@login_required
def GetChannelConfig(channelname):
    if ( int(channelname) in range(1,7)):
        if 1==2:
            #CommunicateToBS()
            return 0#json.dumps(trxconfig.as_dict())
        else:
            return 0

@main.route('/map', methods=['GET','POST'])
@login_required
def map():
    return render_template('map.html')
