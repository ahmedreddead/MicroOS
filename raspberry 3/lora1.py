import os, sys
from LoRaRF import SX126x
import time
from datetime import datetime
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
class Lora:

    def __init__(self):
        self.resetPin = 0
        self.busyPin = 13
        self.irqPin = -1
        self.txenPin = 6
        self.rxenPin = 5
        self.busId = 0
        self.csId = 0
        self.LoRa = None
        #self.database = Database()
    def connect(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT)
        GPIO.output(26, GPIO.HIGH)
        self.LoRa = SX126x()
        self.LoRa.begin(self.busId , self.csId , self.resetPin , self.busyPin , self.irqPin , self.txenPin , self.rxenPin )
        self.LoRa.setDio3TcxoCtrl(self.LoRa.DIO3_OUTPUT_1_8, self.LoRa.TCXO_DELAY_10)
        self.LoRa.setFrequency(915000000)
        print("Set frequency to 915 Mhz")
        self.LoRa.setRxGain(self.LoRa.RX_GAIN_POWER_SAVING)
        sf = 7
        bw = 125000
        cr = 5
        self.LoRa.setLoRaModulation(sf, bw, cr)
        print("Set modulation parameters:\n\tSpreading factor = 12\n\tBandwidth = 125 kHz\n\tCoding rate = 4/5")
        headerType = self.LoRa.HEADER_EXPLICIT
        preambleLength = 8
        payloadLength = 38
        crcType = False
        self.LoRa.setLoRaPacket(headerType, preambleLength, payloadLength, crcType)
        print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 8\n\tPayload Length = 6\n\tCRC off")
        # Set syncronize word for public network (0x3444)
        self.LoRa.setSyncWord(0x3424)
        print("Set syncronize word to 0x3424")

    def receive(self):

        while True:
            # Request for receiving new LoRa packet
            self.LoRa.request()
            # Wait for incoming LoRa packet
            self.LoRa.wait()

            # Put received packet to message and counter variable
            # read() and available() method must be called after request() or listen() method
            message = ""
            # available() method return remaining received payload length and will decrement each read() or get() method called
            while self.LoRa.available() >= 1:
                message += chr(self.LoRa.read())
            counter = self.LoRa.read()

            # Print received message and counter in serial
            print(f"{message}  {counter}")
            cp ='lora'

            try:
                mqttBroker = "localhost"
                port = 1883
                client = mqtt.Client("Hub_lora1")
                client.connect(mqttBroker,port)
                topic_sensor_state = "Micropolis/motion_sensor"


                client.publish(topic_sensor_state, str(message))

            except :
                print("cant send to mqtt ")
                pass
            





            # Print packet/signal status including RSSI, SNR, and signalRSSI
            print("Packet status: RSSI = {0:0.2f} dBm | SNR = {1:0.2f} dB".format(self.LoRa.packetRssi(), self.LoRa.snr()))

            # Show received status in case CRC or header error occur
            status = self.LoRa.status()
            if status == self.LoRa.STATUS_CRC_ERR:
                print("CRC error")
            elif status == self.LoRa.STATUS_HEADER_ERR:
                print("Packet header error")






objectlora = Lora()
objectlora.connect()
objectlora.receive()




