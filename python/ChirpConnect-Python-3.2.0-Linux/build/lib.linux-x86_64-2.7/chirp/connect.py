# ------------------------------------------------------------------------
#
#  This file is part of the Chirp Connect Python SDK.
#  For full information on usage and licensing, see https://chirp.io/
#
#  Copyright (c) 2011-2018, Asio Ltd.
#  All rights reserved.
#
# ------------------------------------------------------------------------

from . import libconnect, __version__

from ctypes import (
    Structure, CFUNCTYPE, POINTER,
    c_char_p, c_uint8, c_uint32, c_uint64,
    c_short, c_float, c_void_p, c_bool, c_size_t
)
from datetime import datetime
from platform import architecture
from random import randrange

from .audio import Audio
from .exceptions import ConnectError
from .network import get_licence_data
from _connect import (
    new_chirp_connect,
    del_chirp_connect,
    chirp_connect_set_licence,
    chirp_connect_process_input,
    chirp_connect_process_output,
    chirp_connect_process_shorts_input,
    chirp_connect_process_shorts_output,
    CHIRP_CONNECT_STATE_STOPPED,
    CHIRP_CONNECT_STATE_PAUSED,
    CHIRP_CONNECT_STATE_RUNNING,
    CHIRP_CONNECT_STATE_SENDING,
    CHIRP_CONNECT_STATE_RECEIVING,
    CHIRP_CONNECT_STATE_NOT_CREATED,
)


CHIRP_CONNECT_STATE = {
    CHIRP_CONNECT_STATE_STOPPED: 'Stopped',
    CHIRP_CONNECT_STATE_PAUSED: 'Paused',
    CHIRP_CONNECT_STATE_RUNNING: 'Running',
    CHIRP_CONNECT_STATE_SENDING: 'Sending',
    CHIRP_CONNECT_STATE_RECEIVING: 'Receiving',
    CHIRP_CONNECT_STATE_NOT_CREATED: 'Not Created'
}

# ------------------------------------------------------------------------
# Callback function pointers
# ------------------------------------------------------------------------
ChirpConnectCallback = CFUNCTYPE(None, c_void_p, POINTER(c_uint8), c_size_t)
ChirpConnectStateCallback = CFUNCTYPE(None, c_void_p, c_uint8, c_uint8)


class ChirpPackage(Structure):
    _fields_ = [
        ("name", c_char_p),
        ("version", c_char_p),
        ("build", c_char_p)
    ]


class ChirpVersion(Structure):
    _fields_ = [
        ("connect", ChirpPackage),
        ("engine", ChirpPackage),
        ("crypto", ChirpPackage)
    ]


class ChirpConnectCallbackSet(Structure):
    _fields_ = [
        ("on_state_changed", ChirpConnectStateCallback),
        ("on_sending", ChirpConnectCallback),
        ("on_sent", ChirpConnectCallback),
        ("on_receiving", ChirpConnectCallback),
        ("on_received", ChirpConnectCallback)
    ]

    def __init__(self, sdk):
        self.sdk = sdk
        self.state_changed_fn = ChirpConnectStateCallback(self.state_changed)
        self.sending_fn = ChirpConnectCallback(self.sending)
        self.sent_fn = ChirpConnectCallback(self.sent)
        self.receiving_fn = ChirpConnectCallback(self.receiving)
        self.received_fn = ChirpConnectCallback(self.received)
        super(ChirpConnectCallbackSet, self).__init__(
            self.state_changed_fn, self.sending_fn, self.sent_fn,
            self.receiving_fn, self.received_fn
        )

    def state_changed(self, cid, old, new):
        self.sdk.callbacks.on_state_changed(old, new)

    def sending(self, cid, payload, length):
        self.sdk.callbacks.on_sending(_Payload(self.sdk, payload[:length]))

    def sent(self, cid, payload, length):
        self.sdk.callbacks.on_sent(_Payload(self.sdk, payload[:length]))

    def receiving(self, cid, payload, length):
        self.sdk.callbacks.on_receiving()

    def received(self, cid, payload, length):
        self.sdk.callbacks.on_received(_Payload(self.sdk, payload[:length]))


# ------------------------------------------------------------------------
# Symbol bindings: Utils
# ------------------------------------------------------------------------
libconnect.chirp_connect_get_version.restype = ChirpVersion
libconnect.chirp_connect_get_package_full_version.restype = c_char_p
libconnect.chirp_connect_get_package_name.restype = c_char_p
libconnect.chirp_connect_get_package_version.restype = c_char_p
libconnect.chirp_connect_get_package_build.restype = c_char_p
libconnect.chirp_connect_error_code_to_string.argtypes = [c_uint8]
libconnect.chirp_connect_error_code_to_string.restype = c_char_p
libconnect.chirp_connect_trigger_callbacks.argtypes = [c_void_p, POINTER(c_uint8), c_size_t]

# ------------------------------------------------------------------------
# Symbol bindings: Getters & Setters
# ------------------------------------------------------------------------
libconnect.chirp_connect_set_licence.argtypes = [c_void_p, c_char_p]
libconnect.chirp_connect_set_licence.restype = c_uint8
libconnect.chirp_connect_set_random_seed.argtypes = [c_void_p, c_uint32]
libconnect.chirp_connect_set_volume.argtypes = [c_void_p, c_float]
libconnect.chirp_connect_get_volume.argtypes = [c_void_p]
libconnect.chirp_connect_get_volume.restype = c_float
libconnect.chirp_connect_set_sample_rate.argtypes = [c_void_p, c_uint32]
libconnect.chirp_connect_set_sample_rate.restype = c_uint8
libconnect.chirp_connect_get_sample_rate.argtypes = [c_void_p]
libconnect.chirp_connect_get_sample_rate.restype = c_uint32
libconnect.chirp_connect_get_state.argtypes = [c_void_p]
libconnect.chirp_connect_get_state.restype = c_uint8
libconnect.chirp_connect_set_auto_mute.argtypes = [c_void_p, c_bool]
libconnect.chirp_connect_get_auto_mute.argtypes = [c_void_p]
libconnect.chirp_connect_get_auto_mute.restype = c_bool
libconnect.chirp_connect_get_protocol_name.argtypes = [c_void_p]
libconnect.chirp_connect_get_protocol_name.restype = c_char_p
libconnect.chirp_connect_get_duration_for_payload_length.argtypes = [c_void_p, c_size_t]
libconnect.chirp_connect_get_duration_for_payload_length.restype = c_float
libconnect.chirp_connect_get_protocol_version.argtypes = [c_void_p]
libconnect.chirp_connect_get_protocol_version.restype = c_uint8
libconnect.chirp_connect_get_expiry_time.argtypes = [c_void_p]
if architecture()[0] == '32bit':  # Determine size of time_t
    libconnect.chirp_connect_get_expiry_time.restype = c_uint32
else:
    libconnect.chirp_connect_get_expiry_time.restype = c_uint64

# ------------------------------------------------------------------------
# Symbol bindings: States
# ------------------------------------------------------------------------
libconnect.chirp_connect_start.argtypes = [c_void_p]
libconnect.chirp_connect_start.restype = c_uint8
libconnect.chirp_connect_pause.argtypes = [c_void_p, c_bool]
libconnect.chirp_connect_pause.restype = c_uint8
libconnect.chirp_connect_stop.argtypes = [c_void_p]
libconnect.chirp_connect_stop.restype = c_uint8

# ------------------------------------------------------------------------
# Symbol bindings: Callbacks
# ------------------------------------------------------------------------
libconnect.chirp_connect_set_callbacks.argtypes = [c_void_p, ChirpConnectCallbackSet]
libconnect.chirp_connect_set_callbacks.restype = c_uint8
libconnect.chirp_connect_set_callback_ptr.argtypes = [c_void_p, c_void_p]

# ------------------------------------------------------------------------
# Symbol bindings: Payload
# ------------------------------------------------------------------------
libconnect.chirp_connect_get_max_payload_length.argtypes = [c_void_p]
libconnect.chirp_connect_get_max_payload_length.restype = c_size_t
libconnect.chirp_connect_new_payload.argtypes = [c_void_p, c_size_t]
libconnect.chirp_connect_new_payload.restype = POINTER(c_uint8)
libconnect.chirp_connect_random_payload.argtypes = [c_void_p, c_size_t]
libconnect.chirp_connect_random_payload.restype = POINTER(c_uint8)
libconnect.chirp_connect_is_valid.argtypes = [c_void_p, POINTER(c_uint8), c_size_t]
libconnect.chirp_connect_is_valid.restype = c_uint8
libconnect.chirp_connect_as_string.argtypes = [c_void_p, POINTER(c_uint8), c_size_t]
libconnect.chirp_connect_as_string.restype = c_char_p
libconnect.chirp_connect_send.argtypes = [c_void_p, POINTER(c_uint8), c_size_t]
libconnect.chirp_connect_send.restype = c_uint8


class _Payload(bytearray):
    """
    A Chirp Payload.
    Subclass of built in type - bytearray.
    """
    def __init__(self, sdk, *args, **kwargs):
        self._sdk = sdk
        self.max_length = self._sdk.max_payload_length
        super(_Payload, self).__init__(*args, **kwargs)
        if len(self) > self.max_length:
            raise ValueError('Payload has a maximum length of {}'.format(self.max_length))

    def __str__(self):
        return self._sdk.as_string(self)

    def isvalid(self):
        return self._sdk.is_valid(self)

    def extend(self, data):
        self.max_length = self._sdk.max_payload_length
        if len(self) + len(data) > self.max_length:
            raise ValueError('Payload has a maximum length of {}'.format(self.max_length))
        super(_Payload, self).extend(data)


class CallbackSet(object):
    """
    An abstract class to implement callback methods.

    The ChirpConnectSDK will call these methods when it is
    changing state, or is sending/receiving data. To handle
    data transmission you should inherit this, and assign
    it to the `callbacks` attribute of the SDK after loading
    the licence.
    """
    def on_state_changed(self, old, new):
        """
        Called when the state of Chirp Library has changed.

        Args:
            old (str): Previous state
            new (str): Current state
        """
        pass

    def on_sending(self, payload):
        """
        Called when the Chirp Library has begun sending data.

        Args:
            payload (Payload): The Chirp Payload (bytearray)
        """
        pass

    def on_sent(self, payload):
        """
        Called when the Chirp Library has sent the whole payload.

        Args:
            payload (Payload): The Chirp Payload (bytearray)
        """
        pass

    def on_receiving(self):
        """
        Called when the Chirp Library hears the start of a payload.
        """
        pass

    def on_received(self, payload):
        """
        Called when the Chirp Library has decoded a full payload.
        Note: A length of 0 indicates a failed decode.

        Args:
            payload (Payload): The Chirp Payload (bytearray)
            length (int): The length of the payload
        """
        pass


class AudioSet(object):
    """
    An abstract class for overriding the default audio layer.

    The ChirpConnectSDK uses `sounddevice` to handle audio streams.
    If you need to provide your own audio layer then you should
    subclass this, and assign it to the `audio` attribute of
    the SDK before loading the licence.

    The Audio layer must provide methods to start/stop the
    input/output streams, and close the audio engine. These
    will be called by SDK appropriately.
    """
    def __init__(self, sdk):
        pass

    def start(self, send=True, receive=True):
        """
        Start the audio engine.

        Args:
            send (bool): Enable output audio
            receive (bool): Enable input audio
        """
        pass

    def stop(self):
        """
        Stop the audio engine.
        """
        pass

    def close(self):
        """
        Close the audio engine.
        """
        pass


class ChirpConnect(object):
    """
    The Chirp Connect SDK.

    This is the main wrapper around the Chirp Connect Library.
    It exposes methods to send arbitrary payloads, and receive
    decoded chirps from the audio layer. Received data is handled
    in callback methods using the `CallbackSet`.
    """
    def __init__(self, key, secret, licence=None, debug=False):
        """
        Instantiate the SDK with an application key, secret, and licence.
        These can be found at admin.chirp.io.

        You can set the SDK to run in debug mode by setting the flag true.
        This will write any input data from the microphone to a wav file
        called chirp_audio.wav.

        Args:
            key (str): Chirp application key
            secret (str): Chirp application secret
            licence (str): Path to licence file
            debug (bool): Enter debug mode
        """
        self.audio = None
        self.debug = debug
        self.key = key
        self.secret = secret
        self._sdk = new_chirp_connect(self.key, self.secret)
        self.callbacks = CallbackSet()
        self._callback_set = ChirpConnectCallbackSet(self)
        self._set_seed()
        self.load_licence(licence) if licence else self.get_licence()

    def __str__(self):
        """
        Convenience method to output Chirp Connect Library version information.

        Returns:
            dict: Version information for Chirp
                connect/engine/crypto libraries.
        """
        version = self.version['connect']
        return 'Chirp Connect {pyversion} [{cversion} {cbuild}] initialised.'.format(
            pyversion=__version__, cversion=version['version'], cbuild=version['build']
        )

    @property
    def version(self):
        """
        Get version information from the Chirp Connect Library.

        Returns:
            dict: Version information for Chirp
                connect/engine/crypto libraries.
        """
        v = libconnect.chirp_connect_get_version()
        return {
            'connect': {
                'name': v.connect.name.decode(),
                'version': v.connect.version.decode(),
                'build': v.connect.build.decode()
            },
            'engine': {
                'name': v.engine.name.decode(),
                'version': v.engine.version.decode(),
                'build': v.engine.build.decode()
            },
            'crypto': {
                'name': v.crypto.name.decode(),
                'version': v.crypto.version.decode(),
                'build': v.crypto.build.decode()
            }
        }

    def close(self):
        """
        Closes sounddevice streams and frees memory in the
        Chirp Connect Library.

        Raises:
            ConnectError: If an error occurs when freeing memory.
        """
        if self.audio:
            self.audio.close()
        if self._sdk:
            del_chirp_connect()

    def _call(self, fn, *args):
        """
        Internal method to make a call to C SDK functions that return
        an error code. If an error occurs, then get the associated
        error message and raise a ConnectError with it.

        Raises:
            ConnectError: If an error occurs.
        """
        rc = fn(*args)
        if rc != 0:
            err = libconnect.chirp_connect_error_code_to_string(rc)
            raise ConnectError(err.decode(), code=rc)

    # -- Getters & Setters

    def load_licence(self, filename):
        """
        Load a licence from file, and initialise the Chirp Connect Library.

        This must be done after immediately after instantiating the SDK.
        Unless you are implementing your own audio layer, then the audio
        attribute must be set first.

        Args:
            filename (str): The path to the licence file

        Raises:
            ConnectError: If the licence is invalid or there is an error
                setting the callbacks.
        """
        with open(filename, 'r') as licence:
            self.set_licence(licence.read())

    def set_licence(self, licence):
        """
        Initialise the Chirp Connect Library with a licence.

        This sets up the licence and the internal callback set.
        If using the default sounddevice audio layer, then this is instantiated here.

        Args:
            licence (str): Licence string

        Raises:
            ConnectError: If the licence is invalid or there is an error setting
                the callbacks.
        """
        if not self.audio:
            self.audio = Audio(self)
        try:
            chirp_connect_set_licence(licence)
        except UnicodeDecodeError:
            raise ValueError('This doesn\'t look like a valid licence')
        self._call(libconnect.chirp_connect_set_callbacks, self._sdk, self._callback_set)
        self._max_payload_length = self.max_payload_length

    def get_licence(self, name=None):
        """
        Retrieve a licence for your application, and initialise the
        Chirp Connect Library. If no licence name is specified, then
        the default licence is used.

        Args:
            name (str): Licence name, default is used if not set

        Raises:
            ConnectNetworkError: If the request to retrieve the licence fails.
            ConnectError: If the licence is invalid or there is an error setting
                the callbacks.
        """
        licence = get_licence_data(self.key, self.secret, name)
        if licence:
            self.set_licence(licence)

    def _set_seed(self, seed=None):
        """ Set the seed for the random generator """
        seed = randrange(2 ** 32 - 1) if seed is None else seed
        libconnect.chirp_connect_set_random_seed(self._sdk, seed)

    def set_callbacks(self, callbacks):
        """
        Set the callback set, used for consistency between platforms.

        Args:
            callbacks: (CallbackSet): Callback set

        Raises:
            ConnectError: If there is an error setting the callbacks.
        """
        self._call(libconnect.chirp_connect_set_callbacks, self._sdk, self._callback_set)
        self.callbacks = callbacks

    @property
    def volume(self):
        """
        float: Property to get/set the SDK volume.
        """
        return round(libconnect.chirp_connect_get_volume(self._sdk), 2)

    @volume.setter
    def volume(self, level):
        libconnect.chirp_connect_set_volume(self._sdk, float(level))

    @property
    def sample_rate(self):
        """
        int: Property to get/set the SDK sample rate.
        """
        rv = libconnect.chirp_connect_get_sample_rate(self._sdk)
        if rv == 0:
            raise ConnectError("Couldn't get sample rate (Connect not initialised?)")
        return rv

    @sample_rate.setter
    def sample_rate(self, rate):
        self._call(libconnect.chirp_connect_set_sample_rate, self._sdk, rate)

    @property
    def state(self):
        """
        str: Property to get the current state of the SDK.

        Returns either
            chirp.CHIRP_CONNECT_STATE_NOT_CREATED
            chirp.CHIRP_CONNECT_STATE_STOPPED
            chirp.CHIRP_CONNECT_STATE_PAUSED
            chirp.CHIRP_CONNECT_STATE_RUNNING
            chirp.CHIRP_CONNECT_STATE_SENDING
            chirp.CHIRP_CONNECT_STATE_RECEIVING
        """
        return libconnect.chirp_connect_get_state(self._sdk)

    @property
    def auto_mute(self):
        """
        bool: Property to get/set the auto mute function of the SDK.

        Auto-mute prevents the SDK from hearing its own chirps when
        it is sending data. This should be True in almost all cases.
        """
        return libconnect.chirp_connect_get_auto_mute(self._sdk)

    @auto_mute.setter
    def auto_mute(self, mute):
        libconnect.chirp_connect_set_auto_mute(self._sdk, bool(mute))

    @property
    def protocol_name(self):
        """
        str: Property to get the configured protocol name.
        """
        return libconnect.chirp_connect_get_protocol_name(self._sdk)

    @property
    def protocol_version(self):
        """
        int: Returns the current protocol version.
        """
        return libconnect.chirp_connect_get_protocol_version(self._sdk)

    @property
    def expiry(self):
        """
        datetime: Returns the expiry date of the current licence.
        """
        dt = libconnect.chirp_connect_get_expiry_time(self._sdk)
        return datetime.utcfromtimestamp(dt)

    def get_duration(self, length):
        """
        float: Returns the duration of a chirp of `length` bytes in seconds.
        """
        return round(libconnect.chirp_connect_get_duration_for_payload_length(self._sdk, length), 3)

    # -- States

    def start(self, send=True, receive=True):
        """
        Start the SDK running.

        The SDK can be configured to run in send mode, receive mode
        or both. The default is send and receive mode.
        This also calls the `start` method in the audio layer.

        Args:
            send (bool): Enable send mode
            receive (bool): Enable receive mode

        Raises:
            ConnectError: If there is an error starting the
                Chirp Connect Library.
        """
        self._call(libconnect.chirp_connect_start, self._sdk)
        if self.audio:
            self.audio.start(send, receive)

    def pause(self, state):
        """
        Pause the SDK and audio streams.

        Args:
            state (bool): True to pause, False to resume

        Raises:
            ConnectError: If there is an error pausing the
                Chirp Connect Library.
        """
        if self.audio:
            self.audio.stop() if state else self.audio.start()
        self._call(libconnect.chirp_connect_pause, self._sdk, bool(state))

    def stop(self):
        """
        Stop the SDK and audio streams.

        Raises:
            ConnectError: If there is an error stopping the
                Chirp Connect Library.
        """
        if self.audio:
            self.audio.stop()
        self._call(libconnect.chirp_connect_stop, self._sdk)

    # -- Callbacks

    def trigger_callbacks(self, payload):
        """
        Trigger the callback methods with a payload.

        Args:
            payload (bytearray): The data for the simulation.
        """
        data = (c_uint8 * len(payload))(*payload)
        libconnect.chirp_connect_trigger_callbacks(self._sdk, data, len(data))

    # -- Processing

    def process_input(self, input):
        """
        Process input data only. Used for receive only mode.

        An input array of floating-point audio samples should be passed in.
        The Chirp Connect Library will trigger the callback methods
        if any chirps are decoded. The input data must contain values
        ranging from -1 to +1, and must be sampled at the same rate as
        the SDK's sample_rate property.

        Args:
            input (:obj:`list` of :obj:`float`): The input audio data.

        Raises:
            ConnectError: If there is an error processing the data.
        """
        chirp_connect_process_input(input)

    def process_output(self, output):
        """
        Process output data only. Used for send only mode.

        An output array should be passed by reference.
        The Chirp Connect Library will populate the
        output buffer with any data to be sent.

        Args:
            output (:obj:`list` of :obj:`float`): The output buffer to be populated.

        Raises:
            ConnectError: If there is an error processing the data.
        """
        chirp_connect_process_output(output)

    def process_shorts_input(self, input):
        """
        Process input data only. Used for receive only mode.

        An input array of 16bit signed integer audio samples should be passed in.
        The Chirp Connect Library will trigger the callback methods
        if any chirps are decoded. The input data must contain values
        ranging from -32767 to +32767, and must be sampled at the same rate as
        the SDK's sample_rate property.

        Args:
            input (:obj:`list` of :obj:`int`): The input audio data.

        Raises:
            ConnectError: If there is an error processing the data.
        """
        chirp_connect_process_shorts_input(input)

    def process_shorts_output(self, output):
        """
        Process output data only. Used for send only mode.

        An output array should be passed by reference.
        The Chirp Connect Library will populate the
        output buffer with any data to be sent.

        Args:
            output (:obj:`list` of :obj:`int`): The output buffer to be populated.

        Raises:
            ConnectError: If there is an error processing the data.
        """
        chirp_connect_process_shorts_output(output)

    # -- Payload

    @property
    def max_payload_length(self):
        """
        int: Property to get the max payload length available with the configured licence.
        """
        return int(libconnect.chirp_connect_get_max_payload_length(self._sdk))

    def new_payload(self, data=None):
        """
        Generate an arbitrary Chirp Payload.
        A Chirp Payload is subclass of the built in type (bytearray).
        It will accept the same data types as a bytearray, ie. an integer,
        a string or an array of bytes.

        Args:
            data: The payload data

        Returns:
            payload (Payload): The Chirp Payload (bytearray)

        Raises:
            ValueError: If the data length is longer than the max payload length.
                This is set by the configured licence. Or if there is no data.
        """
        data = [] if data is None else data
        if len(data) == 0:
            raise ValueError('Cannot generate a null payload')
        return _Payload(self, data)

    def random_payload(self, length=None):
        """
        Generate a random Chirp Payload of `length` bytes
        If no length is specified, then a payload of a random
        length (up to the max_payload_length) is generated.

        Args:
            length: The required length of the payload (optional)

        Returns:
            Payload: A Chirp Payload containing random data (bytearray)

        Raises:
            ValueError: If a length of 0 is specified
        """
        length = randrange(1, self._max_payload_length) if length is None else length
        if length == 0:
            raise ValueError('Cannot generate a null payload')
        payload = libconnect.chirp_connect_random_payload(self._sdk, length)
        return _Payload(self, payload[:length])

    def is_valid(self, payload):
        """
        Check if a payload is valid.

        Args:
            payload (Payload): The Chirp Payload (bytearray)

        Returns:
            bool: True if valid.
        """
        data = (c_uint8 * len(payload))(*payload)
        rc = libconnect.chirp_connect_is_valid(self._sdk, data, len(data))
        return rc == 0

    def as_string(self, payload):
        """
        Returns the string representation of the Chirp Payload.

        Args:
            payload (Payload): The Chirp Payload (bytearray)

        Returns:
            str: The string representation of the Chirp Payload.
        """
        data = (c_uint8 * len(payload))(*payload)
        return str(libconnect.chirp_connect_as_string(self._sdk, data, len(payload)).decode())

    def send(self, payload):
        """
        Send a Chirp Payload.
        This will pass the payload data to the Chirp Connect Library, which will then be
        processed into the output buffer in the `process` functions.

        Args:
            payload (Payload): The Chirp Payload (bytearray)

        Raises:
            ConnectError: If there is an error sending the data.
        """
        data = (c_uint8 * len(payload))(*payload)
        self._call(libconnect.chirp_connect_send, self._sdk, data, len(data))
