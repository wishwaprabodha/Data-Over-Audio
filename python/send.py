
import time
import sys

from chirp import ChirpConnect

sdk = ChirpConnect("bccBb28f9D13b5C7Ec5d6B5D2", "f48cfC1Ae8cada9dfe023b03fB6be7FB7988f69201b4BdBEEE")
sdk.start(send=True, receive=False)
my_str = input()
my_str_as_bytes = str.encode(my_str)

payload = sdk.new_payload(my_str_as_bytes)
sdk.send(payload)

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

