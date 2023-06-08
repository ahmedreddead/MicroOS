import json
import uuid
import paho.mqtt.client as mqtt
import time
import datetime
import re
from app.module import database

mqttBroker = "micropolis.local"
port = 1883
program = 0
client_door_sensor = ""
while program == 0:
    try : 
        client_door_sensor = mqtt.Client("HUB200")
        client_door_sensor.connect(mqttBroker, port)
        client_door_sensor.loop_start()
        client_door_sensor.subscribe("#")
        program = 1
    except :
        pass

print ("mqtt successfully conected")
object = database.Database("micropolis.local", 3306, "grafana", "pwd123", "grafanadb")
object.connect()

print ("database successfully conected")

"""

mqtt:
  sensor:
    - name: "Door Sensor"
      state_topic: "Micropolis/door_sensor/9985/status"
    - name: "Motion Sensor"
      state_topic: "Micropolis/motion_sensor/1231l/status"
    - name: "Motion Sensor lora"
      state_topic: "Micropolis/motion_sensor/loram4512/status"
  switch:
    - unique_id: micropolis_switch
      name: "Micropolis Switch"
      state_topic: "Micropolis/switch/1221/status"
      command_topic: "Micropolis/switch"
      payload_on: "{id:1C,status:on}"
      payload_off: "{id:1C,status:off}"
      state_on: "{id:1C,status:on}"
      state_off: "{id:1C,status:off}"
    - unique_id: micropolis_siren
      name: "Micropolis Siren"
      state_topic: "Micropolis/Siren/1221/status"
      command_topic: "Micropolis/Siren"
      payload_on: "{id:S12235,status:on}"
      payload_off: "{id:S12235,status:off}"
      state_on: "{id:S12235,status:on}"
      state_off: "{id:S12235,status:off}"


"""


def str_to_int_or_ascii(string):
    try:
        return int(string)
    except ValueError:
        return ''.join([str(ord(char)) for char in string])
def connect_and_send_alarm(payload):
    try:
        topic_sensor_state = "IoT_alarm"
        client = mqtt.Client("Hub_alarm")
        client.connect(mqttBroker,port)
        client.loop_start()
        client.publish(topic_sensor_state, str(payload))
        client.loop_stop()
    except :
        pass
def connect_and_send(payload):
    try:
        topic_sensor_state = "IoT_sensor_state"
        client = mqtt.Client("Hub_")
        client.connect(mqttBroker,port)
        client.loop_start()
        print(str(payload))
        client.publish(topic_sensor_state, str(payload))
        client.loop_stop()
    except :
        pass
def connect_and_send_with_topic(topic , payload):
    try:
        client = mqtt.Client("Hub_new")
        client.connect(mqttBroker,port)
        client.loop_start()
        print(str(topic)+ str(payload))
        client.publish(str(topic), str(payload))
        client.loop_stop()
    except :
        pass
def send_mqtt_to_rasberrypi(topic, payload) :
    global client_door_sensor

    client_door_sensor.publish(str(topic), str(payload))
def on_message(client, userdata, message):
    global object
    #print("message received " ,str(message.payload.decode("utf-8")))
    #print("message topic=",message.topic)
    try:
        if message.topic == "Micropolis/door_sensor" :
            topic = 2
            payload = str(message.payload.decode("utf-8")).strip()
            print(payload)
            _id = payload.replace("{", "").replace("}", "").split(",")[0].split(":")[1]
            #result = re.search('{status:(.*)}',payload)
            #if result is not None:
            #_status = result.group(1)
            _status = payload.replace("{", "").replace("}", "").split(",")[1].split(":")[1]



            print(_status)
            status = _status

            if _status == "opened":
                _status = 1
            else:
                _status = 0
            battery = 3.3
            online = 1
            #json_payload_dictionary = {"serial_number": _id, "battery": battery, "state": _status, "online": online}
            #json_payload = json.dumps(json_payload_dictionary)
            #connect_and_send(json_payload)

            #send_topic = "Micropolis/"+str(topic)+ "/"+str(_id)
            #connect_and_send_with_topic(str(send_topic),json_payload)

            #send_topic2 = "Micropolis/"+str(topic)+ "/"+str(_id)+"/status"
            #connect_and_send_with_topic(str(send_topic2), str(_status))

            send_mqtt_to_rasberrypi('Micropolis/door_sensor/9985/status',str(status))

            ## database insertion

            if not object.ckeck_connection():
                object = database.Database("micropolis.local", 3306, "grafana", "pwd123", "grafanadb")
                object.connect()


            if len(str (str_to_int_or_ascii(_id)) ) > 5 :
                _id = str_to_int_or_ascii(_id)[:5]


            result = object.check_sensorid(str_to_int_or_ascii(_id))
            if result is None:
                object.insert_new_sensor(str_to_int_or_ascii(_id) ,"wifi" , "micropolis door sensor")

            object.insert_door_sensor_reading(str_to_int_or_ascii(_id), str(status), datetime.datetime.now())
            ##object.disconnect()

        elif message.topic == "Micropolis/panic_sensor" :
            payload = str(message.payload.decode("utf-8")).strip()
            if payload == "Alarm_ON":
                _id = str(uuid.uuid4())
                list_of_sensors = ["00123"]
                json_payload_dictionary = {"id": _id, "sensors": list_of_sensors}
                json_payload = json.dumps(json_payload_dictionary)
                connect_and_send_alarm(json_payload)
                e = datetime.datetime.now()
                send_mqtt_to_rasberrypi('Micropolis/panic/22/status', "Alarm On at"+"\n"+str(e.strftime("%Y-%m-%d %H:%M:%S")))

        elif message.topic == "Micropolis/Siren" :
            topic = 1
            payload = str(message.payload.decode("utf-8")).strip()
            _id = payload.replace("{", "").replace("}", "").split(",")[0].split(":")[1]
            _status = payload.replace("{", "").replace("}", "").split(",")[1].split(":")[1]
            status = _status
            if _status == "on":
                _status = 1
            else:
                _status = 0
            battery = 3.3
            online = 1
            #json_payload_dictionary = {"serial_number": _id, "battery": battery, "state": _status, "online": online}
            #json_payload = json.dumps(json_payload_dictionary)
            #connect_and_send(json_payload)
            send_mqtt_to_rasberrypi('Micropolis/Siren/1221/status',str(status))

            #send_topic = "Micropolis/" + str(topic) + "/" + str(_id)
            #connect_and_send_with_topic(str(send_topic), json_payload)

            #send_topic2 = "Micropolis/" + str(topic) + "/" + str(_id) + "/status"
            #connect_and_send_with_topic(str(send_topic2), str(_status))


            if not object.ckeck_connection():
                object = database.Database("micropolis.local", 3306, "grafana", "pwd123", "grafanadb")
                object.connect()
            print(str_to_int_or_ascii(_id))

            if len(str (str_to_int_or_ascii(_id)) ) > 5 :
                _id = str_to_int_or_ascii(_id)[:5]


            result = object.check_actuatorid(str_to_int_or_ascii(_id))
            if result is None:
                object.insert_new_actuator(str_to_int_or_ascii(_id), "wifi", "micropolis siren ")

            object.insert_siren_reading(str_to_int_or_ascii(_id), str(status), datetime.datetime.now())
            #object.disconnect()

        elif message.topic == "Micropolis/switch" :
            topic = 0
            payload = str(message.payload.decode("utf-8")).strip()
            _id = payload.replace("{", "").replace("}", "").split(",")[0].split(":")[1]
            _status = payload.replace("{", "").replace("}", "").split(",")[1].split(":")[1]
            status = _status
            if _status == "on":
                _status = 1
            else:
                _status = 0
            battery = 3.3
            online = 1

            json_payload_dictionary = {"serial_number": _id, "battery": battery, "state": _status, "online": online}
            json_payload = json.dumps(json_payload_dictionary)
            #connect_and_send(json_payload)
            send_mqtt_to_rasberrypi('Micropolis/switch/1221/status', str(status))

            #send_topic = "Micropolis/" + str(topic) + "/" + str(_id)
            #connect_and_send_with_topic(str(send_topic), json_payload)

            #send_topic2 = "Micropolis/" + str(topic) + "/" + str(_id) + "/status"
            #connect_and_send_with_topic(str(send_topic2), str(_status))

            if not object.ckeck_connection():
                object = database.Database("micropolis.local", 3306, "grafana", "pwd123", "grafanadb")
                object.connect()

            result = object.check_actuatorid(str_to_int_or_ascii(_id))
            if result is None:
                object.insert_new_actuator(str_to_int_or_ascii(_id) ,"wifi" , "micropolis switch ")

            object.insert_relay_switch_reading(str_to_int_or_ascii(_id), str(status), datetime.datetime.now())
            #object.disconnect()

        elif message.topic == "Micropolis/motion_sensor" :
            topic = 3
            payload = str(message.payload.decode("utf-8")).strip()
            _id = payload.replace("{", "").replace("}", "").split(",")[0].split(":")[1]
            _status = payload.replace("{", "").replace("}", "").split(",")[1].split(":")[1]
            print(_id)
            print(_status)
            status = _status
            if _status == " Motion Detected":
                _status = 1
            else:
                _status = 0
            battery = 3.3
            online = 1
            json_payload_dictionary = {"serial_number": _id, "battery": battery, "state": _status, "online": online}
            json_payload = json.dumps(json_payload_dictionary)
            #connect_and_send(json_payload)
            e = datetime.datetime.now()
            if _id == "loram4512" :
                send_mqtt_to_rasberrypi('Micropolis/motion_sensor/loram4512/status',
                                        str(status) + "\n" + str(e.strftime("%Y-%m-%d %H:%M:%S")))

            else :
                send_mqtt_to_rasberrypi('Micropolis/motion_sensor/1231l/status',str(status)+"\n"+str(e.strftime("%Y-%m-%d %H:%M:%S")))

            #send_topic = "Micropolis/" + str(topic) + "/" + str(_id)
            #connect_and_send_with_topic(str(send_topic), json_payload)

            #send_topic2 = "Micropolis/" + str(topic) + "/" + str(_id) + "/status"
            #connect_and_send_with_topic(str(send_topic2), str(_status))


            if not object.ckeck_connection():
                object = database.Database("micropolis.local", 3306, "grafana", "pwd123", "grafanadb")
                object.connect()


            if len(str (str_to_int_or_ascii(_id)) ) > 5 :
                _id = str_to_int_or_ascii(_id)[:5]

            result = object.check_sensorid(str_to_int_or_ascii(_id))
            if result is None:
                object.insert_new_sensor(str_to_int_or_ascii(_id) ,"wifi" , "micropolis motion sensor")

            object.insert_motion_sensor_reading(str_to_int_or_ascii(_id), str(status), datetime.datetime.now())
            time.sleep(3)
            object.insert_motion_sensor_reading(str_to_int_or_ascii(_id), str("No Motion"), datetime.datetime.now())

            #object.disconnect()


        elif str (message.topic).startswith("Micropolis/0/") :
            topic = "Micropolis/switch"
            status = "non"
            id = str(message.topic).split('/')[2]
            if str(message.payload) == "1" :
                status ="on"
            else:
                status = "off"
            payload = '{id:'+str(id)+',status:'+status+'}'
            connect_and_send_with_topic(topic , payload)
        elif str (message.topic).startswith("Micropolis/1/") :
            topic = "Micropolis/Siren"
            status = "non"
            id = str(message.topic).split('/')[2]
            if str(message.payload) == "1" :
                status ="on"
            else:
                status = "off"
            payload = '{id:'+str(id)+',status:'+status+'}'
            connect_and_send_with_topic(topic , payload)


    except Exception as e:
        print(e)



client_door_sensor.on_message = on_message


while 1 :
    #time.sleep(300)
    pass

