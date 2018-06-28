# ------------------------------------------------------------------------
#
#  This file is part of the Chirp Connect Python SDK.
#  For full information on usage and licensing, see http://chirp.io/
#
#  Copyright (c) 2011-2018, Asio Ltd.
#  All rights reserved.
#
# ------------------------------------------------------------------------

__title__ = 'chirp'
__version__ = '3.2.0'
__author__ = 'Asio Ltd.'
__license__ = 'Apache 2.0 for non-commercial use only, commercial licenses apply for commercial usage.'
__copyright__ = 'Copyright 2011-2018, Asio Ltd.'


from ctypes import CDLL, RTLD_GLOBAL
import ctypes.util
import os
import platform

# Explicitly load libgcc as ctypes on RPi doesn't dynamically link it.
gcc = CDLL(ctypes.util.find_library('gcc_s'), mode=RTLD_GLOBAL)

# ------------------------------------------------------------------------
# Locate the libchirp-connect-shared library in order of preference:
#  - the locally-stored library from the libraries subdirectory
#  - the system-wide installation
# To install, download the appropriate Chirp Connect library for your
# operating system and place in the PATH.
# If the library cannot be located, try setting the LD_LIBRARY_PATH
# environment variable.
# ------------------------------------------------------------------------
try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    library_path = os.path.join(
        dir_path, 'libraries',
        ('libchirp-connect-shared.dylib' if platform.system() == 'Darwin' else
         'libchirp-connect-shared.so'))
    libconnect = CDLL(library_path)
except OSError:
    library_path = ctypes.util.find_library('chirp-connect-shared')
    if not library_path:
        raise Exception("Couldn't find libchirp-connect-shared. Please install the Chirp C SDK.")
    libconnect = CDLL(library_path)

from .connect import *
from _connect import (
    CHIRP_CONNECT_STATE_STOPPED,
    CHIRP_CONNECT_STATE_PAUSED,
    CHIRP_CONNECT_STATE_RUNNING,
    CHIRP_CONNECT_STATE_SENDING,
    CHIRP_CONNECT_STATE_RECEIVING,
    CHIRP_CONNECT_STATE_NOT_CREATED,
    CHIRP_CONNECT_BUFFER_SIZE
)
from .exceptions import *
