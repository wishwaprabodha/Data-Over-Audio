# ------------------------------------------------------------------------
#
#  This file is part of the Chirp Connect Python SDK.
#  For full information on usage and licensing, see https://chirp.io/
#
#  Copyright (c) 2011-2018, Asio Ltd.
#  All rights reserved.
#
# ------------------------------------------------------------------------

import argparse
import sys
import time

from chirp import ChirpConnect, CallbackSet, CHIRP_CONNECT_STATE


class MyCallbacks(CallbackSet):

    def on_state_changed(self, previous_state, current_state):
        """ Called when the SDK's state has changed """
        print("State changed from {} to {}".format(
            CHIRP_CONNECT_STATE.get(previous_state),
            CHIRP_CONNECT_STATE.get(current_state)))

    def on_sending(self, payload):
        """ Called when a chirp has started to be transmitted """
        print('Sending: ' + str(payload))

    def on_sent(self, payload):
        """ Called when the entire chirp has been sent """
        print('Sent data')

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
            print('Received:' + str(payload))


def main(app_key, app_secret, licence_file,
         input_device, output_device,
         block_size, sample_rate):

    # Initialise ConnectSDK
    sdk = ChirpConnect(app_key, app_secret, licence_file)
    print(str(sdk))
    print(sdk.audio.query_devices())

    # Configure audio
    sdk.audio.input_device = input_device
    sdk.audio.output_device = output_device
    sdk.audio.block_size = block_size
    sdk.sample_rate = sample_rate

    # Set callback functions
    sdk.set_callbacks(MyCallbacks())

    # Generate random payload and send
    payload = sdk.random_payload()
    sdk.start(send=True, receive=True)
    sdk.send(payload)

    try:
        # Process audio streams
        while True:
            time.sleep(0.1)
            sys.stdout.write('.')
            sys.stdout.flush()
    except KeyboardInterrupt:
        print('Exiting')

    sdk.stop()
    sdk.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Chirp Connect SDK Example',
        epilog='Sends a random chirp payload, then continuously listens for chirps'
    )
    parser.add_argument('key', help='Chirp application key')
    parser.add_argument('secret', help='Chirp application secret')
    parser.add_argument('-l', help='Path to licence file (optional)')
    parser.add_argument('-i', type=int, default=None, help='Input device index (optional)')
    parser.add_argument('-o', type=int, default=None, help='Output device index (optional)')
    parser.add_argument('-b', type=int, default=0, help='Block size (optional)')
    parser.add_argument('-s', type=int, default=44100, help='Sample rate (optional)')
    args = parser.parse_args()

    main(args.key, args.secret, args.l, args.i, args.o, args.b, args.s)
