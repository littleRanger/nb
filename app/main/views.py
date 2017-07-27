#coding:UTF-8

from flask import render_template
from flask_login import login_required
from . import main
from ..models import BSConfig
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
    print("a")
    bsconfig = BSConfig.query.filter_by(bsid=1).first()
    return json.dumps(bsconfig.as_dict())

@main.route('/channel/trxconfigdata',methods = ['GET','POST'])
@login_required
def GetChannelConfig():
    trxconfig = TrxConfig.query.filter_by(trxId=1).first()
    print trxconfig
    return json.dumps(trxconfig.as_dict())


@main.route('/channel', methods=['GET','POST'])
@login_required
def channel():
    return render_template('channel.html')

@main.route('/map', methods=['GET','POST'])
@login_required
def map():
    return render_template('map.html')
