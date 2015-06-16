#!/usr/bin/env python

from distutils.core import setup
from sys import hexversion,exit

if hexversion <= 0x03000000:
	print('Version 3.0 of Python required!')
	exit(-1)


setup(
	name='pyzfslib',
	version='0.1.0.0',
	description='Package for interfacing with zfs',
	author='Lasse Poulsen',
	author_email='llp@innocore.dk',
	url='https://github.com/innollp/pyzfslib/',
	packages=['pyzfslib'],
	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
		'Environment :: Plugins',
		'Intended Audience :: Developers',
		'Intended Audience :: System Administrators',
		'Operating System :: POSIX :: BSD',
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Software Development :: Libraries',
		'Topic :: System :: Filesystems',
	],
	
)

