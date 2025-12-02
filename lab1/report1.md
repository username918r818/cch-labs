# Отчет по лабораторной работе №1

## 1. Контейнеризация приложения

- Создан файл `app.py` — простое веб-приложение, имитирующее интернет-магазин
- Создан `Dockerfile` для контейнеризации приложения

## 2. Docker Compose

- Создан файл `docker-compose.yml` для локального запуска связки приложения и Redis

### 2.2 Запуск и тестирование

```bash
docker compose up -d --build
```

## 3. Инициализация Docker Swarm

### 3.1 Переключение в режим Swarm

```bash
docker swarm init --advertise-addr 172.30.163.36
```

### 3.2 Создание docker-stack.yml

Файл `docker-stack.yml` с конфигурацией для Swarm mode

### 3.3 Развертывание стека

```bash
docker stack deploy -c docker-stack.yml shop
```

## 4. Тест на отказ (Self-Healing)

```bash
docker ps --filter "name=shop_frontend"
```

```log
CONTAINER ID   NAMES
23e34c5bec59   shop_frontend.1.0md2dfehm5clrizwx0qhmuu8j
```

```bash
docker kill 23e34c5bec59
```

### 4.3 Наблюдение за восстановлением

```bash
docker service ps shop_frontend
```

## 5. Масштабирование сервиса

### 5.1 Увеличение количества реплик

```bash
docker service scale shop_frontend=5
```

### 5.2 Проверка запущенных реплик

```bash
docker service ps shop_frontend
```

**Результат:**

```log
ID             NAME              IMAGE                  NODE      DESIRED STATE   CURRENT STATE
p02z7kdputcd   shop_frontend.1   lab1-frontend:latest   omni      Running         Running 37 seconds ago
xf3tsd00xeoy   shop_frontend.2   lab1-frontend:latest   omni      Running         Running 8 seconds ago
kodqj9z98pj2   shop_frontend.3   lab1-frontend:latest   omni      Running         Running 8 seconds ago
sepullafpgqi   shop_frontend.4   lab1-frontend:latest   omni      Running         Running 8 seconds ago
p6uuk4503ze2   shop_frontend.5   lab1-frontend:latest   omni      Running         Running 8 seconds ago
```

### 5.3 Проверка контейнеров

```bash
docker ps --filter "name=shop_frontend"
```

## 10. Команды для быстрого запуска

```bash
# Локальный запуск с Docker Compose
docker compose up -d --build

# Инициализация Swarm
docker swarm init --advertise-addr <IP>

# Развертывание стека
docker stack deploy -c docker-stack.yml shop

# Масштабирование
docker service scale shop_frontend=5

# Просмотр логов
docker service logs shop_frontend

# Удаление стека
docker stack rm shop

# Выход из режима Swarm
docker swarm leave --force

curl http://172.30.163.36:5000
```
