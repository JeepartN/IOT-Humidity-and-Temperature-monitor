from machine import Pin
import dht
import utime
import ubinascii
from umqtt.simple import MQTTClient

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
SERVER = "io.adafruit.com"
PORT = 1883

#Settings:
#Username and key for adafruit
USERNAME = ""
PASSWORD = ""
#Where to report the data
TEMP_TOPIC = b""
HUM_TOPIC = b""
#Set the interval at which the picow will report data
publish_interval = 5

last_publish = utime.time()
client = MQTTClient(CLIENT_ID, SERVER, PORT, USERNAME, PASSWORD, keepalive=60)

sensorPin = machine.Pin(28, Pin.IN)
sensor = dht.DHT11(sensorPin)

LED = Pin('LED', machine.Pin.OUT)
def main():
    connectToMQTT()
    while True:
        global last_publish
        if(utime.time() - last_publish) >= publish_interval:
            LED.toggle()
            sensor.measure()
            temp = sensor.temperature()
            humidity = sensor.humidity()
            print("temperature(C): {}" .format(temp))
            print("humidity(%): {}" .format(humidity))
            client.publish(TEMP_TOPIC, str(temp).encode())
            client.publish(HUM_TOPIC, str(humidity).encode())
            LED.toggle()
            last_publish = utime.time()
        utime.sleep(5)
        
    
def connectToMQTT():
    print(f"Connecting to MQTT broker :: {SERVER}")
    client.connect()
    print(f"Connection successful!")

def reset():
    print("Resetting!")
    utime.sleep(3)
    machine.reset()
    
if __name__ == "__main__":
    while True:
        try:
            main()
        except OSError as e:
            print("Error: " + str(e))
            reset()
