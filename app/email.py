#coding:UTF-8
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

def send_async_email(app, msg):
    with app.app_context():
        print "sending_next"
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    print "start to send "
    app = current_app._get_current_object()
    msg = Message(app.config['NB_MAIL_SUBJECT_PREFIX']+subject, sender = app.config['NB_MAIL_SENDER'],recipients=[to] )
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    thr = Thread(target=send_async_email, args = [app,msg])
    thr.start()
    print 111
    return thr
'''def send_email(to, subject, template, **kwargs):
    print "start to send "
    app = current_app._get_current_object()
    msg = Message(app.config['NB_MAIL_SUBJECT_PREFIX']+subject, sender = app.config['NB_MAIL_SENDER'],recipients=[to] )
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    mail.send(msg)
'''
