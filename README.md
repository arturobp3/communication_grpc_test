# gRPC Services Communication Project with Kubernetes

This project demonstrates how to create two services that communicate using gRPC, package them with Docker, deploy them on Kubernetes (using Minikube), and test their integration. `servicio_a` acts as a gRPC client that connects to `servicio_b`.

---

## 📦 Project Structure

```
communication_grpc_test/
├── servicio_a/
│   ├── server.py
│   ├── client.py
│   ├── saludo_personalizado.proto
│   ├── saludo_personalizado_pb2.py
│   ├── saludo_personalizado_pb2_grpc.py
│   ├── saludo_base_pb2.py
│   ├── saludo_base_pb2_grpc.py
│   ├── requirements.txt
│   └── Dockerfile
├── servicio_b/
│   ├── server.py
│   ├── saludo_base.proto
│   ├── saludo_base_pb2.py
│   ├── saludo_base_pb2_grpc.py
│   ├── requirements.txt
│   └── Dockerfile
├── k8s/
│   ├── servicio-a-deployment.yaml
│   ├── servicio-a-service.yaml
│   ├── servicio-b-deployment.yaml
│   └── servicio-b-service.yaml
```

---

## 🚀 Requirements

- Python 3.10+
- Docker and Docker Desktop
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- `grpcio`, `grpcio-tools`, `protobuf`

---

## 🧰 Steps to run it from scratch

### 1. Generate `.proto` files for each service

```bash
# From the project root
python -m grpc_tools.protoc -I./protos --python_out=./servicio_a --grpc_python_out=./servicio_a ./protos/saludo_personalizado.proto
python -m grpc_tools.protoc -I./protos --python_out=./servicio_b --grpc_python_out=./servicio_b ./protos/saludo_base.proto
```

If `servicio_a` depends on `servicio_b`'s proto, also copy:

```bash
cp ./servicio_b/saludo_base_pb2*.py ./servicio_a/
```

---

### 2. Build Docker images

```bash
minikube start
minikube image build -t servicio-b:latest ./servicio_b
minikube image build -t servicio-a:latest ./servicio_a
```

---

### 3. Deploy to Kubernetes

```bash
kubectl apply -f k8s/servicio-b-deployment.yaml
kubectl apply -f k8s/servicio-b-service.yaml
kubectl apply -f k8s/servicio-a-deployment.yaml
kubectl apply -f k8s/servicio-a-service.yaml
```

---

### 4. Check pod status

```bash
kubectl get pods
```

Make sure both are in `Running` state.

---

### 5. Expose `servicio-a` for testing

```bash
minikube service servicio-a --url
```

This will return a URL like `http://127.0.0.1:65053`. Use that IP and port in your client.

---

### 6. Run the local client

```bash
python servicio_a/client.py
```

---

## 🛠️ Useful Debugging

- View service logs:
  ```bash
  kubectl logs -l app=servicio-a
  kubectl logs -l app=servicio-b
  ```

- Restart a deployment:
  ```bash
  kubectl rollout restart deployment servicio-a
  ```

- Access a container:
  ```bash
  kubectl exec -it <pod-name> -- sh
  ```

- Test inter-service connectivity:
  ```bash
  kubectl run tester --rm -i --tty --image=busybox -- /bin/sh
  nc -vz servicio-b 50052
  ```

---

## ✅ Expected Output

```txt
What's your name? Arturo
Server response: Hello, Arturo, hope you have a great day
```

And in `servicio-b` logs:

```
[B] Received name: Arturo
```

---

## 🧑‍💻 Author

Arturo