# 🌤️ End-to-End Weather Prediction MLOps Pipeline

![CI/CD Status](https://github.com/ganapriyahs/weather-predictor/actions/workflows/deploy.yaml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-GKE-blue?logo=kubernetes)

## 📖 Project Overview
This project is a full-stack Machine Learning application deployed on **Google Kubernetes Engine (GKE)**. It predicts the weather temperature for the next hour based on real-time data fetched from the Open-Meteo API.

Unlike simple ML scripts, this project demonstrates a complete **MLOps lifecycle**:
1.  **Model Training:** Scikit-Learn Linear Regression pipeline.
2.  **Containerization:** Dockerized application for consistent environments (handling ARM64 vs AMD64 architecture).
3.  **Orchestration:** Managed Kubernetes cluster (GKE Autopilot) with Load Balancing.
4.  **CI/CD:** Automated GitHub Actions pipeline that builds, pushes, and deploys on every commit.
5.  **Observability:** Integrated Prometheus metrics for monitoring application health and latency.

---

## 🏗️ Architecture


**The Flow:**
1.  **User** visits the web interface (FastAPI + HTML/JS).
2.  **Ingress:** Traffic hits the Google Cloud Load Balancer (External IP).
3.  **Service:** Kubernetes routes traffic to the active Pod.
4.  **App:** FastAPI fetches *current* weather data from **Open-Meteo API**.
5.  **Inference:** The trained Linear Regression model (`.pkl`) predicts the *future* temperature.
6.  **Response:** JSON result is returned to the user.


```mermaid
graph TD;
    User([User]) -->|HTTP Request| LB[Google Load Balancer];
    LB -->|Routes Traffic| K8s[GKE Cluster];

    subgraph Kubernetes
        K8s -->|Service| Svc[Weather Service];
        Svc -->|Selects Pod| Pod[App Pod];

        subgraph Pod
            App[FastAPI App];
            Model[("ML Model (.pkl)")]
        end

        App -->|Load| Model;
    end

    App -->|Fetch Data| API[Open-Meteo API];
    API -->|JSON| App;
    App -->|JSON Response| User;

    style User fill:#f9f,stroke:#333,stroke-width:2px
    style LB fill:#bbf,stroke:#333,stroke-width:2px
    style API fill:#ff9,stroke:#333,stroke-width:2px

---

## 🛠️ Tech Stack

* **Language:** Python 3.9
* **Framework:** FastAPI (High-performance web API)
* **ML Library:** Scikit-Learn, Pandas
* **Containerization:** Docker
* **Orchestration:** Google Kubernetes Engine (GKE)
* **CI/CD:** GitHub Actions + Google Artifact Registry
* **Monitoring:** Prometheus Instrumentator

---

## 🚀 Key Features

### 1. **Automated CI/CD Pipeline**
* **Trigger:** Push to `main` branch.
* **Build:** GitHub Actions builds a Docker image (multi-arch `linux/amd64`).
* **Push:** Uploads image to Google Artifact Registry.
* **Deploy:** Updates the Kubernetes deployment using `kubectl rollout`.
* **Zero Downtime:** Rolling updates ensure the app never goes offline during deployment.

### 2. **Real-Time ML Inference**
* Fetches live weather data dynamically.
* Uses a serialized model (`weather_model.pkl`) to generate predictions instantly.

### 3. **Production-Grade Monitoring**
* Exposes a `/metrics` endpoint for Prometheus.
* Tracks Request Count, Latency, and Error Rates.
* Tracks Python Garbage Collection and Memory Usage.

---

## 📂 Project Structure

```bash
├── .github/workflows/   # CI/CD Pipeline definition (YAML)
├── app/
│   ├── main.py          # FastAPI application entry point
│   ├── model.py         # ML Inference logic
│   ├── weather_client.py# External API handler
│   ├── static/          # Frontend (HTML/CSS/JS)
│   └── weather_model.pkl# Trained ML Model
├── k8s/                 # Kubernetes Manifests
│   ├── deployment.yaml  # Pod & ReplicaSet configuration
│   └── service.yaml     # LoadBalancer configuration
├── Dockerfile           # Container definition
├── train_model.py       # Script to fetch data and retrain model
└── requirements.txt     # Python dependencies


⚡ How to Run Locally

Clone the repository:

Bash
git clone [https://github.com/ganapriyahs/weather-predictor.git](https://github.com/ganapriyahs/weather-predictor.git)
cd weather-predictor
Install dependencies:

Bash
pip install -r requirements.txt
Run the application:

Bash
uvicorn app.main:app --reload
Access the App:
Open http://127.0.0.1:8000 in your browser.

☁️ Deployment (Manual)
Note: Deployment is handled automatically by GitHub Actions, but here are the manual steps.

Build & Push Docker Image:

Bash
docker build --platform linux/amd64 -t gcr.io/PROJECT_ID/weather-app:v1 .
docker push gcr.io/PROJECT_ID/weather-app:v1
Deploy to GKE:

Bash
kubectl apply -f k8s/
Check Status:

Bash
kubectl get services
# Copy EXTERNAL-IP and visit in browser

📈 Future Improvements
Database Integration: Store historical predictions in PostgreSQL/BigQuery to analyze model drift.

Advanced Model: Switch from Linear Regression to LSTM (Long Short-Term Memory) for time-series forecasting.

HTTPS/SSL: Configure a managed certificate for secure access.

Grafana Dashboard: Visualize the Prometheus metrics.
