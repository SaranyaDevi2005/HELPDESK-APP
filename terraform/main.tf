# ── Provider ──────────────────────────────────────────────────
terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = var.do_token
}

# ── Kubernetes Cluster ────────────────────────────────────────
resource "digitalocean_kubernetes_cluster" "helpdesk" {
  name    = "helpdesk-cluster"
  region  = "blr1"           # Bangalore — closest to Tamil Nadu
  version = "1.29.1-do.0"

  node_pool {
    name       = "default-pool"
    size       = "s-2vcpu-4gb"  # 2 CPU, 4GB RAM — small and cheap
    node_count = 2
    auto_scale = true
    min_nodes  = 1
    max_nodes  = 3
  }

  tags = ["helpdesk", "devops"]
}

# ── Save kubeconfig ───────────────────────────────────────────
resource "local_file" "kubeconfig" {
  content  = digitalocean_kubernetes_cluster.helpdesk.kube_config[0].raw_config
  filename = "${path.module}/kubeconfig.yaml"
}

output "cluster_endpoint" {
  value = digitalocean_kubernetes_cluster.helpdesk.endpoint
}
