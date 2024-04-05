
module "genai_run_service_account" {
  source     = "terraform-google-modules/service-accounts/google"
  version    = "~> 3.0"
  project_id = var.project_id
  names      = ["genai-marketing-run"]
  project_roles = [
    "${var.project_id}=>roles/logging.logWriter",
    "${var.project_id}=>roles/artifactregistry.reader",
    "${var.project_id}=>roles/storage.objectViewer",
    "${var.project_id}=>roles/aiplatform.admin",
    "${var.project_id}=>roles/secretmanager.secretAccessor",
  ]
}

resource "google_service_account_key" "sa_key" {
  service_account_id = module.genai_run_service_account.service_account.name
}