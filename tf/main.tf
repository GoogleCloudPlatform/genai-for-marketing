
resource "google_project_service" "project" {
  count   = length(local.services)
  project = var.project_id
  service = local.services[count.index]

  timeouts {
    create = "30m"
    update = "40m"
  }

}

## Creating venv for python scripts
resource "null_resource" "py_venv" {
  triggers = {
    bq_dataset = var.dataset_name
  }

  provisioner "local-exec" {
    command = "cp -rf ../notebooks/aux_data . ;[ ! -d \"venv\" ] && python3 -m venv venv; source venv/bin/activate;pip install google-cloud-datacatalog google-cloud-storage google-cloud-bigquery numpy google-api-python-client google.cloud google.auth google-cloud-discoveryengine google-cloud-dialogflow-cx"
  }

}
