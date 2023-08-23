import paho.mqtt.client as mqtt

broker_address = "3.19.148.223"
topic = "servo"

client = mqtt.Client("raspberry-pub")
client.connect(broker_address)

message = "90"
client.publish(topic, message)
