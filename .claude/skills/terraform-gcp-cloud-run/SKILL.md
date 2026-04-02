---
name: terraform-gcp-cloud-run
description: Terraform patterns for GCP Cloud Run, Cloud SQL, Cloud Storage, IAM, and state management. Use when provisioning GCP infrastructure, deploying containers to Cloud Run, or managing Terraform modules for Google Cloud.
---

# Terraform GCP Cloud Run Infrastructure

Production Terraform patterns for deploying FastAPI services to GCP Cloud Run with Cloud SQL, IAM, and security hardening.

## When to Apply

- Deploying containerized services to Cloud Run
- Provisioning Cloud SQL PostgreSQL instances
- Configuring IAM service accounts with least privilege
- Setting up Terraform state management on GCS
- Migrating from homelab Docker to GCP production

## Critical Rules

**Always use remote state**: Never store Terraform state locally

```hcl
# backend.tf
terraform {
  backend "gcs" {
    bucket = "my-project-terraform-state"
    prefix = "prod"
  }
}
```

**Least-privilege IAM**: Never use default compute service account

```hcl
# WRONG - default service account with editor role
resource "google_cloud_run_service" "api" {
  template {
    spec {
      # Uses default compute SA with broad permissions
    }
  }
}

# RIGHT - dedicated SA with minimal permissions
resource "google_service_account" "cloud_run_sa" {
  account_id   = "cloud-run-api"
  display_name = "Cloud Run API Service Account"
}

resource "google_project_iam_member" "cloud_sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}
```

## Key Patterns

### Cloud Run Service with Cloud SQL

```hcl
module "cloud_run" {
  source  = "GoogleCloudPlatform/cloud-run/google"
  version = "~> 0.21"

  service_name = var.service_name
  project_id   = var.project_id
  location     = var.region
  image        = "${var.region}-docker.pkg.dev/${var.project_id}/${var.repo_name}/${var.image_name}:${var.image_tag}"

  service_account_email = google_service_account.cloud_run_sa.email

  limits = {
    cpu    = "1000m"
    memory = "512Mi"
  }

  template_annotations = {
    "autoscaling.knative.dev/minScale"      = var.min_instances
    "autoscaling.knative.dev/maxScale"      = var.max_instances
    "run.googleapis.com/cloudsql-instances"  = google_sql_database_instance.main.connection_name
    "run.googleapis.com/startup-cpu-boost"   = "true"
  }

  env_vars = [
    { name = "ENVIRONMENT", value = var.environment },
    { name = "GCP_PROJECT", value = var.project_id },
  ]

  env_secret_vars = [
    {
      name = "DATABASE_URL"
      value_from = [{
        secret_key_ref = {
          name = google_secret_manager_secret.db_url.secret_id
          key  = "latest"
        }
      }]
    },
  ]
}
```

### Cloud SQL PostgreSQL Instance

```hcl
resource "google_sql_database_instance" "main" {
  name             = "${var.project_name}-db-${var.environment}"
  database_version = "POSTGRES_16"
  region           = var.region
  project          = var.project_id

  settings {
    tier              = var.db_tier  # "db-f1-micro" for dev, "db-custom-2-4096" for prod
    availability_type = var.environment == "prod" ? "REGIONAL" : "ZONAL"
    disk_size         = var.db_disk_size
    disk_autoresize   = true

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = var.environment == "prod"
      start_time                     = "03:00"
      transaction_log_retention_days = 7

      backup_retention_settings {
        retained_backups = 30
      }
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
    }

    database_flags {
      name  = "log_checkpoints"
      value = "on"
    }
  }

  deletion_protection = var.environment == "prod"
}

resource "google_sql_database" "app" {
  name     = var.db_name
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "app" {
  name     = var.db_user
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
}

resource "random_password" "db_password" {
  length  = 32
  special = false
}
```

### Secret Manager Integration

```hcl
resource "google_secret_manager_secret" "db_url" {
  secret_id = "${var.service_name}-database-url"
  project   = var.project_id

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_url" {
  secret      = google_secret_manager_secret.db_url.id
  secret_data = "postgresql+asyncpg://${google_sql_user.app.name}:${random_password.db_password.result}@/${google_sql_database.app.name}?host=/cloudsql/${google_sql_database_instance.main.connection_name}"
}

resource "google_secret_manager_secret_iam_member" "cloud_run_accessor" {
  secret_id = google_secret_manager_secret.db_url.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}
```

### Artifact Registry for Container Images

```hcl
resource "google_artifact_registry_repository" "app" {
  location      = var.region
  repository_id = var.repo_name
  format        = "DOCKER"
  project       = var.project_id

  cleanup_policies {
    id     = "keep-recent"
    action = "KEEP"
    most_recent_versions {
      keep_count = 10
    }
  }
}
```

### Variables and Outputs

```hcl
# variables.tf
variable "project_id" { type = string }
variable "region" { type = string; default = "us-central1" }
variable "environment" { type = string; default = "dev" }
variable "service_name" { type = string }
variable "image_tag" { type = string; default = "latest" }
variable "min_instances" { type = number; default = 0 }
variable "max_instances" { type = number; default = 10 }
variable "db_tier" { type = string; default = "db-f1-micro" }
variable "db_disk_size" { type = number; default = 10 }
variable "db_name" { type = string }
variable "db_user" { type = string }

# outputs.tf
output "service_url" {
  value = module.cloud_run.service_url
}

output "cloud_sql_connection" {
  value = google_sql_database_instance.main.connection_name
}
```

## Common Mistakes

- **Hardcoding project IDs**: Always use variables — resources must be portable across dev/staging/prod
- **No deletion protection**: Enable `deletion_protection` on Cloud SQL and critical resources in production
- **Public Cloud SQL**: Set `ipv4_enabled = false` and use private networking or Cloud SQL Auth Proxy
- **Missing secret IAM**: Cloud Run SA must have `secretmanager.secretAccessor` role to read secrets
- **No state locking**: GCS backend provides locking automatically — never use local backend in team environments
- **Skipping `terraform plan`**: Always review the plan before applying — especially for destructive changes
