# Transition guide for Chirp Connect SDK v3.3.4 from Android SDK v2.5.2

## Overall changes
* The SDK can now work completely offline if you have a licence file.
* Chirp with associated data has been removed and is no longer available.
* The Chirp is now called a payload and it is represented by a `byte[]` array which can have a dynamic length with a maximum length defined by your protocol.



## Changes in SDK code
* All old dependencies were removed and a new dependency `com.squareup.okhttp3:okhttp:3.9.0` was added.
``` java
compile 'io.chirp.connect:chirp-connect:3.3.4-release@aar'
compile 'com.squareup.okhttp3:okhttp:3.9.0'
```



* Package imports are updated. New minimal dependencies required look like this:
``` java
import io.chirp.connect.ChirpConnect;
import io.chirp.connect.interfaces.ConnectEventListener;
import io.chirp.connect.interfaces.ConnectAuthenticationStateListener;
import io.chirp.connect.models.ChirpError;
import io.chirp.connect.models.ConnectState;
```



* SDK initialisation has been change as well. 


```java
chirpConnect = new ChirpConnect(this, APP_KEY, APP_SECRET);
```

Licence was introduced in new SDK wich contains the protocol information.  Use the following to set the licence.

```java
ChirpError setLicenceError = chirpConnect.setLicence(LICENCE);
if (setLicenceError.getCode() > 0) {
    Log.e("ChirpError:", setLicenceError.getMessage());
}
```

Or you can use the dynamic licence loading  if you want to be able to control the licence from the Admin Centre.

```java
chirpConnect.getLicence(new ConnectLicenceListener() {

    @Override
    public void onSuccess(String networkLicence) {
        Log.d("getLicence", "onSuccess");
        ChirpError setLicenceError = chirpConnect.setLicence(networkLicence);
        if (setLicenceError.getCode() > 0) {
            Log.e("ChirpError:", setLicenceError.getMessage());
        }
    }

    @Override
    public void onError(ChirpError chirpError) {
        Log.e("getLicence", chirpError.getMessage());
    }
});
```



* The callback interface has changed as well. The interface is now called `ConnectEventListener` and have the following implementation:

```java
chirpConnect.setListener(new ConnectEventListener() {

  @Override
  public void onSent(byte[] payload) {
    Log.v("chirpConnectDemoApp", "This is called when a payload has been sent " + payload);
  }

  @Override
  public void onSending(byte[] payload) {
    Log.v("chirpConnectDemoApp", "This is called when a payload is being sent " + payload);
  }

  @Override
  public void onReceived(byte[] payload) {
    Log.v("chirpConnectDemoApp", "This is called when a payload has been received " + payload);
  }

  @Override
  public void onReceiving() {
    Log.v("chirpConnectDemoApp", "This is called when the SDK is expecting a payload to be received");
  }

  @Override
  public void onStateChanged(byte oldState, byte newState) {
    Log.v("chirpConnectDemoApp", "This is called when the SDK state has changed " + oldState + " -> " + newState);
  }

  @Override
  public void onSystemVolumeChanged(int old, int current) {
    Log.d("chirpConnectDemoApp", "This is called when the Android system volume has changed " + old + " -> " + current);
  }

});
```



* To start and stop audio processing loop you should call the same `.start()` and `.stop()` method except now it needs to be called on the new `chirpConnect` instance.
```java
chirpConnect.start();    //to start audio processing
chirpConnect.stop();    //to stop audio processing
```



* The `.chirp()` method that sends the data is now called `.send()` and you have to pass a byte array instead of a string. The size of the payload can be dynamic which will make your chirp shorter for smaller payloads however there is a maximum size that you can send and it is defined by your licence. The maximum payload length is returned by the `.getMaxPayloadLength()` method.
```java
long maxLength = chirpConnect.getMaxPayloadLength();
byte[] payload = chirpConnect.randomPayload(maxLength);
chirpConnect.send(payload);
```

For convenience here are two functions that converts a string to byte-array and a byte-array to string.

```java
public static byte[] stringToByteArray(String s) {
	return s.getBytes(StandardCharsets.US_ASCII);
}
```
```java
public static String bytesToString(byte[] byteArray) {
    return new String(byteArray, StandardCharsets.US_ASCII)
}
```

* Create a chirp with JSON data is not longer available in the SDK. Alternatively, if you need to map a payload to a JSON Object you can use a cloud service such as Firebase. See [firebase.google.com](https://firebase.google.com/) for more details.




## License
This software is copyright © 2011-2018, Asio Ltd.
All rights reserved.

This software is strictly confidential and not to be redistributed in its entirety or in part outside of the terms of agreements between the receiving party and Asio Ltd.

This software is strictly for use in 'proof of concept' implementations and may not under any circumstances be used in any commercial or publicly distributed application.

The contents of this folder, all associated software, and any information or disclosing details contained within are strictly confidential and remain the property of Chirp. They are strictly not for wider disclosure or release beyond recipients involved directly with proof of concept work with Asio Ltd.

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the software.