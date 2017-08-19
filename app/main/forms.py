#coding:UTF-8
from flask_wtf import FlaskForm
from wtforms import FloatField,IntegerField,StringField,TextField,SubmitField
from wtforms.validators import Required,IPAddress,Length, Regexp



class BaseForm(FlaskForm):
    bs_name=StringField('BaseName',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_]*$',0,'BaseName must have only letters,''numbers and underscores')])
    BSIP1=StringField('BSIP1',validators=[IPAddress(ipv4=True, ipv6=False, message=None)])
    BSPort1= IntegerField('BSPort1', validators=[Required()])
    BSIP2=StringField('BSIP2',validators=[IPAddress(ipv4=True, ipv6=False, message=None)])
    BSPort2= IntegerField('BSPort2', validators=[Required()])
    
    ulPacketTime =IntegerField('ulPacketTime',validators=[Required()])
    ulPacketNum  =IntegerField('ulPacketTime',validators=[Required()])
    dlLogicSubFrameNum = IntegerField('dlLogicSubFrame', validators=[Required()])
    dlPacketTime  = IntegerField('dlPacketTime',validators=[Required()])

    ulCompetitionSectionTime = IntegerField('ulCompetitionSectionTime',validators=[Required()])
    sin_family = IntegerField('sin_family', validators=[Required()])
    dlLogicSubFrameIdx = IntegerField('dlLogicSubFrameIdx',validators=[Required()])
    
    def validate_bs_name(self.field):
        if BSConfig.query.filter_by(bs_name=field.data).first():
            raise ValidationError('username already registered')

class TrxForm(FlaskForm):
    trx_name=StringField('TrxName',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_]*$',0,'BaseName must have only letters,''numbers and underscores')])
    TRXIP=StringField('TRXIP',validators=[IPAddress(ipv4=True, ipv6=False, message=None)])
    
    TRXPort= IntegerField('TRXPort1', validators=[Required()])
    TRXTxPower=IntegerField('TRXTxPower',validators=[Required()])
    TRXDataRate =IntegerField('TRXDataRate',validators=[Required()])
    TRXFreq = FloatField('TRXFreq',validators=[Required()])
    
class SSForm(FlaskForm):
    ssID=TextField('ssID',validators=[Required()])
    ssIP=StringField('ssIP',validators=[IPAddress(ipv4=True, ipv6=False, message=None)])
    ssTxPower=IntegerField('ssTxPower',validators=[Required()])
    ssDataRate =IntegerField('ssDataRate',validators=[Required()])
    ssFreq = FloatField('ssFreq',validators=[Required()])

