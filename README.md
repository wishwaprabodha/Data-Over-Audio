# chirp-test
Data-over-Sound POC on python and android

## Python Module

### Steps

For audio I/O, the SDK relies on the host having the PortAudio library installed.

1. install dependencies for python libraries using the proper linux distribution

Debian/Ubuntu
```
sudo apt-get install python3-dev python3-setuptools portaudio19-dev libffi-dev libsndfile1
```
CentOS

```
sudo yum install python3-dev python3-setuptools portaudio19-dev libffi-dev libsndfile1
```
2. install SDK (In the SDK file)

```
python setup.py install
```

* [Click Here for additional configuration details](https://developers.chirp.io/connect/getting-started/python/)

3. Enter API key and Secret

in send.py & receive.py file I have entered my trial edition credentials and those will expire in month. 
To get your credentails log into [Chirp](https://www.chirp.io) and register.

## Android Module

### Steps

* Simply go to the demo app and open the project using Andriod Studio and build the project.
* Change the API key & Secret for your credentials.
* Please refer the [Original guide](https://developers.chirp.io/connect/transition-guides/android/) for any further clarification.

## Enjoy!
