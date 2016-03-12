#!env/bin/python

import os
import click

from lib.check_wireless import student_can_access_uniwireless


@click.command()
@click.option('--staff-username')
@click.option('--student-username', required=True)
def search_ldap(staff_username, student_username):
    # If a staff username was provided on the command line then
    # override the environment variable.
    if not staff_username:
        staff_username = os.environ.get('LDAP_STAFF_USERNAME')

    # Only allow passwords in environment variables for security reasons
    staff_password = os.environ.get('LDAP_STAFF_PASSWORD')

    # We need login info to continue. Die if it doesn't exist
    if not staff_username or not staff_password:
        print('ERROR: Missing LDAP_STAFF_USERNAME or LDAP_STAFF_PASSWORD environment variable.')
        return

    _, student_id, access= student_can_access_uniwireless(staff_username, staff_password, student_username)

    print ('{} ({}) can {} UniWireless.'.format(
            student_username,
            student_id,
            'access' if access else 'not access'))


if __name__ == '__main__':
    search_ldap()

