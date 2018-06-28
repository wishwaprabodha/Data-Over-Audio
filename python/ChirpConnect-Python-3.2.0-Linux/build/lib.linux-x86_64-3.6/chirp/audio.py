# ------------------------------------------------------------------------
#
#  This file is part of the Chirp Connect Python SDK.
#  For full information on usage and licensing, see https://chirp.io/
#
#  Copyright (c) 2011-2018, Asio Ltd.
#  All rights reserved.
#
# ------------------------------------------------------------------------

import platform
import time
import threading

try:
    from multiprocessing import SimpleQueue
except ImportError:  # python2
    from multiprocessing.queues import SimpleQueue

import sounddevice as sd

from .exceptions import ConnectAudioError


class Audio(object):
    """
    Chirp Connect Audio I/O
    """
    def __init__(self, sdk):
        self.sdk = sdk
        self.processing = None
        self.input_stream = None
        self.output_stream = None

        self.output_channels = 1
        self.wav_filename = None
        self.sample_size = 'float32'
        self.block_size = 4096 if platform.system() == 'Linux' else 0

        if self.sample_size == 'float32':
            self.sample_format = 'f'
            self.process_input_fn = self.sdk.process_input
            self.process_output_fn = self.sdk.process_output
        elif self.sample_size == 'int16':
            self.sample_format = 'h'
            self.process_input_fn = self.sdk.process_shorts_input
            self.process_output_fn = self.sdk.process_shorts_output
        else:
            raise ConnectAudioError(
                'Invalid audio format: %s. Only float32 and int16 are supported' %
                self.sample_size)

    def start(self, send=True, receive=True):
        """ Start audio I/O stream and processing thread """
        if receive:
            sd.check_input_settings(
                device=self.input_device, channels=1,
                dtype=self.sample_size, samplerate=self.sdk.sample_rate
            )
            self.processing = AudioProcessingThread(parent=self)
            self.input_stream = sd.RawInputStream(
                device=self.input_device,
                channels=1,
                samplerate=int(self.sdk.sample_rate),
                dtype=self.sample_size,
                blocksize=self.block_size,
                callback=self.process_input
            )
            self.input_stream.start()
        if send:
            sd.check_output_settings(
                device=self.output_device, channels=self.output_channels,
                dtype=self.sample_size, samplerate=self.sdk.sample_rate
            )
            self.output_stream = sd.RawOutputStream(
                device=self.output_device,
                channels=self.output_channels,
                samplerate=int(self.sdk.sample_rate),
                dtype=self.sample_size,
                blocksize=self.block_size,
                callback=self.process_output
            )
            self.output_stream.start()

    def stop(self):
        if self.processing:
            self.processing.stop()
        if self.input_stream:
            self.input_stream.stop()
        if self.output_stream:
            self.output_stream.stop()

    def process_input(self, indata, frames, time, status):
        """ Process input audio data - receive only audio callback """
        self.processing.block_size = frames
        self.processing.input_queue.put(bytes(indata))

    def process_output(self, outdata, frames, time, status):
        """ Process output audio data - send only audio callback """
        self.process_output_fn(outdata)

    def query_devices(self):
        """ Return info about available devices """
        return sd.query_devices()

    @property
    def input_device(self):
        return sd.default.device[0]

    @input_device.setter
    def input_device(self, index):
        sd.default.device[0] = index

    @property
    def output_device(self):
        return sd.default.device[1]

    @output_device.setter
    def output_device(self, index):
        sd.default.device[1] = index

    def close(self):
        """ Close I/O streams """
        if self.input_stream:
            self.input_stream.close()
        if self.output_stream:
            self.output_stream.close()


class AudioProcessingThread(threading.Thread):
    """
    Chirp Connect audio processing thread
    """
    DEBUG_AUDIO_FILENAME = 'chirp_audio.wav'

    def __init__(self, parent=None, *args, **kwargs):
        """
        Initialise audio processing.
        In debug mode, the audio data is saved to file.
        """
        self.sdk = parent.sdk
        self.sample_size = parent.sample_size
        self.block_size = parent.block_size
        self.sample_format = parent.sample_format
        self.process_input_fn = parent.process_input_fn
        self.sample_rate = float(parent.sdk.sample_rate)

        self.block_period = self.block_size / self.sample_rate or 0.1
        self.wav_filename = parent.wav_filename or self.DEBUG_AUDIO_FILENAME
        self.input_queue = SimpleQueue()
        super(AudioProcessingThread, self).__init__(*args, **kwargs)

        if self.sdk.debug:
            import soundfile as sf
            self.wav_file = sf.SoundFile(
                self.wav_filename, mode='w', channels=1,
                samplerate=self.sdk.sample_rate)

        self.daemon = True
        self.start()

    def run(self):
        """
        Continuously process any input data from circular buffer.
        Note: We need to sleep as much as possible in this thread
        to restrict CPU usage.
        """
        while self.is_alive():

            tstart = time.time()
            while not self.input_queue.empty():
                data = self.input_queue.get()
                self.process_input_fn(data)
                if self.sdk.debug and not self.wav_file.closed:
                    self.wav_file.buffer_write(data, dtype=self.sample_size)
                self.block_period = self.block_size / self.sample_rate

            tsleep = (self.block_period - ((time.time() - tstart)))
            if tsleep > 0:
                time.sleep(tsleep)

    def stop(self):
        """ In debug mode, close wav file """
        if self.sdk.debug:
            self.wav_file.close()
