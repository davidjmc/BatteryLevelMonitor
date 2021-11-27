#!/usr/bin/env python
#
#
# BatteryLevelMonitor.py
#
#
# Copyright 2021 David Cavalcanti
#
#
#

## import general libraries
from machine import Pin, ADC
from time import sleep
from umqttsimple import MQTTClient

try:
  import usocket as socket
except:
  import socket

## WiFi Credentials
WIFI_SSID = 'YourWifiSSID'
WIFI_PASS = 'YourWifiPassword'

## Function to connect to local WiFi:
def do_connect():
    wifi = network.WLAN(network.STA_IF)
    if not wifi.isconnected():

        print('Connecting to WiFi...')

        wifi.active(True)
        wifi.connect(WIFI_SSID, WIFI_PASS)
        while not wifi.isconnected():
            pass

    print('Network Configuration:', wifi.ifconfig())

## Run connect function
do_connect()

## ThingSpeak Credentials
SERVER = "mqtt.thingspeak.com"
CHANNEL_ID = "YOUR CHANNEL ID"
THINGSPEAK_WRITE_KEY = "YOUR API ID"

## MQTT Settings
client = MQTTClient("umqtt_client", SERVER) # MQTT client object
topic = "channels/" + CHANNEL_ID + "/publish/" + THINGSPEAK_WRITE_KEY # Create a MQTT topic string
PUB_TIME_SEC = 30


# timings in seconds
MESUREMENT_INTERVAL = 10
LAST_MESUREMENT_TIME = 0.0

## Application Settings
adc = ADC(0)        # Analog channel A0 used to get battery voltage
ratioFactor = 1.3   # Resistors ration factor

# Battery Settings
voltageMax = 4.2
voltageMin = 2.8

## Function to map Voltage to Percentage
def map(v, in_min, in_max, out_min, out_max):
    return int((v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

## Function to mesure Voltage and Percentage
def mesure_voltage_and_percentage():
    voltageRaw = adc.read()
    voltage = (voltageRaw / 1024) * 3.3
    voltage = voltage * ratioFactor
    percent = map(voltage, voltageMin, voltageMax, 0, 100)

    print('Voltage: %.2f and Charge: %.2d' % (voltage, percent))

    payload = "field1=%.2f&field2=%.2f" % (voltage, percent)

  return payload

## Main function
def main():
    while True:
        current_time = time.time()
        if current_time - LAST_MESUREMENT_TIME > MESUREMENT_INTERVAL:
            payload = mesure_voltage_and_percentage()
            client.connect()
            client.publish(topic, payload)
            client.disconnect()
            LAST_MESUREMENT_TIME = current_time

        time.sleep(PUB_TIME_SEC)

## Run main function
main()
