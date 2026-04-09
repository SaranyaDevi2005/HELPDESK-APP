#!/bin/bash
# Run once after: terraform apply

echo "1️⃣  Installing ArgoCD..."
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo "⏳ Waiting for ArgoCD pods..."
kubectl wait --for=condition=available --timeout=120s deployment/argocd-server -n argocd

echo "2️⃣  Exposing ArgoCD UI..."
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'

echo "3️⃣  Applying Helpdesk app..."
kubectl apply -f ../argocd-app.yaml

echo ""
echo "✅ ArgoCD installed! Get admin password with:"
echo "   kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d"
echo ""
echo "   ArgoCD will now auto-sync manifests/ from GitHub 🚀"
