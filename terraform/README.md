# Terraform — DigitalOcean K8s Cluster

## Quick Start

```bash
# 1. Set your DigitalOcean token
export TF_VAR_do_token="your_do_token_here"

# 2. Init and apply
terraform init
terraform plan
terraform apply

# 3. Use the cluster
export KUBECONFIG=./kubeconfig.yaml
kubectl get nodes
```

## After cluster is ready

```bash
# Install ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Apply ArgoCD app (points to your GitHub manifests/)
kubectl apply -f ../manifests/argocd-app.yaml

# Get ArgoCD admin password
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```
