# ------------------------------------------------------------------------
#
#  This file is part of the Chirp Connect Python SDK.
#  For full information on usage and licensing, see https://chirp.io/
#
#  Copyright (c) 2011-2018, Asio Ltd.
#  All rights reserved.
#
# ------------------------------------------------------------------------


class ConnectError(Exception):

    def __init__(self, message, code=None):
        Exception.__init__(self)
        self.message = message
        self.error_code = code

    def __str__(self):
        return self.message


class ConnectAudioError(Exception):

    pass


class ConnectNetworkError(Exception):

    pass
