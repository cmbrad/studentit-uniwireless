#!/usr/bin/env python

from setuptools import setup, find_packages
print(find_packages(exclude=['tests*']))

setup(
	name='sit-wifi',
	version='0.0.1',
	description='StudentIT WiFi checker',
	author='Christopher Bradley',
	author_email='chris.bradley@unimelb.edu.au',
	packages=find_packages(exclude=['tests*']),
	entry_points={
		'console_scripts': [
			'sit-wifi=bin.cli:search_ldap',
		],
	},
)
