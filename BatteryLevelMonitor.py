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

# ESP8266
## Run connect function
#do_connect()

## ThingSpeak Credentials
SERVER = "mqtt.thingspeak.com"
CHANNEL_ID = "YOUR CHANNEL ID"
THINGSPEAK_WRITE_KEY = "YOUR API ID"


# timings in seconds
MESUREMENT_INTERVAL = 10
LAST_MESUREMENT_TIME = 0.0
PUB_TIME_SEC = 5

# ESP8266
## Application Settings
#adc = ADC(0)        # Analog channel A0 used to get battery voltage
#PUB_TIME_SEC = 30


# Battery Settings
vinMax = 4.2
vinMin = 2.8

## Function to map Voltage to Percentage
def map(v, in_min, in_max, out_min, out_max):
    return int((v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def map_float(v, in_min, in_max, out_min, out_max):
    return float((v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


## Function to mesure Voltage and Percentage
def mesure_voltage_and_percentage():
    ratioFactor = 1.27   # Resistors ration factor
    #raw = 0

    # ESP8266
    #for r in range(5):
        #raw = raw + adc.read()
        #time.sleep(1)
    #voltageRaw = raw/5.0

    #test
    voltageRaw = 980
    print('Voltage Raw: {c:.2f}'.format(c=voltageRaw))

    voltage_pinA0 = (voltageRaw / 1024) * 3.3
    print('Voltage on pin A0: {v:.2f}'.format(v=voltage_pinA0))

    voltage_battery = voltage_pinA0 * ratioFactor
    print('Voltage on battery: {v:.2f}'.format(v=voltage_battery))

    percent_battery = map(voltage_battery, vinMin, vinMax, 0, 100)
    print('Voltage: {v:.2f} and Charge: {c:.2f} and Raw: {r:.2f}'.format(v=voltage_battery, c=percent_battery, r=voltageRaw))

    payload = "field1={v:.2f}&field2={c:.2f}&field3={r}&field4={p:.2f}".format(v=voltage_battery, c=percent_battery, r=voltageRaw, p=voltage_pinA0)
    return payload


# ESP8266
def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


## Main function
def main():

    ## MQTT Settings
    #client = MQTTClient("umqtt_client", SERVER) # MQTT client object
    #topic = "channels/" + CHANNEL_ID + "/publish/" + THINGSPEAK_WRITE_KEY # Create a MQTT topic string

    while True:
        payload = mesure_voltage_and_percentage()

        # test with mqtt
        #client.connect()
        #client.publish(topic, payload)
        #client.disconnect()
        time.sleep(PUB_TIME_SEC)

    ## Run main function
main()

# ESP8266
#try:
#    main()
#except OSError as e:
#    restart_and_reconnect()
