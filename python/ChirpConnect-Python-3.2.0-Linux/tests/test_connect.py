"""
To run tests:
    python -m tests.test_connect
"""
import array as ar
import configparser
from datetime import datetime
import os
import sys
import unittest

from _connect import ConnectError as _ConnectError
from chirp import (
    CHIRP_CONNECT_STATE_STOPPED,
    CHIRP_CONNECT_STATE_PAUSED,
    CHIRP_CONNECT_STATE_RUNNING,
    CHIRP_CONNECT_STATE_SENDING,
    CHIRP_CONNECT_STATE_RECEIVING,
    CHIRP_CONNECT_STATE_NOT_CREATED,
    AudioSet, ChirpConnect, ConnectError
)


class TestConnectSDK(unittest.TestCase):
    BUFFER_SIZE = 1024
    TEST_PAYLOAD_LENGTH = 3

    def setUp(self):
        config = configparser.ConfigParser()
        config.read(os.path.expanduser('~/.chirp/config'))

        try:
            self.app_key = config.get('test', 'app_key')
            self.app_secret = config.get('test', 'app_secret')
            self.licence_path = config.get('test', 'licence_path')
            self.licence_path = os.path.expanduser(self.licence_path)
        except configparser.NoSectionError:
            raise Exception("Couldn't find test credentials. Please add a [test] section to your ~/.chirp/config.")

        self.sdk = ChirpConnect(self.app_key, self.app_secret, self.licence_path)
        self.sdk.audio = AudioSet(self.sdk)
        self.is2 = sys.version[0] == '2'

    def tearDown(self):
        self.sdk.audio.stop()
        self.sdk.audio.close()
        del self.sdk

    def test_version(self):
        version = self.sdk.version
        for module in ['connect', 'engine', 'crypto']:
            self.assertIn(module, version)
            for data in ['name', 'version', 'build']:
                self.assertIn(data, version[module])
                self.assertTrue(len(version[module][data]) > 0)

    # -- Getters & Setters

    def test_volume(self):
        self.assertEqual(self.sdk.volume, 1.0)

    def test_set_volume(self):
        self.sdk.volume = 0.33
        self.assertEqual(self.sdk.volume, 0.33)

    def test_sample_rate(self):
        self.assertEqual(self.sdk.sample_rate, 44100)

    def test_set_sample_rate(self):
        self.sdk.sample_rate = 48000
        self.assertEqual(self.sdk.sample_rate, 48000)
        with self.assertRaises(ConnectError):
            self.sdk.sample_rate = 0

    def test_default_state(self):
        self.assertEqual(self.sdk.state, CHIRP_CONNECT_STATE_STOPPED)

    def test_get_auto_mute(self):
        self.assertTrue(self.sdk.auto_mute)

    def test_set_auto_mute(self):
        self.sdk.auto_mute = True
        self.assertTrue(self.sdk.auto_mute)

    def test_protocol_name(self):
        self.assertEqual(self.sdk.protocol_name.decode(), 'standard')

    def test_protocol_version(self):
        self.assertIsInstance(self.sdk.protocol_version, int)

    def test_protocol_duration(self):
        self.assertEqual(self.sdk.get_duration(10), 2.04)

    def test_expiry(self):
        self.assertIsInstance(self.sdk.expiry, datetime)

    # -- States

    def test_not_created(self):
        with self.assertRaises(IOError):
            sdk = ChirpConnect(self.app_key, self.app_secret, '/not/real/path')
            self.assertEqual(sdk.state, CHIRP_CONNECT_STATE_NOT_CREATED)

    def test_start(self):
        self.sdk.start()
        self.assertEqual(self.sdk.state, CHIRP_CONNECT_STATE_RUNNING)

    def test_already_started(self):
        self.sdk.start()
        with self.assertRaises(ConnectError):
            self.sdk.start()

    def test_pause(self):
        self.sdk.start()
        self.sdk.pause(True)
        self.assertEqual(self.sdk.state, CHIRP_CONNECT_STATE_PAUSED)

    def test_unpause(self):
        self.sdk.start()
        self.sdk.pause(True)
        self.sdk.pause(False)
        self.assertEqual(self.sdk.state, CHIRP_CONNECT_STATE_RUNNING)

    def test_already_paused(self):
        with self.assertRaises(ConnectError):
            self.sdk.pause(True)

    def test_stop(self):
        self.sdk.start()
        self.sdk.stop()
        self.assertEqual(self.sdk.state, CHIRP_CONNECT_STATE_STOPPED)

    def test_already_stopped(self):
        with self.assertRaises(ConnectError):
            self.sdk.stop()

    # -- Callbacks

    def stub_connect_state_callback(self, old, new):
        self.old = old
        self.new = new

    def stub_connect_callback(self, payload):
        self.length = len(payload)

    def stub_receiving_callback(self):
        self.recv = True

    def test_state_changed_callback(self):
        self.sdk.callbacks.on_state_changed = self.stub_connect_state_callback
        self.sdk.trigger_callbacks([0, 1, 2, 3, 4])
        self.assertIsNotNone(self.old)
        self.assertIsNotNone(self.new)

    def test_sending_callback(self):
        self.sdk.callbacks.on_sending = self.stub_connect_callback
        self.sdk.trigger_callbacks([0, 1, 2, 3, 4])
        self.assertIsNotNone(self.length)

    def test_sent_callback(self):
        self.sdk.callbacks.on_sent = self.stub_connect_callback
        self.sdk.trigger_callbacks([0, 1, 2, 3, 4])
        self.assertIsNotNone(self.length)

    def test_receiving_callback(self):
        self.sdk.callbacks.on_receiving = self.stub_receiving_callback
        self.sdk.trigger_callbacks([0, 1, 2, 3, 4])
        self.assertTrue(self.recv)

    def test_received_callback(self):
        self.sdk.callbacks.on_received = self.stub_connect_callback
        self.sdk.trigger_callbacks([0, 1, 2, 3, 4])
        self.assertIsNotNone(self.length)

    # -- Processing

    def test_process_input(self):
        indata = ar.array('f', [0.025] * self.BUFFER_SIZE)
        self.sdk.start()
        self.sdk.process_input(getattr(indata, 'tostring' if self.is2 else 'tobytes')())

    def test_process_input_not_started(self):
        indata = ar.array('f', [0.025] * self.BUFFER_SIZE)
        with self.assertRaises(_ConnectError):
            self.sdk.process_input(getattr(indata, 'tostring' if self.is2 else 'tobytes')())

    def test_process_output(self):
        outdata = ar.array('f', [0.05] * self.BUFFER_SIZE)
        self.sdk.start()
        self.sdk.process_output(getattr(outdata, 'tostring' if self.is2 else 'tobytes')())

    def test_process_output_not_started(self):
        outdata = ar.array('f', [0.05] * self.BUFFER_SIZE)
        with self.assertRaises(_ConnectError):
            self.sdk.process_output(getattr(outdata, 'tostring' if self.is2 else 'tobytes')())

    def test_process_shorts_input(self):
        indata = ar.array('h', [128] * self.BUFFER_SIZE)
        self.sdk.start()
        self.sdk.process_shorts_input(getattr(indata, 'tostring' if self.is2 else 'tobytes')())

    def test_process_shorts_output(self):
        outdata = ar.array('h', [-128] * self.BUFFER_SIZE)
        self.sdk.start()
        self.sdk.process_shorts_output(getattr(outdata, 'tostring' if self.is2 else 'tobytes')())

    # -- Payload

    def test_get_max_payload_length(self):
        self.assertIsInstance(self.sdk.max_payload_length, int)
        self.assertTrue(self.sdk.max_payload_length > 0)

    def test_new_payload_string(self):
        payload = self.sdk.new_payload('test'.encode())
        self.assertIsInstance(payload, bytearray)

    def test_new_payload_array(self):
        payload = self.sdk.new_payload([64, 27, 33, 27])
        self.assertIsInstance(payload, bytearray)

    def test_random_payload(self):
        payload = self.sdk.random_payload(self.TEST_PAYLOAD_LENGTH)
        self.assertIsInstance(payload, bytearray)
        for byte in range(0, len(payload)):
            self.assertIsInstance(payload[byte], int)

    def test_is_valid(self):
        payload = self.sdk.random_payload(self.TEST_PAYLOAD_LENGTH)
        self.assertTrue(self.sdk.is_valid(payload))

    def test_payload_is_valid(self):
        payload = self.sdk.random_payload(self.TEST_PAYLOAD_LENGTH)
        self.assertTrue(payload.isvalid())

    def test_as_string(self):
        payload = self.sdk.random_payload(self.TEST_PAYLOAD_LENGTH)
        self.assertIsInstance(self.sdk.as_string(payload), str)

    def test_payload_as_string(self):
        payload = self.sdk.random_payload(self.TEST_PAYLOAD_LENGTH)
        self.assertIsInstance(str(payload), str)

    def test_send(self):
        self.sdk.start()
        payload = self.sdk.random_payload(self.TEST_PAYLOAD_LENGTH)
        self.assertIsNone(self.sdk.send(payload))

    def test_null_payload(self):
        with self.assertRaises(ValueError):
            self.sdk.random_payload(0)

    def test_payload_too_long(self):
        payload = self.sdk.new_payload('hello'.encode('ascii'))
        with self.assertRaises(ValueError):
            payload.extend('this-is-wayyyyy-toooooo-long')


if __name__ == '__main__':
    unittest.main()
