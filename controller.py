import time
import datetime
import sys
import json
import requests
import xively
import subprocess
from random import randint
import dhtreader
from Adafruit_BMP085 import Adafruit_BMP085
import spidev

global temp_datastream
global humidity_datastream
global rgb_datastream

#Initialize temp and humidity sensor
dev_type=22
dht_pin=24
dhtreader.init()

#Initialize TCS3200 sensor

#Open SPI bus
spi=spidev.Spidev()
spi.Open(0,0)

#Initialise Xively feed
FEED_ID="feed_id"
API_KEY="api_key"
api=xively.XivelyAPIClient(API_KEY)

#Read temp and humidity from DHT22 sensor
def read_DHT22_sensor():
    temp,humidity=dhtreader.read(dev_type,dht_pin)
    return temp,humidity

#Read rgb value from TCS3200 sensor

#Controller main function
def runController():
    global temp_datastream
    global humidity_datastream
    global rgb_datastream
    
    temp,humidity=read_DHT22_sensor()

    temp_datastream.current_value=temperature
    temp_datastream.at=datetime.datetime.utcnow()

    humidity_datastream.current_value=humidity
    humidity_datastream.at=datetime.datetime.utcnow()

    rgb_datastream.current_value=rgb
    rgb_datastream.at = datetime.datetime.utcnow()

    print ("Updating Xively feed with temperature:%s " % temperature)
    try:
        temp_datastream.update()
    except requests.HTTPError as e:
        print ("HTTP error")

    print("Updating Xively feed with humidity: %s"%humidity)
    try:
        humidity_datastream.update()
    except requests.HTTPError as e:
        print ("HTTP error")
    
    print("Updating Xively feed with rgb: %s"%rgb)
    try:
        rgb_datastream.update()
    except requests.HTTPError as e:
        print("HTTP error")
    
    #Get existing or create new Xively datastream for temperature,humidity and rgb
def get_tempdatastream(feed):
    try:
        datastream= feed.datastreams.get("temperature")
        return datastream
    except:
        datastream=feed.datastreams.create("temperature")
        return datastream
def get_humiditydatastream(feed):
    try:
        datastream= feed.datastreams.get("humidity")
        return datastream
    except:
        datastream=feed.datastreams.create("humidity")
        return datastream
def get_rgbdatastream(feed):
    try:
        datastream= feed.datastreams.get("rgb")
        return datastream
    except:
        datastream=feed.datastreams.create("rgb")
        return datastream
#Controller setup function
def setupController():
    global temp_datastream
    global humidity_datastream
    global rgb_datastream

    feed=api.feeds.get(FEED_ID)

    feed.update()

    temp_datastream=get_tempdatastream(feed)
    humidity_datastream=get_humiditydatastream(feed)
    rgb_datastream=get_rgbdatastream(feed)

setupController()
while True:
    runController()
    time.sleep(10)