#!env/bin/python

import os
import ldap

# LDAP configuraiton information
LDAP_URI = 'ldaps://student.unimelb.edu.au/'
LDAP_STAFF_DN = 'cn={username},OU=People,DC=unimelb,DC=edu,DC=au'
LDAP_STUDENT_DN = 'cn={username},ou=Students,dc=student,dc=unimelb,dc=edu,dc=au'

# If students are in this group then they have access to uniwireless. To be in
# this group they must be enrolled in at least one subject.
STUDENT_GROUP = 'CN=Students-g,OU=SubjectGroups,DC=student,DC=unimelb,DC=edu,DC=au'

# What we return when ldap attribute is missing. Return in a list as LDAP returns list
UNKNOWN = ['UNKNOWN']


def student_in_correct_group(groups):
    return STUDENT_GROUP in groups


def student_can_access_uniwireless(staff_username, staff_password, student_username):
    ldap_client = connect_to_ldap(staff_username, staff_password)

    try:
        results = ldap_client.search_s(
            LDAP_STUDENT_DN.format(username=student_username),
            ldap.SCOPE_BASE
        )

        # Get index 0 because there'll only ever be one student per username
        # Get index 1 because that's where the information is in the result
        student_info = results[0][1]

        username = student_info.get('uid', UNKNOWN)[0]
        student_id = student_info.get('employeeID', UNKNOWN)[0]

        groups = student_info.get('memberOf', [])

        return (username, student_id, student_in_correct_group(groups), groups)
    except ldap.NO_SUCH_OBJECT as e:
        raise Exception('No student with username {} exists.'.format(student_username))

    ldap_client.unbind_s()

    return ('', '', False, [])


def connect_to_ldap(staff_username, staff_password):
    ldap_client = ldap.initialize(LDAP_URI)
    # Referrals can cause the connection to hang. Turn them off
    ldap_client.set_option(ldap.OPT_REFERRALS, 0)
    # We need SSL to connect but don't have the cert, just ignore it
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

    # Connect to the server with staff credentials
    ldap_client.bind_s(
        LDAP_STAFF_DN.format(username=staff_username),
        staff_password
    )

    return ldap_client

