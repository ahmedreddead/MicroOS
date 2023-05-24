import time
from datetime import datetime
import random
import threading
import paho.mqtt.client as mqtt
from app.module import database



# CREATE USER 'grafana'@'micropolis-vostro-15-3510' IDENTIFIED BY 'pwd123';
client = mqtt.Client()
client.connect("micropolis.local", 1883)
def conn(id):
    global object
    if object.connection.is_connected() :
        pass
    else:
        object = database.Database("micropolis.local", 3306, "grafana", "pwd123", "grafanadb")
        object.connect()

    threading.Timer(10.0, conn, args=(id,)).start()
def publish_temp(id,object):
    value = random.randint(20, 30)
    value2 = random.randint(50, 60)
    topic = "micropolis/temperature/" + str(id)
    client.publish(topic, str(value)+ " °C ")
    object.insert_temperature_sensor_reading(str(id), value ,value2, datetime.now())

def publish_polution(id,object):
    value = random.randint(10, 20)
    topic = "micropolis/polution/" + str(id)
    client.publish(topic, str(value)+ " % ")
    object.insert_polution_sensor_reading(str(id),value,datetime.now())

def publish_hum(id):
    value = random.randint(50, 60)
    topic = "micropolis/humidity/" + str(id)
    client.publish(topic, str(value)+ " % ")
    threading.Timer(30.0, publish_hum, args=(id,)).start()

def publish_door(id,object):
    value = random.choice([0, 1])
    topic = "micropolis/door/" + str(id)
    status = "opened"
    if value == 1 :
        client.publish(topic, "closed")
        status = "closed"
    else:
        client.publish(topic, "opened")
    object.insert_door_sensor_reading(str(id),status,datetime.now())


def publish_motion(id,object):
    value = random.choice([0, 1])
    topic = "micropolis/motion/" + str(id)
    status = "No Motion "
    e = datetime.now()
    if value == 1 :
        client.publish(topic, "Motion is detected : "+"\n"+str(e.strftime("%Y-%m-%d %H:%M:%S")))
        status = "Motion is detected"
    else:
        client.publish(topic, "No Motion")

    object.insert_motion_sensor_reading(str(id),status,e)

def publish_smoke(id,object):
    value = random.choice([0, 1])
    topic = "micropolis/smoke/" + str(id)
    import datetime
    e = datetime.datetime.now()
    if value == 1 :
        client.publish(topic, "No Smoke : "+"\n"+str(e.strftime("%Y-%m-%d %H:%M:%S")))
    else:
        pass

    from datetime import datetime
    object.insert_smoke_sensor_reading(str(id),"No Smoke", datetime.now())


def publish_glass(id,object):
    value = random.choice([0, 1])
    topic = "micropolis/glass/" + str(id)
    status = "No Glass Break "
    e = datetime.now()
    if value == 1 :
        client.publish(topic, "No Glass Break  : "+"\n"+str(e.strftime("%Y-%m-%d %H:%M:%S")))
    else:
        pass
    object.insert_glass_sensor_reading(str(id),status ,e)

def publish_power(id,object):
    value = random.randint(30, 40)
    topic = "micropolis/power/" + str(id)
    client.publish(topic, str(value)+ " % ")
    object.insert_power_reading(value,datetime.now())



publish_hum(1)
publish_hum(2)



def function_send_all(tempN , MotionN , PolutionN , GlassN , DoorN , SmokeN, PowerN ):

    object = database.Database("micropolis.local", 3306, "grafana", "pwd123", "grafanadb")
    object.connect()
    for i in range(1,tempN+1) :
        publish_temp(i,object)

    for i in range(1,MotionN+1) :
        publish_motion(i,object)

    for i in range(1,PolutionN+1) :
        publish_polution(i,object)

    for i in range(1,DoorN+1) :
        publish_door(i,object)

    for i in range(1,SmokeN+1) :
        publish_smoke(i,object)

    for i in range(1,PowerN+1) :
        publish_power(i,object)

    for i in range(1,GlassN+1) :
        publish_glass(i,object)


    object.disconnect()
    threading.Timer(30.0, function_send_all, args=(tempN , MotionN , PolutionN , GlassN , DoorN , SmokeN, PowerN,)).start()


function_send_all (2,3,1,2,4,1,1)


client.loop_forever()
