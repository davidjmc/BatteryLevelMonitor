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
#from machine import Pin, ADC
#from time import sleep
#from umqttsimple import MQTTClient

try:
  import usocket as socket
except:
  import socket

import time

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
#do_connect()

## ThingSpeak Credentials
SERVER = "mqtt.thingspeak.com"
CHANNEL_ID = "YOUR CHANNEL ID"
THINGSPEAK_WRITE_KEY = "YOUR API ID"

## MQTT Settings
#client = MQTTClient("umqtt_client", SERVER) # MQTT client object
#topic = "channels/" + CHANNEL_ID + "/publish/" + THINGSPEAK_WRITE_KEY # Create a MQTT topic string
#PUB_TIME_SEC = 30


# timings in seconds
MESUREMENT_INTERVAL = 10
LAST_MESUREMENT_TIME = 0.0
PUB_TIME_SEC = 5

## Application Settings
#adc = ADC(0)
adc = 500        # Analog channel A0 used to get battery voltage
ratioFactor = 1.3   # Resistors ration factor

# Battery Settings
vinMax = 4.2
vinMin = 2.8

# Voltage Divider 3.158 and 2.105
voutMax = 3.1
voutMin = 2.1

## Function to map Voltage to Percentage
def map(v, in_min, in_max, out_min, out_max):
    return int((v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def map_float(v, in_min, in_max, out_min, out_max):
    return float((v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


## Function to mesure Voltage and Percentage
def mesure_voltage_and_percentage():
    #voltageRaw = adc.read()
    voltageRaw = 939
    ratioFactor = 1.35

    voltage_pinA0 = map_float(voltageRaw, 0, 1023, voutMin, voutMax)
    print('Voltage on pin A0: {v:.2f}'.format(v=voltage_pinA0))

    #voltage_battery = voltage_pinA0 * ratioFactor

    voltage_battery = map_float(voltage_pinA0, voutMin, voutMax, vinMin, vinMax)

    print('Voltage on battery: {v:.2f}'.format(v=voltage_battery))

    percent_battery = map(voltage_battery, vinMin, vinMax, 0, 100)

    print('Voltage: {v:.2f} and Charge: {c:.2f}'.format(v=voltage_battery, c=percent_battery))

    payload = "field1={v:.2f}&field2={c:.2f}".format(v=voltage_battery, c=percent_battery)

    return payload

## Main function
def main():
    while True:
        #current_time = time.time()
        #if current_time - LAST_MESUREMENT_TIME > MESUREMENT_INTERVAL:
            payload = mesure_voltage_and_percentage()
            #client.connect()
            #client.publish(topic, payload)
            #client.disconnect()
            #LAST_MESUREMENT_TIME = current_time
            time.sleep(PUB_TIME_SEC)

    ## Run main function
main()
