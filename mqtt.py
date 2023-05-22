import random
import threading

import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("micropolis.local", 1883)

def publish_temp(id):
    value = random.randint(20, 30)
    topic = "micropolis/temperature/" + str(id)
    client.publish(topic, str(value)+ " °C ")
    threading.Timer(30.0, publish_temp, args=(id,)).start()
def publish_polution(id):
    value = random.randint(10, 20)
    topic = "micropolis/polution/" + str(id)
    client.publish(topic, str(value)+ " % ")
    threading.Timer(30.0, publish_polution, args=(id,)).start()
def publish_hum(id):
    value = random.randint(50, 60)
    topic = "micropolis/humidity/" + str(id)
    client.publish(topic, str(value)+ " % ")
    threading.Timer(30.0, publish_hum, args=(id,)).start()

def publish_door(id):
    value = random.choice([0, 1])
    topic = "micropolis/door/" + str(id)
    if value == 1 :
        client.publish(topic, "closed")
    else:
        client.publish(topic, "opened")

    threading.Timer(30.0, publish_door, args=(id,)).start()


def publish_motion(id):
    value = random.choice([0, 1])
    topic = "micropolis/motion/" + str(id)
    import datetime
    e = datetime.datetime.now()
    if value == 1 :
        client.publish(topic, "Motion is detected : "+"\n"+str(e.strftime("%Y-%m-%d %H:%M:%S")))
    else:
        client.publish(topic, "Motion is not detected")

    threading.Timer(30.0, publish_motion, args=(id,)).start()

def publish_smoke(id):
    value = random.choice([0, 1])
    topic = "micropolis/smoke/" + str(id)
    import datetime
    e = datetime.datetime.now()
    if value == 1 :
        client.publish(topic, "No Smoke : "+"\n"+str(e.strftime("%Y-%m-%d %H:%M:%S")))
    else:
        pass

    threading.Timer(30.0, publish_smoke, args=(id,)).start()

def publish_glass(id):
    value = random.choice([0, 1])
    topic = "micropolis/glass/" + str(id)
    import datetime
    e = datetime.datetime.now()
    if value == 1 :
        client.publish(topic, "No Glass Break  : "+"\n"+str(e.strftime("%Y-%m-%d %H:%M:%S")))
    else:
        pass

    threading.Timer(30.0, publish_glass, args=(id,)).start()

publish_temp(1)
publish_temp(2)

publish_hum(1)
publish_hum(2)

publish_smoke(1)

publish_door(1)
publish_door(2)
publish_door(3)
publish_door(4)

publish_motion(1)
publish_motion(2)
publish_motion(3)

publish_glass(1)
publish_glass(2)

publish_polution(1)



client.loop_forever()
