# URL Checker - Prometheus Exporter

This project is a simple Python application that checks the availability and response time of two external URLs, and exposes the results as Prometheus metrics via HTTP.

---

## Features

- Periodically checks:
  - https://httpstat.us/503
  - https://httpstat.us/200
- Reports two metrics for each URL:
  - `sample_external_url_up` (1 = up, 0 = down)
  - `sample_external_url_response_ms` (response time in milliseconds)
- Exposes metrics in Prometheus format at `/metrics`
- Containerized with Docker
- Deployable to Kubernetes using Helm

---

## Requirements

- Python 3.11+
- Docker (Docker Desktop)
- Helm 3+
- Kubernetes cluster (Docker Desktop)

---

## Running Locally

1. Clone the repository:
```bash
git clone https://github.com/tsvetananev1/url-checker.git
cd url-checker
```
2. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Run the application:
```bash
python main.py
```
4. Access metrics:
http://localhost:8000/metrics

## Docker Usage

1. Build the Docker image:
```bash
docker build -t url-checker .
```
2. Run the container:
```bash
docker run -p 8000:8000 url-checker
```
3. Access metrics:
http://localhost:8000/metrics

## Kubernetes Deployment with Helm

For Kubernetes deployment, we are using **Docker Desktop's built-in Kubernetes cluster**.  
Docker Desktop makes it easy to enable a local single-node Kubernetes cluster without needing to install Minikube or other external tools.  
It is ideal for local development, testing, and demos.

---

### Setting up Kubernetes with Docker Desktop

Before proceeding with the deployment, ensure that Kubernetes is enabled and correctly configured.

1. Open **Docker Desktop**.
2. Go to **Settings > Kubernetes**.
3. Check **Enable Kubernetes**.
4. Click **Apply & Restart**.

After Kubernetes is enabled, check that your `kubectl` is connected to the local cluster:
```bash
kubectl config current-context
```
It should return:
```bash
docker-desktop
```
If not, switch the context manually:
```bash
kubectl config use-context docker-desktop
```
Verify that the node is ready:
```bash
kubectl get nodes
```
You should see:
```bash
NAME             STATUS   ROLES           AGE   VERSION
docker-desktop   Ready    control-plane   1m    v1.xx.x
```

### Difference between `helm create` and `helm install` 
- `create` ➔ for **generating** a Helm chart structure  
- `install` ➔ for **deploying** a Helm chart into Kubernetes

---

1. Create the Helm chart:
```bash
helm create url-checker-chart
```
2. Log in to Docker Hub:
```bash
docker login
```
Authenticate to your Docker Hub account.

3. Tag and Push your Docker image:
```bash
docker tag url-checker tsvetananev/url-checker
docker push tsvetananev/url-checker
```
This uploads your local Docker image to Docker Hub so that Kubernetes can pull it.

4. Install the Helm chart:
```bash
helm install url-checker ./url-checker-chart
```
This deploys the application into the Kubernetes cluster.

5. Verify the service:
```bash
kubectl get svc
```
Check the created service and ensure it's running and exposes port 8000.

6. Port-forward to access the service locally:
```bash
kubectl port-forward svc/url-checker-url-checker-chart 8000:8000
```
Expose the service on your local machine on port 8000.

7. Access the metrics endpoint:
http://localhost:8000/metrics

You should see the Prometheus metrics for the monitored URLs.

## Metrics Example
sample_external_url_up{url="https://httpstat.us/503"} 0.0

sample_external_url_up{url="https://httpstat.us/200"} 1.0

sample_external_url_response_ms{url="https://httpstat.us/503"} 690.8538341522217

sample_external_url_response_ms{url="https://httpstat.us/200"} 639.2319202423096

## Useful References

(Prometheus Client Python)
https://github.com/prometheus/client_python

(Helm Docs)
https://helm.sh/docs/

(Docker Documentation)
https://docs.docker.com