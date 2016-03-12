import os
from flask import Flask

app = Flask(__name__)

staff_username = os.environ.get('LDAP_STAFF_USERNAME')
staff_password = os.environ.get('LDAP_STAFF_PASSWORD')

@app.route("/")
def hello():
    _, student_id, access = student_can_access_uniwireless(staff_username, staff_password, student_username)
    return access


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

