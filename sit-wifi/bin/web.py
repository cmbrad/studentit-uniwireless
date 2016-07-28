import os
import json

import jwt
from flask import Flask, jsonify, request

from lib.check_wireless import student_can_access_uniwireless, connect_to_ldap, StudentNotExistException
from lib.cross_origin import crossdomain


app = Flask(__name__)

staff_username = os.environ.get('LDAP_STAFF_USERNAME')
staff_password = os.environ.get('LDAP_STAFF_PASSWORD')
secret = os.environ.get('WIFI_APP_SECRET_KEY', 'studentit')


def login_required(f):
   def decorated(*args, **kwargs):
       auth = request.authorization

       if auth is None:
           return jsonify({'error': 'Authorisation required'})

       try:
           decoded_token = jwt.decode(auth['username'], secret)
       except:
           return jsonify({'error': 'Invalid token'})

       return f(*args, **kwargs)

   return decorated


@app.route('/')
@crossdomain(origin='*')
def home():
    return jsonify({
        'error': 'Not a valid endpoint'
    })


@app.route('/auth', methods=["OPTIONS", "POST"])
@crossdomain(origin='*')
def auth():
    try:
        data = request.get_json()
        if len(data['username']) == 0:
            raise Exception('Username cannot be blank')
        connect_to_ldap(data['username'], data['password'])
    except Exception as e:
        return jsonify({
            'error': e.message
        })

    access_token = jwt.encode({'username': data['username']}, secret)

    return jsonify({
      'access_token': access_token
    })


@app.route("/check/<student_username>", methods=["GET", "OPTIONS"])
@crossdomain(origin='*')
@login_required
def check_wireless(student_username):
    try:
        if not staff_username or not staff_password:
            raise Exception('Server misconfiguration. LDAP credentials not set.')
        _, student_id, access, groups = student_can_access_uniwireless(staff_username, staff_password, student_username)
    except StudentNotExistException as e:
        resp = jsonify({"error": e.message, "username": e.username})
        #resp.status_code = 404
        return resp
    except Exception as e:
        return jsonify({
            'error': e.message
        })

    return jsonify({
        "username": student_username,
        "id": student_id,
        "access": access,
        "groups": groups
    })


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

