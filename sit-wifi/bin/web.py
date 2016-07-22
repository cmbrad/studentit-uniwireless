import os
from flask import Flask, jsonify

from lib.check_wireless import student_can_access_uniwireless
from lib.cross_origin import crossdomain


app = Flask(__name__)

staff_username = os.environ.get('LDAP_STAFF_USERNAME')
staff_password = os.environ.get('LDAP_STAFF_PASSWORD')


@app.route('/')
def home():
    return jsonify({
        'error': 'Not a valid endpoint'
    })


@app.route("/<student_username>")
@crossdomain(origin='*')
def check_wireless(student_username):
    try:
        if not staff_username or not staff_password:
            raise Exception('Server misconfiguration. LDAP credentials not set.')
        _, student_id, access, groups = student_can_access_uniwireless(staff_username, staff_password, student_username)
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

