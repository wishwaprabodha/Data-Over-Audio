# Chirp SDK for Android

The Chirp SDK for Android allows you to send and receive data from within your Android application. It communicates directly with the audio hardware to generate and receive data, played from the device's speaker.

## Getting started with your own app


To get started with the Chirp SDK, you'll first need to register for Chirp Application credentials. Sign up to the developer console at the [Chirp Admin Center](https://admin.chirp.io). Once signed in, you will have access to your app key and secret.

**Step 1** - Copy the `chirp-connect-3.3.4.aar` file to your `app/libs` directory. Add the following to the `dependencies` block of your Module `build.gradle` Gradle script:

``` java
compile 'io.chirp.connect:chirp-connect-3.3.4@aar'
compile 'com.squareup.okhttp3:okhttp:3.9.0'
```

To instruct Gradle where to find the local `.aar` file, add `flatDir` section to the `repositories` block. (You'll need to add a `repositories` block if one does not already exist.)

``` java
repositories {
    flatDir {
        dirs 'libs'
    }
}
```

**Step  2**  - To declare that your app requires audio permissions, add the following to your `AndroidManifest.xml`, inside the bottom of the `<manifest>` element. Please note that `INTERNET` and `ACCESS_NETWORK_STATE` permissions are not required if you already downloaded the licence from the Admin Centre.

``` xml
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />

<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

Chirp SDK requires at minimum of Android 4.1.x which is Android API level 15.


**Step 3** - Include the SDK:
``` java
import io.chirp.connect.ChirpConnect;
import io.chirp.connect.interfaces.ConnectEventListener;
import io.chirp.connect.interfaces.ConnectLicenceListener;
import io.chirp.connect.models.ChirpError;
import io.chirp.connect.models.ConnectState;
```

And instantiate the SDK with your own application key and secret. 

```java
String KEY = "YOUR_APP_KEY_HERE";
String SECRET = "YOUR_APP_SECRET_HERE";
String LICENCE = "YOUR_LICENCE_HERE";   //If you have one

chirpConnect = new ChirpConnect(this, KEY, SECRET);
```

The licence must be set right after the SDK is instantiated. If you dont have the licence you can get it using `getLicence` method:

```Java
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



Otherwise, if you have the licence string you can set it directly:

```java
ChirpError setLicenceError = chirpConnect.setLicence(LICENCE);
if (setLicenceError.getCode() > 0) {
    Log.e("ChirpError:", setLicenceError.getMessage());
}
```



To be able to send and receive data we need to implement the `ConnectEventListener` interface:

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


We can now start the audio processing loop of the SDK in order to send or receive data. Please make sure that the licence is set before starting the SDK.

```java
chirpConnect.start();
```

First we will generate some random data to send using the SDK. When the `.send()` method is called, Connect will encode the data and send it out through the device's loudspeaker. The length of the data can be dynamic but should not exceed the size of the maximum payload length set by your licence configuration. The maximum payload length is returned by the `.getMaxPayloadLength()` method. 
```java
long maxLength = chirpConnect.getMaxPayloadLength();
byte[] payload = chirpConnect.randomPayload(maxLength);
chirpConnect.send(payload);
```

**Step 4** - Requesting Permissions at Run Time
Beginning in version 6.0 (API level 23), Android allows users to toggle apps permissions at run time. Also by default, some permissions will be disabled when the app starts up for the first time.

The RECORD_AUDIO permission, which is fundamental in the use of ChirpConnect, is an example of this. Therefore, it is important to check your app has RECORD_AUDIO permissions every time it is brought to the foreground.

We recommend using the android lifecycle methods, onResume() and onPause() to detect permissions and to trigger start and stopping listening. See the following:

```java
@Override
protected void onResume() {
  super.onResume();

  if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
    ActivityCompat.requestPermissions(this, new String[] {Manifest.permission.RECORD_AUDIO}, RESULT_REQUEST_RECORD_AUDIO);
  }
  else {
    chirpConnect.start();
  }
}

@Override
public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
  switch (requestCode) {
    case RESULT_REQUEST_RECORD_AUDIO: {
      if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
        chirpConnect.start();
      }
      return;
    }
  }
}

@Override
protected void onPause() {
  super.onPause();
  chirpConnect.stop();
}
```



You are now ready to start using ChirpConnect in your own application.

## License
This software is copyright © 2011-2018, Asio Ltd.
All rights reserved.

This software is strictly confidential and not to be redistributed in its entirety or in part outside of the terms of agreements between the receiving party and Asio Ltd.

This software is strictly for use in 'proof of concept' implementations and may not under any circumstances be used in any commercial or publicly distributed application.

The contents of this folder, all associated software, and any information or disclosing details contained within are strictly confidential and remain the property of Chirp. They are strictly not for wider disclosure or release beyond recipients involved directly with proof of concept work with Asio Ltd.

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the software.
