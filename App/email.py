from flask import render_template,current_app
from flask_mail import Message
from threading import Thread
from App.extensions import mail




#异步发送
def send_mail_async(app,msg):
    #管理程序上下文
    with app.app_context():
        mail.send(msg)


def send_mail(subject,to,**kwargs):
    app = current_app._get_current_object() #拿到实例化的flask对象App
    msg = Message(subject=subject,recipients=[to],sender=app.config['MAIL_USERNAME'])
    msg.html = render_template('home/email/activate.html',**kwargs)
    thr = Thread(target=send_mail_async,args=[app,msg]) #创建线程
    thr.start() #开启线程
    return '发送邮件'
