import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    if rc == 0:
        print(f"Is client connected: {client.is_connected()}")
        print(f"message: {message}, topic: {topic}")
        # publish message
        client.publish(topic, message)
        
        # subscribe to a topic
        client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f"message: {msg.payload.decode()}, topic: {msg.topic}")

def on_error(client, userdata, rc):
    print(f"Error: {rc}")
    exit(1)

# Define MQTT parameters
broker_address = "test.mosquitto.org"
topic = "light"
message = "test message"

# Create an MQTT client instance
client = mqtt.Client()

# Assign callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_error = on_error

# Connect to the broker
client.connect(broker_address, 1883, 60)

# Start the loop
client.loop_start()

# # Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Disconnected")
    client.disconnect()
    client.loop_stop()
