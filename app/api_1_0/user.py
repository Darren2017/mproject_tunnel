#encoding: utf-8
from . import api
from ..models import Message
from flask import request, jsonify
from app import db
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')


@api.route('/message/', methods=['POST'])
def message():
    sent_content = request.get_json().get('sent_content')
    sent_name = request.get_json().get('sent_name')
    sent_time_try = request.get_json().get('sent_time')
    sent_address = request.get_json().get('sent_address')

    sent_time = sent_time_try[0:10]

    fcontent = '华大桂声，伴你同行'
    #fcontent.decode('utf-8').encode('gb18030')
    fname = '来自一直惦记着你的'
    #fname.decode('utf-8').encode('gb18030')


    message = Message(content=sent_content + '\n' + fcontent,
                    way=2,
                    name=fname+sent_name,
                    time=sent_time,
                    address=sent_address,
                    status=1,
                    writetime = time.strftime("%d/%m/%Y"))
    try:
        db.session.add(message)
        db.session.commit()
        return jsonify({
        }), 201
    except:
        return jsonify({
        }), 500

'''@api.route('/file/', methods=['POST'])
def files():
    try:
        message = Message.query.all()
        num = len(message)
        soufile = request.files['soundfile']
        picfile = request.files['picturefile']
        soufile.save('/tmp/'+str(num) + '.wav')
        picfile.save('/tmp/'+str(num) + '.jpg')
        return jsonify({
        }), 201
    except:
        return jsonify({
        }), 500'''
