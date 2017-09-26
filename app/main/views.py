#coding:UTF-8

from flask import render_template, redirect, url_for,current_app,request, flash
from flask_login import login_required, current_user
from . import main
from ..import db
from ..models import BSConfig, TRXConfig,SSConfig
import json
from UDPSendRecv import *
from .forms import addBaseForm, BaseForm, TrxForm, SSForm, mform
import struct
import IPy
import socket
packfmt={
  1000:"", #bs add
  1001:"", #bs pull
  1002:"", #bs push
  1100:"",
  1001:"",



}
'''
index
index data
add bs
'''
#index & index_data
@main.route('/', methods=['GET','POST'])
@login_required
def index():
    bsnum=BSConfig.query.filter_by(active=True).count()
    print bsnum
    if bsnum%5==0:
        pagenum = bsnum/5
    else:
        pagenum = bsnum/5+1
    return render_template('index.html',pagenum=pagenum)

@main.route('/index_data',methods=['GET', 'POST'])
@login_required
def page_index_data():#get basenum&its config info
    BSNUM=BSConfig.query.filter_by(active=True).count()
    print BSNUM
    u=BSConfig.query.filter_by(active=True).all()
    page=request.args.get('page')
    p=int(page)
    if 5*p>BSNUM:
        a=5*(p-1)
        b=BSNUM
    else:
        a=5*(p-1)
        b=5*p
    print p,a,b
    key = ('BS_ID', 'BS_Name','num')
    t = ((u[i].BSID,u[i].bs_name, TRXConfig.query.filter_by(BS_ID=u[i].BSID).count()) for i in range(a,b))
    d = [dict(zip(key,value)) for value in t]
    #d= [{'num':'30','id':2},{'num':40,'id':3}]
    print d
    return json.dumps(d)

@main.route('/test', methods=['GET','POST'])
@login_required
def test():
    form=mform()
    code = form['code']
    api=form['api']
    return render_template("formtest.html",form=form, api=api,code=code)
    '''b=BSConfig(bs_name="pfpfp")
    for key in b.__dict__:
        print key,':',b.__dict__[key]
        b.__dict__[key]='axe'
        print key,':',b.__dict__[key]
    form = SSForm()
    if form.validate_on_submit():
        #type(form)
        print form
        dir(form)
        print "aa"
        return "aa"
    else:
        return render_template('formtest.html',form=form)
    '''
@main.route('/addbase', methods=['GET','POST'])
@login_required
def add_bs():
    form = addBaseForm()
    if form.validate_on_submit():
        a= request.form.to_dict()
        print a
        #value check
        #base none
        #write to db
        newbs= BSConfig(bs_name=form.bs_name.data,
                BSIP1=form.BSIP1.data,BSPort1=form.BSPort1.data,
                BSIP2=form.BSIP2.data, BSPort2=form.BSPort2.data,
                ulPacketTime = form.ulPacketTime.data,
                ulPacketNum = form.ulPacketNum.data,
                dlLogicSubFrameNum= form.dlLogicSubFrameNum.data,
                dlLogicSubFrameIdx= form.dlLogicSubFrameIdx.data,
                dlPacketTime= form.dlPacketTime.data,
                ulCompetitionSectionTime = form.ulCompetitionSectionTime.data,
                sin_family = form.sin_family.data,
                #TRXNum = form.TRXNum.data\
                )
        db.session.add(newbs)
        db.session.commit()
        #send to base
           #---package date:head, 3BHIH
           #--payload:   10s15s15s9H
           #--          bs_name 10s
           #--          BSIP1   8s
           #--          BSIP2   8s
           #--1          BSPort1   H (0-65525)
           #--2          BSPort2   H
           #--3     ulPacketTime
           #--4     ulPacketNum
           #--5     dlLogicSubFrameNum
           #--6     dlLogicSubFrameIdx
           #--7     dlPacketTime
           #--8     ulCompetitionSectionTime
           #--9     sin_family
        value=(0x88,0x88,0x00,newbs.BSID,0x00000000, 0x0000,newbs.bs_name.encode('utf-8'), IPy.IP(newbs.BSIP1).strHex()[2:], IPy.IP(newbs.BSIP2).strHex()[2:], newbs.BSPort1,newbs.BSPort2, newbs.ulPacketTime, newbs.ulPacketNum, newbs.dlLogicSubFrameNum,newbs.dlLogicSubFrameIdx, newbs.dlPacketTime, newbs.ulCompetitionSectionTime,newbs.sin_family)
        strt = struct.Struct('!3BHIH10s8s8s9H')
        #print value
        d = strt.pack(*value)
        #print binascii.hexlify(d)
           #---send
        try:
            ret = UDPSendtoBS((current_app.config['SERVER_ADDR'],current_app.config['SERVER_PORT_S']),\
                          (current_app.config['BASE_ADDR'],current_app.config['BASE_PORT']),d)
            if ret==0:
                flash('server have sended base config successfully!')
            else:
                flash('sending data failed!')
        except:
            db.session.delete(newbs)
            db.session.commit()
            flash('sending msg failed!')
        try:
            data = UDPRecvfromBS((current_app.config['BASE_ADDR'],current_app.config['SERVER_PORT_R']))
            strt_b=struct.Struct('!4s')
            d_b = strt_b.unpack(data)
            flash('config succeded!')
            print d_b
        except:
            db.session.delete(newbs)
            db.session.commit()
            flash('no response!')


        return redirect(url_for('main.index'))
    else:
        return render_template('addbase.html',form=form)


'''base page
page    --- /bs/<bsid>
page's data ---/bs/<bsid>/base_data
push bscfg ---/bs/<bsid>/push_bscfg
pull bscfg ---/bs/<bsid>/pull_bscfg
add trx ---/bs/<bsid>/addtrx
'''
@main.route('/bs/<bsid>', methods=['GET','POST'])
@login_required
def bs(bsid):
    id = int(bsid)
    bs = BSConfig.query.filter_by(BSID=id).first()
    if bs == None:
        return render_template('404.html'),404
    form = BaseForm(bs=None)
    return render_template('base.html', bsid=id, form=form, msg=0)

@main.route('/bs/<bsid>/base_data',methods = ['GET','POST'])
@login_required
def page_base_data(bsid):
    bsconfig = BSConfig.query.filter_by(BSID=int(bsid)).first()
    trxNum = TRXConfig.query.filter_by(BS_ID=int(bsid)).count()
    trx = TRXConfig.query.filter_by(BS_ID=int(bsid)).all()
    bscfg=bsconfig.as_dict()
    key=('trxid', 'trx_name','ssnum')
    t = ((trx[i].TRXID, trx[i].trx_name, SSConfig.query.filter_by(TRX_ID=trx[i].TRXID).count()) for i in range(trxNum))
    d = [dict(zip(key,value)) for value in t]
    d.append(bscfg)
    print d
    p= [{'num':'30','id':2},{'num':40,'id':3}]
    return json.dumps(d)

@main.route('/bs/<bsid>/pull_bscfg',methods=['GET', 'POST'])
@login_required
def pull_bscfg(bsid):
    b=BSConfig.query.filter_by(BSID=bsid).first()
    #send to base
    #pull base cfg
    errormsg='none'
    value = (0x88, 0x88, 0x21, b.BSID)
    s=struct.Struct('!3BH')
    d=s.pack(*value)
    try:
        ret = UDPSendtoBS((current_app.config['SERVER_ADDR'], current_app.config['SERVER_PORT_S']), \
                          (current_app.config['BASE_ADDR'], current_app.config['BASE_PORT']), d)
        try:
            rowdata = UDPRecvfromBS((current_app.config['BASE_ADDR'], current_app.config['SERVER_PORT_R']))
            print "a"
            strt = struct.Struct('!3BHIH10s8s8s9H')
            #wait for a bscfg msg from bs wait time: 15s
            try:
                pdata= strt.unpack(rowdata)
                if pdata[0] is not 0x88 or pdata[1] is not 0x88 or\
                    pdata[2] is not 0x21 or\
                    pdata[3] is not b.BSID:
                    b.bs_name = pdata[6]
                    b.BSIP1 = pdata[7]
                    b.BSIP2 = pdata[8]
                    b.BSPort1 = pdata[9]
                    b.BSPort2 = pdata[10]
                    b.ulPacketTime = pdata[11]
                    b.ulPacketNum = pdata[12]
                    b.dlLogicSubFrameNum=pdata[13]
                    b.dlLogicSubFrameIdx=pdata[14]
                    b.dlPacketTime=pdata[15]
                    b.ulCompetitionSectionTime=pdata[16]
                    b.sin_family=pdata[17]
                    db.session.add(b)
                    db.session.commit()
                else:
                    errormsg='wrong_data'
            except socket.error, e:
                errormsg=e
        except socket.error, e:
            errormsg=e.message

    except socket.error, e:
        errormsg=e
    #depack the msg & write to db
    #d={'ret':0,'BSName':'aa', 'BSIP1':'192.168.1.1'}
    #print "c"
    data=b.config_as_dict()
    data['errors']=errormsg
    print data
    return json.dumps(data)

@main.route('/bs/<bsid>/push_bscfg',methods=['GET', 'POST'])
@login_required
def push_bscfg(bsid):
    b=BSConfig.query.filter_by(BSID=bsid).first()
    #db.session.delete(bs_origin)
    #db.session.commit()
    #b=BSConfig()
    form = BaseForm(bs=b)
    print form.validate()
    print form.errors
    #print form.BSPort1.data
    #print form.bs_name.data
    #print type(form.BSPort1.data)
    #a= request.form.to_dict()
    #print a
    #key = a.keys()
    if request.method == 'POST' and form.validate():        #value check
        #base none
        #write to trx_db
        b.bs_name = form.bs_name.data
        b.BSIP1   = form.BSIP1.data
        b.BSPort1 = form.BSPort1.data
        b.BSIP2   = form.BSIP2.data
        b.BSPort2 = form.BSPort2.data
        b.ulPacketTime = form.ulPacketTime.data
        b.ulPacketNum  = form.ulPacketNum.data
        b.dlLogicSubFrameNum = form.dlLogicSubFrameNum.data
        b.dlLogicSubFrameIdx = form.dlLogicSubFrameIdx.data
        b.dlPacketTime = form.dlPacketTime.data
        b.ulCompetitionSectionTime = form.ulCompetitionSectionTime.data
        b.sin_family = form.sin_family.data
        print b.as_dict()
        print b.config_as_dict()
        db.session.add(b)
        '''#send to base
           #---package date:head, 3BHIH
           #--payload:   10s15s15s9H
           #--          bs_name 10s
           #--          BSIP1   8s
           #--          BSIP2   8s
           #--1          BSPort1   H (0-65525)
           #--2          BSPort2   H
           #--3     ulPacketTime
           #--4     ulPacketNum
           #--5     dlLogicSubFrameNum
           #--6     dlLogicSubFrameIdx
           #--7     dlPacketTime
           #--8     ulCompetitionSectionTime
           #--9     sin_family'''
        value=(0x88,0x88,0x31,b.BSID,0x00000000, 0x0000,b.bs_name.encode('utf-8'), IPy.IP(b.BSIP1).strHex()[2:], IPy.IP(b.BSIP2).strHex()[2:], \
               b.BSPort1,b.BSPort2, b.ulPacketTime, b.ulPacketNum, b.dlLogicSubFrameNum,b.dlLogicSubFrameIdx, b.dlPacketTime, \
               b.ulCompetitionSectionTime,b.sin_family)
        #s = struct.Struct(packfmt[10000])
        strt = struct.Struct('!3BHIH10s8s8s9H')
        #print value
        d = strt.pack(*value)
        #print binascii.hexlify(d)
           #---send
        errormsg = 'none'
        try:
            ret = UDPSendtoBS((current_app.config['SERVER_ADDR'], current_app.config['SERVER_PORT_S']), \
                              (current_app.config['BASE_ADDR'], current_app.config['BASE_PORT']), d)
            try:
                rowdata = UDPRecvfromBS((current_app.config['BASE_ADDR'], current_app.config['SERVER_PORT_R']))
                strt_b = struct.Struct('!4s')
                d_b = strt_b.unpack(rowdata)
                #check d_b to know
            except socket.error,e:
                errormsg = 'receive:'+e.message
        except socket.error, e:
            errormsg = 'send:'+e.message
        if errormsg=='none':
            return redirect(url_for('main.bs',form=form, bsid=int(bsid), msg=1))
        else:
            db.session.rollback()
            flash(errormsg)
            return redirect(url_for('main.bs',form=form, bsid=int(bsid), msg=2))
    else:
        return render_template('bs.html',form=form,bsid=int(bsid),msg=2)

@main.route('/bs/<bsid>/addtrx', methods = ['GET', 'POST'])
@login_required     
def add_trx(bsid):
    bs = BSConfig.query.filter_by(BSID=int(bsid)).first()
    form = TrxForm()
    if form.validate_on_submit():
        #value test
        for trx_t in bs.TRXs:
            if trx_t.trx_name==form.trx_name.data:
                form.errors = 'aaa'
                print form.errors
                return render_template('addtrx.html', bsid=int(bsid), form=form)
        #send to bs
        #write to db
        trx = TRXConfig(trx_name=form.trx_name.data,
                TRXIP       = form.TRXIP.data,
                TRXPort     = form.TRXPort.data,
                TRXTxPower  = form.TRXTxPower.data,
                TRXDataRate = form.TRXDataRate.data,
                TRXFreq     = form.TRXFreq.data,
                BS_ID       = int(bsid))
        db.session.add(trx)
        db.session.commit()
        success=0
        try:
            #pack data
            struct_type = struct.Struct('!3BHIH10s8s4H')
            value=(0x88, 0x88, 0x13, trx.BS_ID, trx.TRXID, 0, trx.trx_name.encode('utf-8'), IPy.IP(trx.TRXIP).strHex()[2:], trx.TRXPort, trx.TRXTxPower, trx.TRXDataRate, trx.TRXFreq)
            data = struct_type.pack(*value)
            try:
                ret = UDPSendtoBS((current_app.config['SERVER_ADDR'], current_app.config['SERVER_PORT_S']), \
                                  (current_app.config['BASE_ADDR'], current_app.config['BASE_PORT']), data)
                try:
                    recv_data = UDPRecvfromBS((current_app.config['BASE_ADDR'], current_app.config['SERVER_PORT_R']))
                    strt_b = struct.Struct('!4s')
                    d_b = strt_b.unpack(recv_data)
                    if d_b=='aaaa':
                        success = 0
                    else:
                        success = 1
                except socket.error, e:
                    success = 1
                    flash(e)
                    #recv error

            except socket.error, e:
                #send error
                success = 1
                flash(socket.error)
        except socket.error, e:
            #pack error
            success = 1
            flash(socket.error)
        if success==1:
            flash('failed!')
            db.session.delete(trx)
            return render_template('addtrx.html', bsid=int(bsid), form=form)

        return redirect(url_for('main.bs', bsid=int(bsid)))
    else:
        return render_template('addtrx.html',bsid=int(bsid),form=form)


'''
trx url

trx data

add terminal

trx config---pull cfg
          ---push cfg


'''

@main.route('/bs/<bsid>/<trxid>', methods=['GET','POST'])
@login_required
def trx(bsid,trxid):
    form = TrxForm()
    return render_template('trx.html',form = form, bs=int(bsid),trx=int(trxid))


@main.route('/bs/<bsid>/<trxid>/data', methods=['GET','POST'])
@login_required
def trx_data(bsid,trxid):
    tr = TRXConfig.query.filter_by(TRXID=int(trxid)).first()
    terminal = tr.SSs
    #print terminal
    #print terminal[0].ss_name
    d = [{ 'ss_name': t.ss_name, 'ssip': t.SSIP } for t in terminal]
    d.append(tr.as_dict())
    #print d
    #d=[{'ssid':550,},{'ssid':5690,},{'ssid':4565},{'trxIp':'192.168.1.156','trxPort':'8080'}]
    return json.dumps(d)

#add ss / registe ss
@main.route('/bs/<bsid>/<trxid>/addss',methods = ['GET','POST'])
@login_required
def addss(bsid,trxid):
    bsid, trxid= int(bsid), int(trxid)
    trx = TRXConfig.query.filter_by(TRXID=trxid).first()
    #print trx.SSs
    SS_Names = [ x.ss_name for x in trx.SSs]
    SS_IPs = [ x.SSIP for x in trx.SSs]
    #print SS_Names, SS_IPs
    form = SSForm()
    if form.validate_on_submit():
        if form.ss_name.data in SS_Names or form.ssIP in SS_IPs:
            form.errors='trx_name has existed!'
            return redirect(url_for('main.trx',bsid=int(bsid),trxid=int(trxid)))

        t = SSConfig(ss_name=form.ss_name.data,SSIP=form.ssIP.data,TRX_ID=trxid)
        db.session.add(t)
        db.session.commit()
        success = 0
        try:
            # pack data
            struct_type = struct.Struct('!3BHIH10s8s')
            value = (0x88, 0x88, 0x13, bsid, trxid, t.SSID, t.ss_name.encode('utf-8'), IPy.IP(t.SSIP).strHex()[2:])
            data = struct_type.pack(*value)
            try:
                ret = UDPSendtoBS((current_app.config['SERVER_ADDR'], current_app.config['SERVER_PORT_S']), \
                                  (current_app.config['BASE_ADDR'], current_app.config['BASE_PORT']), data)
                try:
                    recv_data = UDPRecvfromBS((current_app.config['BASE_ADDR'], current_app.config['SERVER_PORT_R']))
                    strt_b = struct.Struct('!4s')
                    d_b = strt_b.unpack(recv_data)
                    if d_b == 'aaaa':
                        success = 0
                    else:
                        success = 1

                except socket.error, e:
                    success = 1
                    error_msg = e
                    print type(error_msg)
                    # flash(error_msg)
                    # recv error
            except socket.error, e:
                # send error
                success = 1
                flash(socket.error)
        except socket.error, e:
            # pack error
            success = 1
            flash(socket.error)
        if success == 1:
            flash('add ss failed!')
            db.session.delete(t)
            return render_template('addss.html', bsid=bsid, form=form, trxid=trxid)
        return redirect(url_for('main.trx',bsid=int(bsid),trxid=int(trxid)))
    else:
        return render_template('addss.html',form=form,bsid=bsid,trxid=trxid)

#pull trx config
@main.route('/bs/<bsid>/<trxid>/pull_trxcfg',methods = ['GET','POST'])
@login_required
def PullTrxCfg(bsid,trxid):
    trx_db=TRXConfig.query.filter_by(TRXID=int(trxid)).first()
    print trx_db.as_dict()
    return json.dumps(trx_db.as_dict())


@main.route('/bs/<bsid>/<trxid>/push_trxcfg',methods=['GET', 'POST'])
@login_required
def Push_TrxCfg(bsid,trxid):
    t=TRXConfig.query.filter_by(TRXID=int(trxid)).first()
    print request.form['trx_name']
    # t.trx_name  = request.form['trx_name']
    # t.TRXIP     = request.form['TRXIP']
    # t.TRXPort   = request.form['TRXPort']
    # t.TRXPower  = request.TRXPort.data
    # t.TRXDataRate = request.TRXDataRate.data
    # t.TRXFreq = request.TRXFreq.data
    return redirect(url_for('main.trx', bsid=int(bsid), trxid=int(trxid)))
    '''
        db.session.add(t)
        db.session.commit()
        #send to base
           #---package date:head, 3BHIH
           #--payload:   10s15s15s9H
           #--          bs_name 10s
           #--          BSIP1   8s
           #--          BSIP2   8s
           #--1          BSPort1   H (0-65525)
           #--2          BSPort2   H
           #--3     ulPacketTime
           #--4     ulPacketNum
           #--5     dlLogicSubFrameNum
           #--6     dlLogicSubFrameIdx
           #--7     dlPacketTime
           #--8     ulCompetitionSectionTime
           #--9     sin_family
        value=(0x88,0x88,0x00,newbs.BSID,0x00000000, 0x0000,newbs.bs_name.encode('utf-8'), IPy.IP(newbs.BSIP1).strHex()[2:], IPy.IP(newbs.BSIP2).strHex()[2:], newbs.BSPort1,newbs.BSPort2, newbs.ulPacketTime, newbs.ulPacketNum, newbs.dlLogicSubFrameNum,newbs.dlLogicSubFrameIdx, newbs.dlPacketTime, newbs.ulCompetitionSectionTime,newbs.sin_family)
        #s = struct.Struct(packfmt[10000])
        strt = struct.Struct('!3BHIH10s8s8s9H')
        print value
        d = strt.pack(*value)
        ret = UDPSendtoBS(current_app.config["LOCALADDR"],current_app.config["DESADDR"],d)
        #feedback

        return redirect(url_for('main.index'))
    else:
        return render_template('addbase.html',form=form)
        
        return redirect(url_for('main.trx',bsid=int(bsid),trxid=int(trxid)))
    '''


@main.route('/bs/<bsid>/<trxid>/push_trxcfg_DataCheck', methods=['GET', 'POST'])
@login_required
def Push_TrxCfg_DataCheck(bsid, trxid):
    #value check
    d={}
    t=TRXConfig.query.filter_by(TRXID=int(trxid)).first()
    bss=BSConfig.query.filter_by(BSID=int(bsid)).first()
    trx_names=[b.trx_name for b in bss.TRXs]
    trx_IPs=[b.TRXIP for b in bss.TRXs]
    print trx_names
    trx_name = request.form['trx_name']
    TRXIP = request.form['TRXIP']
    if (trx_name == t.trx_name) or (trx_name not in trx_names):
        d['trx_name'] = 0
    else:
        d['trx_name'] = 2
    if (TRXIP is t.TRXIP) or (TRXIP not in trx_IPs):
        d['TRXIP'] = 0
    else:
        d['TRXIP'] = 2
    print d
    return json.dumps(d)
        


@main.route('/map/<bsid>', methods=['GET','POST'])

def map(bsid):
    if request.method == 'GET':        #value check
        return render_template('map.html')
    else:
        assert request.method == 'POST'
        print request.form['lon'], request.form['lat'], request.form['radius']


    #    print type(request_data)
     #   print request_data
        d=[{'trxID':'1', 'GPS':'', 'status': 'on'}, {'trxID':'3', 'GPS':'', 'status': 'off'}, {'trxID':'4', 'GPS':'', 'status': 'on'}]
        return json.dumps(d)