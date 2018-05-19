from . import api
from flask import request, jsonify, session, current_app
from ..models import Message as ME
from flask_mail import Message, Mail
from .. import app, db
import os
from config import config
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



def confirm(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return False
    if data.get('id') != 1:
        return False
    return True

app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mails = Mail(app)

def msg_dict2(to, subject, body, **kwargs):
    msg = Message(
        subject='come from ' + subject,
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=[to]
    )
    msg.body = body
    msg.html = body
    return msg.__dict__

def send_async_email(msg_dict):
    with app.app_context():
        msg = Message()
        msg.__dict__.update(msg_dict)
        mails.send(msg)


@api.route('/sent/<int:id>/', methods=['POST'])
def sent(id):
    token = request.headers['token']
    #token1 = session.get('token')
    #if token == token1:
    if confirm(token):
        mess = ME.query.filter_by(id=id).first()
        if mess.way == 2:
            try:
                send_async_email(msg_dict2(mess.address, mess.name, mess.content))
                mess.status = 2
                db.session.add(mess)
                db.session.commit()
                return jsonify({}), 200
            except:
                mess.status = 3
                db.session.add(mess)
                db.session.commit()
                return jsonify({}), 500
        elif mess.way == 1:
            pass
    return jsonify({}), 404