import utime
import network
import socket

wlan = network.WLAN(network.STA_IF)

#Input network details here:
SSID = ""
PASSWORD = ""

def connectToWifi():
    wlan.config(pm = 0xa11140)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while wlan.isconnected() == False:
        print('Connecting...')
        utime.sleep(1)
    print(wlan.ifconfig())
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    
    return ip

try:
    ip = connectToWifi()
except KeyboardInterrupt:
    machine.reset()
    
