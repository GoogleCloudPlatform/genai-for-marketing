
resource "google_project_service" "project" {
  count   = length(local.services)
  project = var.project_id
  service = local.services[count.index]

  timeouts {
    create = "30m"
    update = "40m"
  }
  disable_dependent_services = true
}