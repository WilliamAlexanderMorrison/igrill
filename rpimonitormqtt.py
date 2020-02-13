from builtins import range
from builtins import object
import logging
import threading
import time

import random

import utils

import os
import psutil
import subprocess


class IDevicePeripheral():
    def __init__(self, name):
        """
        Instantiates device
        """
        logging.debug("Loading statistics for the device {}".format(name))
        self.name = name

    def load_1m(self):
        #https://github.com/home-assistant/home-assistant/blob/dev/homeassistant/components/systemmonitor/sensor.py
        try:
            result = round(os.getloadavg()[0], 2)
        except:
            return False

        return result

    def memory_use_percent(self):
        try:
            result = psutil.virtual_memory().percent
        except:
            return False

        return result

    def temperature(self):
        #https://thesmithfam.org/blog/2005/11/19/python-uptime-script/
        try:
            f = open( "/sys/class/thermal/thermal_zone0/temp" )
            result = f.read().split()
            f.close()
        except:
            return False

        return result[0]

    def last_boot(self):
        try:
            result = psutil.boot_time()
        except:
            return False

        return result


    def disk_use_percent(self):
        #https://stackoverflow.com/questions/12027237/selecting-specific-columns-from-df-h-output-in-python
        try:
            p = subprocess.Popen("df -Ph", stdout=subprocess.PIPE, shell=True)
            dfdata, _ = p.communicate()
        except:
            return False

        dfdata = dfdata.splitlines()
        result = dfdata[1].split()
        return result[4].rstrip("%")

    def rpi_power_status(self):
        #https://github.com/custom-components/sensor.rpi_power/blob/master/custom_components/rpi_power/sensor.py
        try:
            f = open( "/sys/devices/platform/soc/soc:firmware/get_throttled" )
            contents = f.read().split()
            f.close()
        except:
            return False

        if contents[0] == '0':
            result = 'Everything is working as intended'
        elif contents[0] == '1000':
            result = 'Under-voltage was detected, consider getting a uninterruptible power supply for your Raspberry Pi.'
        elif contents[0] == '2000':
            result = 'Your Raspberry Pi is limited due to a bad powersupply, replace the power supply cable or power supply itself.'
        elif contents[0] == '3000':
            result = 'Your Raspberry Pi is limited due to a bad powersupply, replace the power supply cable or power supply itself.'
        elif contents[0] == '4000':
            result = 'The Raspberry Pi is throttled due to a bad power supply this can lead to corruption and instability, please replace your changer and cables.'
        elif contents[0] == '5000':
            result = 'The Raspberry Pi is throttled due to a bad power supply this can lead to corruption and instability, please replace your changer and cables.'
        elif contents[0] == '8000':
            result = 'Your Raspberry Pi is overheating, consider getting a fan or heat sinks.'
        else:
            result = 'There is a problem with your power supply or system.'
        return result

class RaspberryPiPeripheral(IDevicePeripheral):
    """
    Specialization of iDevice peripheral for the RaspberryPi
    """
    def __init__(self, name='raspberrypi'):
        logging.debug("Created new device with name {}".format(name))
        IDevicePeripheral.__init__(self, name)

class DeviceThread(threading.Thread):
    device_types = {'raspberrypi': RaspberryPiPeripheral}

    def __init__(self, thread_id, name, device_type, mqtt_config, topic, interval, run_event):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.type = device_type
        self.mqtt_client = utils.mqtt_init(mqtt_config)
        self.topic = topic
        self.interval = interval
        self.run_event = run_event

    def run(self):
        while self.run_event.is_set():
            try:
                logging.debug("Device thread {} (re)started, trying to collect statistics".format(self.name))
                device = self.device_types[self.type](self.name)
                self.mqtt_client.reconnect()
                while True:
                    payload = {}
                    load_1m = device.load_1m()
                    if load_1m:
                        payload['load_1m'] = load_1m
                    memory_use_percent = device.memory_use_percent()
                    if memory_use_percent:
                        payload['memory_use_percent'] = memory_use_percent
                    temperature = device.temperature()
                    if temperature:
                        payload['temperature'] = temperature
                    last_boot = device.last_boot()
                    if last_boot:
                        payload['last_boot'] = last_boot
                    disk_use_percent = device.disk_use_percent()
                    if disk_use_percent:
                        payload['disk_use_percent'] = disk_use_percent
                    rpi_power_status = device.rpi_power_status()
                    if rpi_power_status:
                        payload['rpi_power_status'] = device.rpi_power_status()

                    utils.publish(payload, self.mqtt_client, self.topic, device.name)
                    logging.debug("Published payload: {} to topic {}/{}".format(payload, self.topic, device.name))
                    logging.debug("Sleeping for {} seconds".format(self.interval))
                    time.sleep(self.interval)
            except Exception as e:
                logging.debug(e)
                logging.debug("Sleeping for {} seconds before retrying".format(self.interval))
                time.sleep(self.interval)

        logging.debug('Thread exiting')
