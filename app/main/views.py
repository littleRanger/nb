#coding:UTF-8

from flask import render_template, redirect, url_for,current_app,request
from flask_login import login_required,current_user
from . import main
from ..models import BSConfig,TRXConfig,SSConfig
import json
from UDPSendRecv import *
from ..decorators import admin_required
from .forms import BaseForm,TrxForm,SSForm

'''
index
index data
add bs
'''
#index & index_data
@main.route('/', methods=['GET','POST'])
@login_required
def index():
    return render_template('index.html')

@main.route('/index_data',methods=['GET', 'POST'])
@login_required
def page_index_data():#get basenum&its config info
    BSNUM=BSConfig.query.filter_by(active=True).count()
    u=BSConfig.query.filter_by(active=True).all()
    key = ('id','num')
    t = ((u[i].BSID,u[i].TRXNum) for i in range(BSNUM))
    d = [dict(zip(key,value)) for value in t]
    #d= [{'num':'30','id':2},{'num':40,'id':3}]
    print d
    return json.dumps(d)

@main.route('/addbase', methods=['GET','POST'])
@login_required
def add_bs():
    form = BaseForm()
    if form.validate_on_submit():
        a= request.form.to_dict()
        print a
#send to base

#feedback

#write to db 
        return redirect(url_for('main.index'))
    else:
        return render_template('addbase.html',form=form)


'''base page
page    --- /bs/<bsid>  
page's data ---/bs/<bsid>/base_data
deploy base ---/bs/<bsid>/deploy_bscfg
get basecfg ---/bs/<bsid>/get_bscfg
add trx ---/bs/<bsid>/addtrx
'''
@main.route('/bs/<bsid>', methods=['GET','POST'])
@login_required
def bs(bsid):
    id = int(bsid)
    '''bs = BSConfig.query.filter_by(BSID=id).first()
    if bs != None:
        d=bs.as_dict()'''
    return render_template('bs.html',bsid=id)

@main.route('/bs/<bsid>/base_data',methods = ['GET','POST'])
@login_required
def page_base_data(bsid):
    id = int(bsid)
    bsconfig = BSConfig.query.filter_by(BSID=id).first()
    trxNum = TRXConfig.query.filter_by(BS_ID=id).count()
    trx = TRXConfig.query.filter_by(BS_ID=id).all()
    bsconfig.TRXNum=trxNum
    b=bsconfig.as_dict()
    key=('trxid','ssnum')
    t = ((trx[i].TRXID,trx[i].SSNum) for i in range(trxNum))
    d = [dict(zip(key,value)) for value in t]
    d.append(b)
    print d
    return json.dumps(d)

@main.route('/bs/<bsid>/addtrx', methods = ['GET', 'POST'])
@login_required
def add_trx(bsid):
    id = int(bsid)
    bs = BSConfig.query.filter_by(BSID=id).first()
    trxform = TRXForm(bs_name=bs.user_name)
    if form.validate_on_submit():
        


'''
trx url

trx data

trx config---pull cfg
          ---push cfg
'''

@main.route('/bs/<bsid>/<trxid>', methods=['GET','POST'])
@login_required
def trx(bsid,trxid):
    return render_template('trx.html',bs=int (bsid),trx=int(trxid))

 
@main.route('/bs/<bsid>/<trxid>/data', methods=['GET','POST'])
@login_required
def trx_data(bsid,trxid):
    d=[{'ssid':550,},{'ssid':5690,},{'ssid':4565},{'trxIp':'192.168.1.156','trxPort':'8080'}]
    return json.dumps(d)

#add ss 
@main.route('/bs/<bsid>/<trxid>/addss',methods = ['GET','POST'])
@login_required
def addss(bsid,trxid):
    bsid = int(bsid)
    trxid = int(trxid)
    form = SSForm()
    if form.validate_on_submit():
        a= request.form.to_dict()
        return redirect(url_for('main.trx',bsid=int(bsid),trxid=int(trxid)))
    else:
        return render_template('addss.html',form=form,bsid=bsid,trxid=trxid)

#push,pull trx config
@main.route('/bs/<bsid>/<trxid>/trx_cfg',methods = ['GET','POST'])
@login_required
def PushTrxCfg(bsid,trxid):
    bsid = int(bsid)
    trxid = int(trxid)
    print bsid,trxid
    #push cfg
    if request.method == 'POST':
        a= request.form
        print a.to_dict()
         
        return json.dumps({'ret':0,})
    if request.method ==  'GET':# get cfg 
        d={'trxip':'192.168.8.8','trxPort':8000}
        print request.form
        print 'aaa'

        return json.dumps(d)

    '''
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

'''
#config BS  for ajax get
@main.route('/config_Base/<basename>',methods = ['GET','POST'])
@login_required
def ConfigBS(basename):
    id = int(basename)
    db_trxconfig = TrxConfig.query.filter_by(trxId=int(basename)).first()
    return json.dumps({"BaudRate":1,"Channel":0})

'''





'''


@main.route('/map', methods=['GET','POST'])
@login_required
def map():
    return render_template('map.html')
