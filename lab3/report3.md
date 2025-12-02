# Отчет по лабораторной работе №3

## 1. Запуск инфраструктуры

```bash
docker compose up -d --build
```

```bash
docker ps --filter "network=lab3_factory-net"
```

## 2. Настройка Node-RED

picture

## 3. Тестирование

### 3.1 Мониторинг датчика

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

### 3.2 Мониторинг всех показаний

```bash
docker exec mosquitto mosquitto_sub -h localhost -t "factory/sensor/temperature" -C 10
```

### 3.3 Мониторинг облачных алертов

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

## 4. Команды для быстрого запуска

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
