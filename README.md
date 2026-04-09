# 🎫 HelpDesk DevOps — Full CI/CD Project

A microservices helpdesk app demonstrating the complete DevOps lifecycle:
**Code → Build → Test → Scan → Push → Deploy → Monitor**

---

## 🏗️ Architecture

```
GitHub Push
    │
    ▼
GitHub Actions / Jenkins
    ├── Unit Tests (pytest)
    ├── Docker Build (multi-stage)
    ├── Trivy Scan (CRITICAL CVE check)
    ├── SonarQube (static analysis)
    └── Push to DockerHub
              │
              ▼
         ArgoCD watches manifests/
              │
              ▼
    DigitalOcean K8s Cluster
    ├── auth-service   (port 8001) ← JWT Login
    ├── ticket-service (port 8002)
    ├── comment-service(port 8003)
    ├── frontend       (port 3000)
    └── MongoDB        (port 27017, PVC)
              │
              ▼
    Prometheus + Grafana (monitoring/)
```

---

## 🔒 JWT Authentication Flow

1. User POSTs `/login` with username + password
2. Auth service validates credentials, returns **JWT token**
3. Frontend stores token in `localStorage`
4. All API calls send `Authorization: Bearer <token>` header
5. Token expires after 24 hours → user is logged out

---

## 🚀 Quick Start (Local)

```bash
# 1. Clone and setup
git clone https://github.com/SaranyaDevi2005/helpdesk-devops
cd helpdesk-devops
cp .env.example .env
# Edit .env with your values

# 2. Run everything
docker-compose up --build

# 3. Open browser
# Frontend: http://localhost:3000
# Auth API: http://localhost:8001/docs
# Ticket API: http://localhost:8002/docs
```

---

## ☁️ Cloud Deployment

```bash
# Step 1 — Provision K8s cluster (DigitalOcean)
cd terraform
export TF_VAR_do_token="your_do_token"
terraform init && terraform apply

# Step 2 — Install ArgoCD
export KUBECONFIG=./kubeconfig.yaml
cd ../manifests/deployments
bash argocd-install.sh

# Step 3 — Install Prometheus + Grafana
cd ../../monitoring
bash install.sh

# Step 4 — CI pipeline pushes → ArgoCD auto-syncs → Done! ✅
```

---

## 🔐 DevSecOps Tools

| Tool | Purpose | Where |
|------|---------|-------|
| **Trivy** | Container CVE scanning | CI Pipeline |
| **SonarQube/Cloud** | Static code analysis | CI Pipeline |
| **JWT** | Stateless auth tokens | auth-service |
| **K8s Secrets** | Secure env vars | All deployments |
| **OWASP ZAP** | Dynamic web scanning | Optional stage |

---

## 📊 Monitoring

- **Prometheus** scrapes metrics from all pods
- **Grafana** dashboard at `http://<EXTERNAL-IP>` (admin / helpdesk@123)
- **HPA** auto-scales auth and ticket services at 70% CPU

---

## 📁 Project Structure

```
helpdesk-devops/
├── backend/services/
│   ├── auth_service/       # FastAPI + JWT
│   ├── ticket_service/     # FastAPI
│   └── comment_service/    # FastAPI
├── frontend/               # React
├── manifests/              # K8s YAMLs (ArgoCD source of truth)
│   ├── deployments/
│   ├── services/
│   └── argocd-app.yaml
├── terraform/              # DigitalOcean K8s cluster
├── monitoring/             # Prometheus + Grafana Helm values
├── .github/workflows/      # GitHub Actions CI/CD
├── Jenkinsfile             # Jenkins pipeline
├── docker-compose.yml      # Local dev
└── sonar-project.properties
```
