# Chirp Connect Python SDK

The Chirp Connect Python SDK makes it easy to send and receive data over sound on many different platforms, including

- macOS
- Raspberry Pi
- Linux

The latest stable version can be downloaded from the [Chirp Admin Centre](https://admin.chirp.io/downloads).

Compatible with all supported versions of Python 2 and 3. However for best performance it is recommended to use Python 3.


## Getting Started

**Step 1** - Install dependencies

For audio I/O, the SDK relies on the host having the [PortAudio](http://www.portaudio.com/) library installed.

### macOS

```shell
brew install python
brew install portaudio
```

### Debian/Ubuntu

```shell
sudo apt-get install python3-dev python3-setuptools
sudo apt-get install portaudio19-dev libffi-dev libsndfile1
```

### CentOS
``` shell
sudo yum install gcc python-devel python-setuptools
sudo yum install gcc alsa-lib-devel libffi-devel libsndfile
```

Note: PortAudio will need to be installed from source for CentOS platforms.


**Step 2** - Install SDK

Installing the SDK from source is as simple as

```shell
python setup.py install
```

Note: This may take a few minutes on some platforms.


## Documentation

To read the SDK docs, run

    pydoc chirp.ChirpConnect

    pydoc chirp.CallbackSet

    pydoc chirp.AudioSet


## Usage

```python

from chirp import ChirpConnect

sdk = ChirpConnect(app_key, app_secret)
payload = sdk.new_payload([0, 1, 2, 3])

sdk.start(send=True, receive=False)
sdk.send(payload)
```


See `example.py` for further usage instructions.


## Audio

The audio layer has several configurable options to suit your hardware requirements.
These must be configured after the SDK is instantiated but before the SDK is started.

Any changes to the audio configuration will only take effect if the SDK is not running.

The audio layer will use the default input/output device on the system. However you can
explicitly define which device to use. To check the available devices, run

    sdk.audio.query_devices()

To set a specific input/output device, instruct the SDK to use the device using the index.

    sdk.audio.input_device = 1
    sdk.audio.output_device = 2

The block size of the audio buffer can also be configured. A default of 4096 is used.

    sdk.audio.block_size = 1024

The SDK can process float32 or int16 samples. The SDK uses float32 by default but you can
configure with int16s by running

    sdk.audio.sample_size = 'int16'

The SDK can be instructed to output both mono/stereo data

    sdk.audio.output_channels = 2

The sample rate can also be updated from the default value.

    sdk.sample_rate = 48000



## Example

```
usage: example.py [-h] [-l L] [-i I] [-o O] [-f F] [-s S] key secret

Chirp Connect SDK Example

positional arguments:
  key         Chirp application key
  secret      Chirp application secret

optional arguments:
  -h, --help  show this help message and exit
  -l L        Path to licence file (optional)
  -i I        Input device index (optional)
  -o O        Output device index (optional)
  -b B        Block size (optional)
  -s S        Sample rate (optional)

Sends a random chirp payload, then continuously listens for chirps
```


## Payloads

A Chirp payload is inherited from the built in type - bytearray.
This means you can send data as a string or an iterable of integers.

    payload = sdk.new_payload([104, 101, 108, 108, 111])


## Debugging

To check the quality of the input data from your microphone, you can run the SDK in debug mode.
This will write the input audio data to a file called chirp_audio.wav. To do this, set the debug
flag to `True` when instantiating the SDK. You can also override the output path of the wav file.

```python

from chirp import ChirpConnect

sdk = ChirpConnect(app_key, app_secret, debug=True)
sdk.audio.wav_filename = '/path/to/wav'
sdk.start()
```


## Testing

    python setup.py test

To run the unit tests, you need to add an app_key, app_secret and licence_path to a config file named ~/.chirp, eg.,
Note: The licence file must use the Chirp standard protocol.

    [test]
    app_key = xxxxxxxxxxxxxxxxxxxxxxxxx
    app_secret = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    licence_path = /path/to/licence/file


## Advanced

The Chirp Connect SDK uses `sounddevice` by default, however you can override this if you want to implement your own audio layer.
This is achieved by subclassing the `AudioSet` class, then overriding the `audio` attribute before starting the SDK.

```python
from chirp import AudioSet, ChirpConnect

class Audio(AudioSet):
    """ Override start, stop, close methods """
    pass

sdk = ChirpConnect(key, secret)
sdk.audio = Audio(sdk)
sdk.start(send=True, receive=False)
payload = sdk.random_payload()
sdk.send(payload)
buffer = [0.0] * 4096
sdk.process_output(buffer)
```
