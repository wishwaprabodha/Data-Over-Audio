#!/usr/bin/env python

#------------------------------------------------------------------------
#
#  chirp-play.py: Play chirps via the system's default audio output.
#
#  This file is part of the Chirp Python SDK.
#  For full information on usage and licensing, see http://chirp.io/
#
#  Copyright (c) 2011-2018, Asio Ltd.
#  All rights reserved.
#
#------------------------------------------------------------------------

import time
import argparse

from chirp import ChirpConnect, CallbackSet, CHIRP_CONNECT_STATE_RUNNING

def main(args):
    #------------------------------------------------------------------------
    # Initialise the Connect SDK.
    #------------------------------------------------------------------------
    sdk = ChirpConnect(args.app_key, args.app_secret, args.app_licence)
    print(str(sdk))

    #------------------------------------------------------------------------
    # Generate random payload and send.
    #------------------------------------------------------------------------
    if args.ascii:
        message = args.ascii.encode("utf-8")
        payload = sdk.new_payload(message)
    elif args.hex:
        message = bytearray.fromhex(args.hex)
        payload = sdk.new_payload(message)
    else:
        payload = sdk.random_payload()

    sdk.volume = args.volume
    sdk.start(send=True, receive=False)
    sdk.send(payload)

    while sdk.state != CHIRP_CONNECT_STATE_RUNNING:
        time.sleep(0.1)

if __name__ == '__main__':
    #------------------------------------------------------------------------
    # Parse command-line argumentss.
    #------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description="Play chirps via the system's default audio output"
    )
    parser.add_argument('app_key', help='Chirp application key')
    parser.add_argument('app_secret', help='Chirp application secret')
    parser.add_argument('app_licence', help='Path to application licence file', nargs='?')
    parser.add_argument('-v', '--volume', help='Volume', default=1.0)
    parser.add_argument('-A', '--ascii', type=str, help='ASCII string used to generate payload')
    parser.add_argument('-H', '--hex', type=str, help='Hex string used to generate payload')
    args = parser.parse_args()

    main(args)
