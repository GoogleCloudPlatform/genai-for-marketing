

output "backend_deployment" {
  value = data.google_cloud_run_service.run_service.status[0].url
}

output "backend_service_account" {
  value = module.genai_run_service_account.email
}

output "frontend_deployment" {
  value = "https://${var.project_id}.web.app"
}