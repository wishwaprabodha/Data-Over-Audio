#!/usr/bin/env python

#------------------------------------------------------------------------
#
#  This file is part of the Chirp Connect Python SDK.
#  For full information on usage and licensing, see https://chirp.io/
#
#  Copyright (c) 2011-2018, Asio Ltd.
#  All rights reserved.
#
#------------------------------------------------------------------------

import argparse

import soundfile as sf
from chirp import ChirpConnect, CallbackSet, CHIRP_CONNECT_STATE, CHIRP_CONNECT_BUFFER_SIZE


class Callbacks(CallbackSet):

    def __init__(self, ascii=False):
        self.ascii = ascii

    def on_receiving(self):
        """ Called when a chirp frontdoor is detected """
        print('Receiving data')

    def on_received(self, payload):
        """
        Called when an entire chirp has been received.
        Note: A length of 0 indicates a failed decode.
        """
        if len(payload) == 0:
            print('Decode failed!')
        else:
            if self.ascii:
                data = ''.join(chr(c) for c in payload)
                print('Received ' + data)
            else:
                print('Received: ' + str(payload))


def main(args):
    # Initialise the Chirp Connect SDK
    sdk = ChirpConnect(args.app_key, args.app_secret, args.app_licence)
    print(str(sdk))

    # Disable audio playback
    sdk.audio = None
    sdk.set_callbacks(Callbacks(args.ascii))
    sdk.start(send=False, receive=True)

    data, samplerate = sf.read(args.input_file, dtype='float32')
    for f in range(0, len(data), CHIRP_CONNECT_BUFFER_SIZE):
        sdk.process_input(list(data[f:f + CHIRP_CONNECT_BUFFER_SIZE]))

    # C SDK currently doesn't flush after the final frame
    sdk.process_input([0.0] * CHIRP_CONNECT_BUFFER_SIZE)

    sdk.stop()
    sdk.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Chirp Connect Audio Reader',
        epilog='Reads a .wav file containing Chirp Connect audio payloads, and outputs any payloads found'
    )
    parser.add_argument('app_key', help='Chirp Connect application key')
    parser.add_argument('app_secret', help='Chirp Connect application secret')
    parser.add_argument('app_licence', help='Chirp Connect application licence', nargs='?')
    parser.add_argument('-i', '--input_file', help='Input file')
    parser.add_argument('-A', '--ascii', action='store_true', help='Parse payloads as ASCII')
    args = parser.parse_args()

    main(args)
