#!env/bin/python

import os
import click

from lib.check_wireless import student_can_access_uniwireless


@click.command()
@click.option('--staff-username', required=True, help='Username for a UoM staff account in the UNIMELB domain')
@click.option('--staff-password', required=True, help='Password for the passed username')
@click.option('--student-username', required=True, help='Username of the student to check for access')
@click.option('--show-groups', is_flag=True, help='Print AD groups the user is a part of')
def search_ldap(staff_username, staff_password, student_username, show_groups):
    try:
        _, student_id, access, groups = student_can_access_uniwireless(staff_username, staff_password, student_username)

        if show_groups:
             print('-'*10)
             for group in groups:
                 print(group)
             print('-'*10)

        print ('{} ({}) can {} UniWireless.'.format(
                student_username,
                student_id,
                'access' if access else 'not access'))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    search_ldap(auto_envvar_prefix='SITWIFI')

