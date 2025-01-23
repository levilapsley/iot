import requests
from grove.grove_light_sensor_v1_2 import GroveLightSensor
import time
import grovepi
import board
import busio
from digitalio import DigitalInOut
import adafruit_rfm9x

import random

# Define pins for the RFM9x
CS = DigitalInOut(board.CE1)  # Chip select
RESET = DigitalInOut(board.D25)  # Reset pin

# Initialize SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize RFM9x module
try:
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    print("RFM9x detected!")
except RuntimeError as error:
    print(f"RFM9x error: {error}")
    exit()

blue = 0   # The blue temperature sensor.
tempSensor = 6  # The Sensor goes on digital port 6
# Setup sensor on analog port A0
sensor = GroveLightSensor(0)

# ThingSpeak API configuration
API_KEY = "DGVB047VO4LE5FFF"
URL = f"https://api.thingspeak.com/update?api_key={API_KEY}"

def read_light():
    return sensor.light

def send_to_thingspeak(light, temp, humidity):
    response = requests.get(URL + f"&field1={light}&field2={temp}&field3={humidity}")
    if response.status_code == 200:
        print(f"Data sent to ThingSpeak: {light} and {temp} and {humidity}")
    else:
        print("Failed to send data to ThingSpeak")

def alert():
    rfm9x.send(b"Alert!")




def main():
    print("Reading sensor values. Press CTRL+C to exit.")
    try:
        while True:
            light = read_light()
            print(f"Light Level: {light}")
            [temp,humidity] = grovepi.dht(tempSensor,blue)
            print(f"Temperature: {temp} C, Humidity: {humidity}%")  
            send_to_thingspeak(light, temp, humidity)

            # Light Level Alerts
            if light < 20 or light > 80:
                alert()

            # Temperature Alerts
            if temp < 10 or temp > 30:
                alert()

            # Humidity Alerts
            if humidity < 40 or humidity > 80:
                alert()




            time.sleep(15)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()


