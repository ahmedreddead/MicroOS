import json
import uuid
import paho.mqtt.client as mqtt
import time

mqttBroker = "micropolis.local"
port = 1883

client = mqtt.Client("HUB")
client.connect(mqttBroker, port)
client.loop_start()
client.subscribe("#")

def connect_and_send_alarm(payload):
    try:
        topic_sensor_state = "IoT_alarm"
        global client
        client.connect(mqttBroker,port)
        client.publish(topic_sensor_state, str(payload))
    except :
        pass

def connect_and_send(payload):
    try:
        topic_sensor_state = "IoT_sensor_state"
        global client
        client.connect(mqttBroker,port)
        client.publish(topic_sensor_state, str(payload))
    except :
        pass


def connect_and_send_ras(topic, payload):
    try:
        global client
        client.connect(mqttBroker,port)
        client.publish(str(topic), str(payload))
    except :
        pass
def send_mqtt_to_rasberrypi(topic, payload) :
    global client
    client.connect(mqttBroker, port)
    client.publish(str(topic), str(payload))

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    try:
        if message.topic == "Micropolis/door_sensor" :
            topic = 2
            payload = str(message.payload.decode("utf-8")).strip()
            _id = payload.replace("{", "").replace("}", "").split(",")[0].split(":")[1]
            _status = payload.replace("{", "").replace("}", "").split(",")[1].split(":")[1]
            status = _status
            if _status == "opened":
                _status = 1
            else:
                _status = 0
            battery = 3.3
            online = 1
            json_payload_dictionary = {"serial_number": _id, "battery": battery, "state": _status, "online": online}
            json_payload = json.dumps(json_payload_dictionary)
            connect_and_send_ras(json_payload)

            send_topic = "Micropolis/"+str(topic)+ "/"+str(_id)
            connect_and_send_ras(str(send_topic), json_payload)

            send_topic2 = "Micropolis/"+str(topic)+ "/"+str(_id)+"/status"
            connect_and_send_ras(str(send_topic2), str(_status))

            send_mqtt_to_rasberrypi('Micropolis/door_sensor/9985/status',str(status))

        elif message.topic == "Micropolis/panic_sensor" :
            payload = str(message.payload.decode("utf-8")).strip()
            if payload == "Alarm_ON":
                _id = str(uuid.uuid4())
                list_of_sensors = ["00123"]
                json_payload_dictionary = {"id": _id, "sensors": list_of_sensors}
                json_payload = json.dumps(json_payload_dictionary)
                connect_and_send_alarm(json_payload)

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
            json_payload_dictionary = {"serial_number": _id, "battery": battery, "state": _status, "online": online}
            json_payload = json.dumps(json_payload_dictionary)
            connect_and_send_ras(json_payload)
            send_mqtt_to_rasberrypi('Micropolis/Siren/1221/status',str(status))

            send_topic = "Micropolis/" + str(topic) + "/" + str(_id)
            connect_and_send_ras(str(send_topic), json_payload)

            send_topic2 = "Micropolis/" + str(topic) + "/" + str(_id) + "/status"
            connect_and_send_ras(str(send_topic2), str(_status))

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
            connect_and_send_ras(json_payload)
            send_mqtt_to_rasberrypi('Micropolis/switch/1221/status', str(status))

            send_topic = "Micropolis/" + str(topic) + "/" + str(_id)
            connect_and_send_ras(str(send_topic), json_payload)

            send_topic2 = "Micropolis/" + str(topic) + "/" + str(_id) + "/status"
            connect_and_send_ras(str(send_topic2), str(_status))

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
            connect_and_send_ras(json_payload)
            import datetime
            e = datetime.datetime.now()
            send_mqtt_to_rasberrypi('Micropolis/motion_sensor/1231l/status',str(status)+"\n"+str(e.strftime("%Y-%m-%d %H:%M:%S")))

            send_topic = "Micropolis/" + str(topic) + "/" + str(_id)
            connect_and_send_ras(str(send_topic), json_payload)

            send_topic2 = "Micropolis/" + str(topic) + "/" + str(_id) + "/status"
            connect_and_send_ras(str(send_topic2), str(_status))

        elif str (message.topic).startswith("Micropolis/0/") :
            topic = "Micropolis/switch"
            status = "non"
            id = str(message.topic).split('/')[2]
            if str(message.payload) == "1" :
                status ="on"
            else:
                status = "off"
            payload = '{id:'+str(id)+',status:'+status+'}'
            connect_and_send_ras(topic, payload)
        elif str (message.topic).startswith("Micropolis/1/") :
            topic = "Micropolis/Siren"
            status = "non"
            id = str(message.topic).split('/')[2]
            if str(message.payload) == "1" :
                status ="on"
            else:
                status = "off"
            payload = '{id:'+str(id)+',status:'+status+'}'
            connect_and_send_ras(topic, payload)


    except :
        pass



client.on_message = on_message

while 1 :
    time.sleep(30)