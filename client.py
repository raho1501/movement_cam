import paho.mqtt.client as mqtt
import time

############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload))

########################################
broker_address="192.168.1.250"
#broker_address="iot.eclipse.org"
print("creating new instance")
mclient = mqtt.Client("Sniff") #create new instance
mclient.on_message=on_message #attach function to callback
print("connecting to broker")
mclient.connect(broker_address,port=40008, keepalive=60) #connect to broker
mclient.loop_start() #start the loop
print("Subscribing")
mclient.subscribe("home")
run = True
try:
    while True:
        mclient.loop()
except KeyboardInterrupt:
    mclient.loop_stop()
    mclient.disconnect()
    pass
