import mysql.connector
from mysql.connector import Error

"""
host='localhost',
database='gateway',
user='root',
password='0000',
port='9999'
"""


class Database :

    def __init__(self,host,port,username,password,database_name):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database_name = database_name
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                 database=self.database_name,
                                                 user=self.username,
                                                 password=self.password,
                                                 port=self.port
                                                 )
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                print(record)
                cursor.close()

        except Error as e:
            print("Error while connecting to MySQL", e)

    def disconnect(self):

            if self.connection.is_connected():
                self.connection.close()
                print("MySQL connection is closed")

    def insert_new_sensor(self,sensorid,cp,name):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO sensors(sensorid,cp,name) VALUES (%s,%s,%s)"""
            records_to_insert = (sensorid,cp,name)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_new_actuator(self,actuatorid ,cp,name):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO actuators(actuatorid ,cp,name) VALUES (%s,%s,%s)"""
            records_to_insert = (actuatorid ,cp,name)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_temperature_sensor_reading(self,sensorid,temp,hum,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO temperature_sensor(sensorid,temperature,humidty,date_time) VALUES (%s,%s,%s,%s)"""
            records_to_insert = (sensorid,temp,hum,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_door_sensor_reading(self,sensorid,status,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO door_sensor(sensorid,door_status,date_time) VALUES (%s,%s,%s)"""
            records_to_insert = (sensorid,status,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_smoke_sensor_reading(self,sensorid,status,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO smoke_sensor(sensorid,fire_status,date_time) VALUES (%s,%s,%s)"""
            records_to_insert = (sensorid,status,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error
    def insert_glass_sensor_reading(self,sensorid,status,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO glass_sensor(sensorid,glass_status,date_time) VALUES (%s,%s,%s)"""
            records_to_insert = (sensorid,status,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error
    def insert_motion_sensor_reading(self,sensorid,status,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO motion_sensor(sensorid,motion_status,date_time) VALUES (%s,%s,%s)"""
            records_to_insert = (sensorid,status,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error
    def insert_polution_sensor_reading(self,sensorid,polution,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO polution_sensor(sensorid,polution,date_time) VALUES (%s,%s,%s)"""
            records_to_insert = (sensorid,polution,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error
    def insert_power_reading(self,power,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO power(power,date_time) VALUES (%s,%s)"""
            records_to_insert = (power,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error
    def insert_relay_switch_reading(self,actuatorid,status,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO relay_switch(actuatorid,status,datetime) VALUES (%s,%s,%s)"""
            records_to_insert = (actuatorid,status,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error

    def insert_siren_reading(self,actuatorid,status,datetime):
        try:
            cursor = self.connection.cursor()
            command = """INSERT INTO siren(actuatorid,status,datetime) VALUES (%s,%s,%s)"""
            records_to_insert = (actuatorid,status,datetime)
            cursor.execute(command, records_to_insert)
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return error