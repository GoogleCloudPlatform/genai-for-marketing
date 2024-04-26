/**
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 
resource "google_artifact_registry_repository" "docker-repo" {
  project       = var.project_id
  location      = "us-central1"
  repository_id = "docker"
  format        = "DOCKER"
}

resource "google_secret_manager_secret" "secret-cred" {
  project   = var.project_id
  secret_id = "credentials"
  replication {
    auto {}
  }
}


resource "google_secret_manager_secret_version" "secret-cred-version" {
  secret      = google_secret_manager_secret.secret-cred.id
  secret_data = base64decode(google_service_account_key.sa_key.private_key)
}

resource "null_resource" "backend_deployment" {

  triggers = {
    sa = module.genai_run_service_account.service_account.name
  }

  provisioner "local-exec" {
    command = "cp -rf ../installation_scripts/backend_deployment.sh aux_data/"
  }

  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-c"]
    command     = "sh aux_data/backend_deployment.sh ${var.region} ${module.genai_run_service_account.email}"
  }

  depends_on = [google_artifact_registry_repository.docker-repo, local_file.config_toml]
}

data "google_cloud_run_service" "run_service" {
  project    = var.project_id
  name       = "genai-for-marketing"
  location   = var.region
  depends_on = [null_resource.backend_deployment]
}

resource "google_firebase_project" "firebase" {
  provider = google-beta
  project  = var.project_id
}

resource "google_firebase_web_app" "app_front" {
  provider     = google-beta
  project      = var.project_id
  display_name = "GenAI for marketing"
}

data "google_firebase_web_app_config" "app_front" {
  project    = var.project_id
  provider   = google-beta
  web_app_id = google_firebase_web_app.app_front.app_id
}

module "gcs_assets_bucket" {
  source     = "terraform-google-modules/cloud-storage/google"
  version    = "~> 5.0"
  project_id = var.project_id
  names      = ["marketing"]
  prefix     = var.project_id
}


resource "local_file" "config_toml" {
  content = templatefile("${path.module}/templates/config.toml.tftpl", {
    project_id              = var.project_id,
    region                  = var.region,
    dataset_name            = var.dataset_name,
    credentials_secret_name = google_secret_manager_secret_version.secret-cred-version.name,
    search_datastore_id     = google_discovery_engine_data_store.search_datastore.data_store_id,
    tag_template_id         = var.tag_template_id,
    drive_folder_id         = local.gdrive_resuts.GDRIVE_FOLDER_ID,
    slides_template_id      = local.gdrive_resuts.MarketingPptID,
    doc_template_id         = local.gdrive_resuts.MarketingDocID,
    sheet_template_id       = local.gdrive_resuts.MarketingExcelID,
    domain                  = var.domain,
    gcs_assets_bucket       = module.gcs_assets_bucket.name
    }
  )
  filename = "${path.module}/templates/config.toml"
}

resource "local_file" "enviroments_ts" {
  content = templatefile("${path.module}/templates/environments.ts.tftpl", {
    run_service_url        = data.google_cloud_run_service.run_service.status[0].url,
    fb_api_key             = data.google_firebase_web_app_config.app_front.api_key,
    fb_auth_domain         = data.google_firebase_web_app_config.app_front.auth_domain,
    fb_project_id          = var.project_id,
    fb_storage_bucket      = lookup(data.google_firebase_web_app_config.app_front, "storage_bucket", ""),
    fb_messaging_sender_id = lookup(data.google_firebase_web_app_config.app_front, "messaging_sender_id", ""),
    fb_api_id              = google_firebase_web_app.app_front.app_id,
    fb_measurement_id      = lookup(data.google_firebase_web_app_config.app_front, "measurement_id", ""),
    dialogflow_cx_agent_id = google_discovery_engine_chat_engine.chat_app.chat_engine_metadata[0].dialogflow_agent
    }
  )
  filename = "${path.module}/templates/environments.ts"
}

resource "null_resource" "frontend_deployment" {

  triggers = {
    sa = module.genai_run_service_account.service_account.name
  }

  provisioner "local-exec" {
    command = "cp -rf ../installation_scripts/frontend_deployment.sh aux_data/"
  }

  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-c"]
    command     = "sh aux_data/frontend_deployment.sh ${var.project_id}"
  }

  depends_on = [google_artifact_registry_repository.docker-repo, local_file.enviroments_ts]
}