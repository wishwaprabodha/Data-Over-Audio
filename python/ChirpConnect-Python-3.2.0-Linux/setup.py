#!/usr/bin/env python

# ------------------------------------------------------------------------
#
#  This file is part of the Chirp Connect Python SDK.
#  For full information on usage and licensing, see http://chirp.io/
#
#  Copyright (c) 2011-2018, Asio Ltd.
#  All rights reserved.
#
# ------------------------------------------------------------------------

import re
from setuptools import setup, Extension

vstr = open('chirp/__init__.py', 'r').read()
regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
version = re.search(regex, vstr, re.M)

connect = Extension('_connect',
                    sources=['chirp/_connect.c'],
                    include_dirs=['./chirp', './chirp/include'],
                    library_dirs=['./chirp/libraries', '/usr/local/lib'],
                    runtime_library_dirs=['$ORIGIN/chirp/libraries', '/usr/local/lib'],
                    libraries=['chirp-connect-shared'])

setup(
    name='chirp',
    version=version.group(1),
    description='Chirp Connect Python SDK',
    long_description='The Chirp Connect Python SDK enables the user to create, '
                     'send and query chirps, using the Chirp audio protocol.',
    license='License :: Other/Proprietary License',
    author='Asio Ltd.',
    author_email='developers@chirp.io',
    url='http://developers.chirp.io',
    packages=['chirp', 'tests', 'bin'],
    ext_modules=[connect],
    install_requires=['sounddevice>=0.3.10', 'pysoundfile>=0.9.0', 'requests>=2.18.1'],
    include_package_data=True,
    tests_require=['configparser'],
    keywords=('sound', 'networking', 'chirp'),
    test_suite='tests',
    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Communications',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers'
    ],
)
