import paho.mqtt.client as mqtt
import os
from datetime import datetime

# Конфигурация MQTT
MQTT_BROKER = os.getenv('MQTT_BROKER', 'mosquitto')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'cloud/alerts/temperature')

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Cloud Monitor connected to MQTT Broker: {MQTT_BROKER}")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic: {MQTT_TOPIC}")
        print("=" * 60)
        print("Waiting for critical alerts (Temperature > 80°C)...")
        print("=" * 60)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperature = float(msg.payload.decode())
    print(f"[{timestamp}] 🚨 ALERT! Temperature: {temperature:.2f}°C")

# Создание MQTT клиента
client = mqtt.Client("CloudMonitor")
client.on_connect = on_connect
client.on_message = on_message

# Подключение к брокеру
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("\nCloud Monitor stopped")
    client.disconnect()
except Exception as e:
    print(f"Connection error: {e}")
    exit(1)
