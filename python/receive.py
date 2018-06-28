
import time
import sys
import binascii

from chirp import ChirpConnect, CallbackSet


class Callbacks(CallbackSet):
    def on_received(self, payload):
        sys.stdout.buffer.write(binascii.unhexlify(str(payload)))

sdk = ChirpConnect("bccBb28f9D13b5C7Ec5d6B5D2", "f48cfC1Ae8cada9dfe023b03fB6be7FB7988f69201b4BdBEEE")

callbacks = Callbacks()
sdk.set_callbacks(callbacks)
sdk.start(send=False, receive=True)

try:
        # Process audio streams
        while True:
            time.sleep(0.1)
            #sys.stdout.write('.')
            sys.stdout.flush()
except KeyboardInterrupt:
        print('Exiting')
sdk.stop()
sdk.close()