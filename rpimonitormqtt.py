from builtins import range
from builtins import object
import logging
import threading
import time

import random

import utils


class IDevicePeripheral():
    def __init__(self, name):
        """
        Connects to the device given by address performing necessary authentication
        """
        logging.debug("Trying to connect to the device {}".format(name))
        self.name = name

class RaspberryPi():
    """
    Specialization of iDevice peripheral for the RaspberryPi
    """
    def __init__(self, name='raspberrypi'):
        logging.debug("Created new device with name {}".format(name))
        IDevicePeripheral.__init__(self, name)	

class DeviceThread(threading.Thread):

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
                self.mqtt_client.reconnect()
                while True:
                    payload = 100;
                    utils.publish(payload, self.mqtt_client, self.topic, self.name)
                    logging.debug("Published payload: {} to topic {}/{}".format(payload, self.topic, self.name))
                    logging.debug("Sleeping for {} seconds".format(self.interval))
                    time.sleep(self.interval)
            except Exception as e:
                logging.debug(e)
                logging.debug("Sleeping for {} seconds before retrying".format(self.interval))
                time.sleep(self.interval)

        logging.debug('Thread exiting')
