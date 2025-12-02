import paho.mqtt.client as mqtt
import time
import random
import os

# Конфигурация MQTT
MQTT_BROKER = os.getenv('MQTT_BROKER', 'mosquitto')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'factory/sensor/temperature')

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker: {MQTT_BROKER}")
    else:
        print(f"Failed to connect, return code {rc}")

# Создание MQTT клиента
client = mqtt.Client("TemperatureSensor")
client.on_connect = on_connect

# Подключение к брокеру
try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
except Exception as e:
    print(f"Connection error: {e}")
    exit(1)

print(f"Temperature Sensor started. Publishing to topic: {MQTT_TOPIC}")

# Генерация и отправка данных
try:
    while True:
        # Генерация случайной температуры (60-100°C)
        temperature = random.uniform(60, 100)
        
        # Публикация в MQTT топик
        client.publish(MQTT_TOPIC, f"{temperature:.2f}")
        print(f"Published: {temperature:.2f}°C")
        
        # Пауза 1 секунда
        time.sleep(1)
except KeyboardInterrupt:
    print("\nSensor stopped")
    client.loop_stop()
    client.disconnect()
