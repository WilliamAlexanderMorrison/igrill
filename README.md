# iGrill
Monitor your Raspberry Pi 4 and forward it to a mqtt-server.

## What do you need
### Hardware
* A raspberry pi
* A mqtt server as message receiver

## Configuration of MQTT

## Step-by-Step Instructions to Install Configure Raspberry Pi Monitor
* Install both Docker and Docker Compose following instructions in this [documentation](https://withblue.ink/2019/07/13/yes-you-can-run-docker-on-raspbian.html)
* Create a directory with the docker and monitor configuration files in this repo by using the command `git clone https://github.com/WilliamAlexanderMorrison/rpi-monitor-mqtt`
* Navigate into the rpi-monitor-mqtt directory 
* Open the `device.yaml` configuration file 
  * Make naming and topic configuration changes as desired
* Open the `mqtt.yaml` configuration file
  * Replace `IPHOSTNAME` with the IP of your Raspberry Pi with the Broker
  * Replace `USERNAME` to match the `USERNAME` you created for Home Assistant/Mosquitto broker
  * Replace `PASSWORD` to match the `PASSWORD` you created for Home Assistant/Mosquitto broker
  * Make any other configuration changes as desired
* Build the docker with the command `docker-compose build`
  * This will create a docker container with the rpi-monitor-mqtt repo
* Start the docker container with the command `docker-compose up -d`
* Test that the monitor is pushing data to the Mosquitto broker by navigating to the MQTT Developer Tools within Home Assistant, and set the Listen to a Topic to `#` (all) channels and Start Listening
  * You should see a temperature update and a battery update about every 20 seconds
