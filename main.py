import time
import ntptime
import urllib.urequest as http

import dht
from machine import I2C, Pin

import CCS811

DATA_URL = 'http://api-server:8080/air_data'
LOC = 'office'
ntptime.host = "us.pool.ntp.org"

def main():
    # setup the pins, 5/4 are normal scl/sda, 12 is normal 1-wire, 16 is on-board LED
    i2c = I2C(scl=Pin(5), sda=Pin(4))
    s = CCS811.CCS811(i2c=i2c, addr=90)
    d = dht.DHT22(Pin(12))
    activity_led = Pin(16, Pin.OUT)
    ntptime.settime()
    l_counter = 0
    time.sleep(1)

    # Main run loop, run forever
    while True:

        # Get a timestamp and make it pretty
        c_time = time.gmtime()
        str_time = f'{c_time[0]}-{c_time[1]:02d}-{c_time[2]:02d} {c_time[3]:02d}:{c_time[4]:02d}:{c_time[5]:02d}'

        # Update the environment sensor every 10th run
        if l_counter % 10 == 0:
            d.measure()
            print(f'Updating env, Temp:{d.temperature()}, Humidity:{d.humidity()}')
            s.put_envdata(d.humidity(), d.temperature())

        # Update the time from ntp every 100 runs
        if l_counter >= 100:
            print(f'{str_time} - time refresh')
            ntptime.settime()
            l_counter = -1

        # Get the environment data and send it to the server
        if s.data_ready():
            # Inverse-logic, turn on LED to show we're doing things
            activity_led.off()
            payload = f'["{str_time}", {d.temperature()}, {d.humidity()}, {s.eCO2}, {s.tVOC}, "{LOC}"]'
            print(payload)
            resp = http.urlopen(DATA_URL, data=payload, method='POST')
            print(resp.read())
            resp.close()
            time.sleep(1)
        
        # Turn off the LED, inc the counter, and sleep
        activity_led.on()
        l_counter += 1
        time.sleep(9)

# Run the loop
main()