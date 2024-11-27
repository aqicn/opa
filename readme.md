
# OPA: Open your Puple Air device to the world 

This standalone python script can be used to export your Puple Air real-time data to the World AQI server.
The script uses the local PA API endpoint (`/json`), so you need to execute this script on the same network
as your PA device.

## Configuration with the local API endpoint

Before starting, make sure to configure the exporter, by editing the `opa.ini` file.
You need to configure the `IP` address of you PA device.

```ini
[pa_local_api]
; IP address of your PA device
ip = 192.168.1.1
; optional name of the device, used on the waqi.info and aqicn.org maps (eg "GEA-SCLA", "")
; name = ...
; optional URL of the website your want to attribute for your PA sensor
; attribution = http://your-website.com
```

You also need to add your own WAQI token, which you can get for free from https://aqicn.org/data-platform/token/:

```ini
[waqi]
; Get your own free token from https://aqicn.org/data-platform/token/
token = dummy-token-for-test-purpose-only
```


You can then run the script using  `python opa.py`


## Configuration with the PA cloud API endpoint 

It is also possible to re-export your data from the PA cloud server, but you will
first need to request an API key from PA: https://community.purpleair.com/t/creating-api-keys/3951

Once you have your key, you need to edit the `opa.ini` file and input the `pa_remote_api` section.

```ini
[pa_remote_api]
sensor_index = 21436
api_key = B144C732-11DE-11EE-A445-42098A784009
```

## Setup

This script is completely library free, so you do not need to install any library.
