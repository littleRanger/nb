#coding:UTF-8
from flask_wtf import FlaskForm
from wtforms import FloatField,IntegerField,StringField,TextField,SubmitField
from wtforms.validators import Required,IPAddress



class SSForm(FlaskForm):
    ssID=TextField('ssID',validators=[Required()])
    ssIP=StringField('ssIP',validators=[IPAddress(ipv4=True, ipv6=False, message=None)])
    ssTxPower=IntegerField('ssTxPower',validators=[Required()])
    ssDataRate =IntegerField('ssDataRate',validators=[Required()])
    ssFreq = FloatField('ssFreq',validators=[Required()])

