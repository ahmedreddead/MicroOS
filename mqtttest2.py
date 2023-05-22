import random
import threading

import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("micropolis.local", 1883)

value = random.randint(20, 30)
client.publish("online", "online")
topic = "office/light/switch/2"
client.publish(topic, "ON")