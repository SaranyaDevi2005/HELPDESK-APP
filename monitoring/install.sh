#!/bin/bash
# Run this after terraform apply + ArgoCD setup

echo "📊 Installing Prometheus + Grafana..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace \
  -f prometheus-values.yaml

echo ""
echo "✅ Done! Wait ~2 min then:"
echo "kubectl get svc -n monitoring | grep grafana"
echo "Access Grafana at the EXTERNAL-IP, login: admin / helpdesk@123"
