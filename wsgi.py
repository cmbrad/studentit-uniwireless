#!/usr/bin/env python

import os, sys

sys.path.insert(0, '/apps/studentit-uniwireless/sit-wifi')
#from bin.web import app as application

def application(environ, start_response):
    for key in ['LDAP_STAFF_USERNAME', 'LDAP_STAFF_PASSWORD']:
        os.environ[key] = environ.get(key, '')
    from bin.web import app as _application

    return _application(environ, start_response)
