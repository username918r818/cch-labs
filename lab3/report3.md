# Отчет по лабораторной работе №3

## 1. Создание файлов

Файл `sensor.py`:

```python
import paho.mqtt.client as mqtt
import time
import random
import os

MQTT_BROKER = os.getenv('MQTT_BROKER', 'mosquitto')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'factory/sensor/temperature')

client = mqtt.Client("TemperatureSensor")
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

while True:
    temperature = random.uniform(60, 100)
    client.publish(MQTT_TOPIC, f"{temperature:.2f}")
    print(f"Published: {temperature:.2f}°C")
    time.sleep(1)
```

Файл `cloud_monitor.py`:

```python
import paho.mqtt.client as mqtt
from datetime import datetime

def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperature = float(msg.payload.decode())
    print(f"[{timestamp}] ALERT! Temperature: {temperature:.2f}°C")

client = mqtt.Client("CloudMonitor")
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe("cloud/alerts/temperature")
client.loop_forever()
```

## 2. Запуск инфраструктуры

```bash
docker compose up -d --build
```

```bash
docker ps --filter "network=lab3_factory-net"
```

## 3. Настройка Node-RED

```bash
открыть http://localhost:1880
```

Импорт flow:

1. Открыть меню → Import
2. Вставить содержимое `nodered-flow.json`
3. Deploy

## 4. Тестирование

### 4.1 Мониторинг датчика

```bash
docker logs sensor --tail 10
```

```log
Published: 79.93°C
Published: 93.02°C
Published: 90.48°C
Published: 98.90°C
Published: 80.71°C
```

### 4.2 Мониторинг всех показаний

```bash
docker exec mosquitto mosquitto_sub -h localhost -t "factory/sensor/temperature" -C 10
```

### 4.3 Мониторинг облачных алертов

```bash
docker logs cloud -f
```

```log
[2025-12-02 17:31:38] ALERT! Temperature: 92.26°C
[2025-12-02 17:31:42] ALERT! Temperature: 93.02°C
[2025-12-02 17:31:43] ALERT! Temperature: 90.48°C
[2025-12-02 17:31:44] ALERT! Temperature: 98.90°C
[2025-12-02 17:31:45] ALERT! Temperature: 80.71°C
```

## 5. Команды для быстрого запуска

```bash
docker compose up -d --build
docker compose down
docker compose logs -f
docker logs sensor -f
docker logs cloud -f
docker exec mosquitto mosquitto_sub -h localhost -t "factory/sensor/temperature"
docker exec mosquitto mosquitto_sub -h localhost -t "cloud/alerts/temperature"
docker exec mosquitto mosquitto_pub -h localhost -t "factory/sensor/temperature" -m "95.5"
docker network inspect lab3_factory-net
```
