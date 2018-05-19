#encoding: utf-8
from . import api
from ..models import Message
from flask import request, jsonify
from app import db

@api.route('/message/', methods=['POST'])
def message():
    sent_content = request.get_json().get('sent_content')
    sent_name = request.get_json().get('sent_name')
    sent_time = request.get_json().get('sent_time')
    sent_address = request.get_json().get('sent_address')

    message = Message(content=sent_content,
                      way=2,
                      name=sent_name,
                      time=sent_time,
                      address=sent_address,
                      status=1)
    try:
        db.session.add(message)
        db.session.commit()
        return jsonify({
        }), 200
    except:
        return jsonify({
        }), 500