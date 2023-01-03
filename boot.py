# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
#import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)

# WiFi setup
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('ssid','passphrase')
    while not wlan.isconnected():
        pass

import gc
gc.collect()
