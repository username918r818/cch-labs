# Отчет по лабораторной работе №2

## 1. Установка Minikube и kubectl

### 1.1 Установка Minikube

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
rm minikube-linux-amd64
```

### 1.2 Установка kubectl

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm kubectl
```

### 1.3 Запуск Minikube

```bash
minikube start --driver=docker
```

## 2. Подготовка образа для Kubernetes

### 2.1 Копирование файлов приложения

```bash
cp ../lab1/{app.py,requirements.txt,Dockerfile} ./
```

### 2.2 Сборка образа в окружении Minikube

```bash
eval $(minikube docker-env)
docker build -t shop-frontend:v1 .
docker pull redis:7-alpine
```

## 4. Развертывание приложения

```bash
kubectl apply -f .
```

### 4.2 Проверка статуса

```bash
kubectl get all
```

## 5. Доступ к приложению

### 5.1 Через Minikube Service

```bash
minikube service frontend --url
```

### 5.2 Через Port Forwarding

```bash
kubectl port-forward service/frontend 8080:5000
```

## 6. Rolling Update

### 6.1 Изменение приложения

В `app.py` изменим текст заголовка:

```python
<title>Интернет-магазин2</title>
```

### 6.2 Сборка новой версии образа

```bash
eval $(minikube docker-env)
docker build -t shop-frontend:v2 .
```

### 6.3 Обновление Deployment

Изменим образ в `frontend-deployment.yaml`:

```yaml
image: shop-frontend:v2
```

Применим изменения:

```bash
kubectl apply -f frontend-deployment.yaml
```

### 6.4 Наблюдение за Rolling Update

```bash
kubectl rollout status deployment/frontend
```

### 6.5 Проверка истории деплоя

```bash
kubectl rollout history deployment/frontend
```

### 6.6 Откат к предыдущей версии (если нужно)

```bash
kubectl rollout undo deployment/frontend
```

## 7. Полезные команды

```bash
kubectl get all

kubectl describe pod <pod-name>

kubectl logs <pod-name>

kubectl exec -it <pod-name> -- /bin/sh

kubectl port-forward service/frontend 8080:5000

kubectl scale deployment frontend --replicas=5

kubectl delete -f .

kubectl rollout status deployment/frontend

kubectl rollout undo deployment/frontend

minikube stop

minikube delete

unset DOCKER_HOST DOCKER_TLS_VERIFY DOCKER_CERT_PATH MINIKUBE_ACTIVE_DOCKERD
```
