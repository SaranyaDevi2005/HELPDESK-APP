# ── Terraform config — for DEMO/VIVA use "terraform plan" only ──
# No card needed for "terraform plan" — it just previews what would be created.
# If you want to actually deploy, add a DigitalOcean API token.

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

# ── Kubernetes Cluster (2-node, Bangalore region) ─────────────
resource "digitalocean_kubernetes_cluster" "helpdesk" {
  name    = "helpdesk-cluster"
  region  = "blr1"
  version = "1.29.1-do.0"

  node_pool {
    name       = "default-pool"
    size       = "s-2vcpu-4gb"
    node_count = 2
    auto_scale = true
    min_nodes  = 1
    max_nodes  = 3
  }

  tags = ["helpdesk", "devops"]
}

resource "local_file" "kubeconfig" {
  content  = digitalocean_kubernetes_cluster.helpdesk.kube_config[0].raw_config
  filename = "${path.module}/kubeconfig.yaml"
}

output "cluster_endpoint" {
  value = digitalocean_kubernetes_cluster.helpdesk.endpoint
}
