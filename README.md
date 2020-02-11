# iGrill
Monitor your Raspberry Pi 4 and forward it to a mqtt-server.

## What do you need
### Hardware
* A raspberry pi
* A mqtt server as message receiver

## Configuration of MQTT

## Docker Instructions
DOCUMENTATION FOR INSTALLING VIA DOCKER HERE

REMAINING DOCUMENTATION FROM FORKED PROJECT, TO BE DELETED.
## Installation
1. clone this repo
1. install required modules (see requirements.txt)
1. Add at least one device config (see ./exampleconfig/device.yaml) - to find your device MAC just run `hcitool lescan`
1. start application `./monitor.py`
1. enjoy

### systemd startup-script

Place this file into the proper folder - for instance: `/lib/systemd/system/igrill.service`

```bash
[Unit]
Description=igrill MQTT service
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=2
ExecStart=/usr/bin/python <path_to_igrill_repo>/monitor.py -c <path_to_config_dir>

[Install]
WantedBy=multi-user.target
```

Run `systemctl daemon-reload && systemctl enable igrill && systemctl start igrill`

Next time you reboot, the iGrill service will connect and reconnect if something goes wrong...

