package io.chirp.connectdemoapp;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.support.design.widget.Snackbar;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.util.Random;

import io.chirp.connect.ChirpConnect;
import io.chirp.connect.interfaces.ConnectEventListener;
import io.chirp.connect.interfaces.ConnectLicenceListener;
import io.chirp.connect.models.ChirpError;
import io.chirp.connect.models.ConnectState;


public class MainActivity extends AppCompatActivity {

    private ChirpConnect chirpConnect;

    private static final int RESULT_REQUEST_RECORD_AUDIO = 1;

    TextView status;
    TextView lastChirp;
    TextView versionView;




    Button startStopSdkBtn;
    Button startStopSendingBtn;
    EditText txt;
    Boolean startStopSdkBtnPressed = false;

    Activity activity = this;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final View parentLayout = findViewById(android.R.id.content);

        status = (TextView) findViewById(R.id.stateValue);
        lastChirp = (TextView) findViewById(R.id.lastChirp);
        versionView = (TextView) findViewById(R.id.versionView);
        startStopSdkBtn = (Button) findViewById(R.id.startStopSdkBtn);
        startStopSendingBtn = (Button) findViewById(R.id.startStopSengingBtn);
        txt=(EditText)findViewById(R.id.enterText);
        startStopSendingBtn.setAlpha(.4f);
        startStopSendingBtn.setClickable(false);
        startStopSdkBtn.setAlpha(.4f);
        startStopSdkBtn.setClickable(false);

        Log.v("Connect Version: ", ChirpConnect.getVersion());
        versionView.setText(ChirpConnect.getVersion());

        String APP_KEY = "bccBb28f9D13b5C7Ec5d6B5D2";
        String APP_SECRET = "f48cfC1Ae8cada9dfe023b03fB6be7FB7988f69201b4BdBEEE";

        /**
         * Key and secret initialisation
         */
        chirpConnect = new ChirpConnect(this, APP_KEY, APP_SECRET);
        chirpConnect.getLicence(new ConnectLicenceListener() {

            @Override
            public void onSuccess(String licence) {
                ChirpError licenceError = chirpConnect.setLicence(licence);
                if (licenceError.getCode() > 0) {
                    Log.e("setLicenceError", licenceError.getMessage());
                    return;
                }
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        startStopSdkBtn.setAlpha(1f);
                        startStopSdkBtn.setClickable(true);
                    }
                });
            }

            @Override
            public void onError(ChirpError chirpError) {
                Log.e("getLicenceError", chirpError.getMessage());
            }
        });


        /**
         * Set-up the connect callbacks
         */
        chirpConnect.setListener(new ConnectEventListener() {

            @Override
            public void onSending(byte[] data) {
            	/**
		         * onSending is called when a send event begins.
		         * The data argument contains the payload being sent.
		         */
                String hexData = "null";
                if (data != null) {
                    hexData = bytesToHex(data);
                }
                Log.v("connectdemoapp", "ConnectCallback: onSending: " + hexData);
                updateLastPayload(hexData);
            }

            @Override
            public void onSent(byte[] data) {
            	/**
		         * onSent is called when a send event has completed.
		         * The data argument contains the payload that was sent.
		         */
                String hexData = "null";
                if (data != null) {
                    hexData = bytesToHex(data);
                }
                updateLastPayload(hexData);
                Log.v("connectdemoapp", "ConnectCallback: onSent: " + hexData);
            }

            @Override
            public void onReceiving() {
            	/**
		         * onReceiving is called when a receive event begins.
		         * No data has yet been received.
		         */
                Log.v("connectdemoapp", "ConnectCallback: onReceiving");
            }

            @Override
            public void onReceived(byte[] data) {
            	/**
		         * onReceived is called when a receive event has completed.
		         * If the payload was decoded successfully, it is passed in data.
		         * Otherwise, data is null.
		         */
                String hexData = "null";
                if (data != null) {
                    hexData = bytesToHex(data);
                }
                Log.v("connectdemoapp", "ConnectCallback: onReceived: " + hexData);
                updateLastPayload(hexData);
            }

            @Override
            public void onStateChanged(byte oldState, byte newState) {
            	/**
		         * onStateChanged is called when the SDK changes state.
		         */
                Log.v("connectdemoapp", "ConnectCallback: onStateChanged " + oldState + " -> " + newState);
                if (newState == 0) {
                    updateStatus("Stopped");
                } else if (newState == 1) {
                    updateStatus("Paused");
                } else if (newState == 2) {
                    updateStatus("Running");
                } else if (newState == 3) {
                    updateStatus("Sending");
                } else if (newState == 4) {
                    updateStatus("Receiving");
                } else {
                    updateStatus(newState + "");
                }

            }

            @Override
            public void onSystemVolumeChanged(int oldVolume, int newVolume) {
                /**
                 * onSystemVolumeChanged is called when the system volume is changed.
                 */
                Snackbar snackbar = Snackbar.make(parentLayout, "System volume has been changed to: " + newVolume, Snackbar.LENGTH_LONG);
                snackbar.setAction("CLOSE", new View.OnClickListener() {
                            @Override
                            public void onClick(View view) {

                            }
                        })
                        .setActionTextColor(getResources().getColor(android.R.color.holo_red_light ))
                        .show();
                Log.v("connectdemoapp", "System volume has been changed, notify user to increase the volume when sending data");
            }

        });

    }

    @Override
    protected void onResume() {
        super.onResume();

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[] {Manifest.permission.RECORD_AUDIO}, RESULT_REQUEST_RECORD_AUDIO);
        }
        else {
            if (startStopSdkBtnPressed) startSdk();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String permissions[], int[] grantResults) {
        switch (requestCode) {
            case RESULT_REQUEST_RECORD_AUDIO: {
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    if (startStopSdkBtnPressed) stopSdk();
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

    public void updateStatus(final String newStatus) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                status.setText(newStatus);
            }
        });
    }
    public void updateLastPayload(final String newPayload) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {


                StringBuilder output = new StringBuilder("");
	                for (int i = 0; i < newPayload.length(); i += 2) {
		                String str = newPayload.substring(i, i + 2);
		                output.append((char) Integer.parseInt(str, 16));
	                    }
	                String a=output.toString();


                lastChirp.setText(a);
            }
        });
    }

    public void stopSdk() {
        ChirpError error = chirpConnect.stop();
        if (error.getCode() > 0) {
            Log.e("ConnectError: ", error.getMessage());
            return;
        }
        startStopSendingBtn.setAlpha(.4f);
        startStopSendingBtn.setClickable(false);
        startStopSdkBtn.setText("Start Sdk");
    }

    public void startSdk() {
        ChirpError error = chirpConnect.start();
        if (error.getCode() > 0) {
            Log.e("ConnectError: ", error.getMessage());
            return;
        }
        startStopSendingBtn.setAlpha(1f);
        startStopSendingBtn.setClickable(true);
        startStopSdkBtn.setText("Stop Sdk");
    }

    public void startStopSdk(View view) {
        /**
         * Start or stop the SDK.
         * Audio is only processed when the SDK is running.
         */
        startStopSdkBtnPressed = true;
        if (chirpConnect.getConnectState() == ConnectState.AudioStateStopped) {
            startSdk();
        } else {
            stopSdk();
        }
    }

    public void sendPayload(View view) {
    	/**
         * A payload is a byte array dynamic size with a maximum size defined by the licence settings.
         * 
         * Generate a random payload, and send it.
         */
    	long maxPayloadLength = chirpConnect.getMaxPayloadLength();
    	long size = (long) new Random().nextInt((int) maxPayloadLength) + 1;

        String str=txt.getText().toString();
        byte[] abc=str.getBytes();
        byte[] payload = chirpConnect.randomPayload(size);
        long maxSize = chirpConnect.getMaxPayloadLength();
        if (maxSize < payload.length) {
            Log.e("ConnectError: ", "Invalid Payload");
            return;
        }
        ChirpError error = chirpConnect.send(abc);
        if (error.getCode() > 0) {
            Log.e("ConnectError: ", error.getMessage());
        }
    }

    public static String bytesToHex(byte[] in) {
        final StringBuilder builder = new StringBuilder();
        for(byte b : in) {
            builder.append(String.format("%02x", b));
        }
        return builder.toString();
    }
}
