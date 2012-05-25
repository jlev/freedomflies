"""
 py2app/py2exe build script for Freedom Flies.

 Will automatically ensure that all build prerequisites are available
 via ez_setup

 Usage: python setup.py
"""

#import ez_setup
#ez_setup.use_setuptools()

import sys
from setuptools import setup

NAME='Freedom Flies'
VERSION='0.1'
mainscript = 'main.py'
data_files = ['images/icon.icns']

if sys.platform == 'darwin':
	plist = dict(
		CFBundleIconFile='icon.icns',
		CFBundleName=NAME,
		CFBundleShortVersionString=VERSION,
		CFBundleGetInfoString=' '.join([NAME, VERSION]),
		CFBundleExecutable=NAME,
		CFBundleIdentifier='edu.mit.compcult.freedomflies',
	)
	
	extra_options = dict(
		setup_requires=['py2app'],
		app=[mainscript],
		options=dict(py2app=dict(argv_emulation=True,
			iconfile='images/icon.icns',
			plist=plist,
			semi_standalone=False,
			site_packages=True)
		),
		data_files=data_files,
		script_args=("py2app",)
	)
	
	
elif sys.platform == 'win32':
	extra_options = dict(
		setup_requires=['py2exe'],
		app=[mainscript],
		data_files=[data_files],
		script_args=("py2exe",)
	)
	
	
else:
	extra_options = dict(
		# Normally unix-like platforms will use "setup.py install"
		# and install the main script as such
		scripts=[mainscript],
		data_files=[data_files]
	)

setup(
	name=NAME,
	**extra_options
)