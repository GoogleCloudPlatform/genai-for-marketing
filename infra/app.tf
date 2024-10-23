/**
 * Copyright 2024 Google LLC
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
  depends_on    = [module.project_services]
}

/*
* Deploying sample image to get Cloud Run
* This is a workarround that allow us to get the URL of the service and pass the resulting value to the fontend deployment
*/
resource "google_cloud_run_service" "backend" {
  name     = "genai-for-marketing-backend-apis"
  location = var.region
  project  = var.project_id

  template {
    spec {
      containers {
        image = "us-docker.pkg.dev/cloudrun/container/hello"
      }
      service_account_name = module.genai_run_service_account.email
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Allow unauthenticated invocations
resource "google_cloud_run_service_iam_member" "invoker" {
  location = google_cloud_run_service.backend.location
  project  = google_cloud_run_service.backend.project
  service  = google_cloud_run_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_firebase_project" "firebase" {
  provider   = google-beta
  project    = var.project_id
  depends_on = [module.project_services]
}

resource "google_firebase_web_app" "app_front" {
  provider     = google-beta
  project      = var.project_id
  display_name = "GenAI for marketing"
  depends_on   = [module.project_services]
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
  depends_on = [module.project_services]
}

resource "local_file" "config_toml" {
  content = templatefile("${path.module}/templates/config.toml.tftpl", {
    project_id              = var.project_id,
    region                  = var.region,
    dataset_name            = var.dataset_name,
    search_datastore_id     = google_discovery_engine_data_store.search_datastore.data_store_id,
    tag_template_id         = var.tag_template_id,
    drive_folder_id         = var.gdrive_config.gdrive_folder_id,
    slides_template_id      = var.gdrive_config.marketing_slide_id,
    doc_template_id         = var.gdrive_config.marketing_doc_id,
    sheet_template_id       = var.gdrive_config.marketing_sheet_id,
    domain                  = var.domain,
    gcs_assets_bucket       = module.gcs_assets_bucket.name
    }
  )
  filename = "${path.module}/output_config/config.toml"
}

resource "local_file" "enviroments_ts" {
  content = templatefile("${path.module}/templates/environments.ts.tftpl", {
    run_service_url        = google_cloud_run_service.backend.status[0].url,
    fb_api_key             = data.google_firebase_web_app_config.app_front.api_key,
    fb_auth_domain         = data.google_firebase_web_app_config.app_front.auth_domain,
    fb_project_id          = var.project_id,
    fb_storage_bucket      = lookup(data.google_firebase_web_app_config.app_front, "storage_bucket", ""),
    fb_messaging_sender_id = lookup(data.google_firebase_web_app_config.app_front, "messaging_sender_id", ""),
    fb_api_id              = google_firebase_web_app.app_front.app_id,
    fb_measurement_id      = lookup(data.google_firebase_web_app_config.app_front, "measurement_id", ""),
    dialogflow_cx_agent_id = reverse(split("/",google_discovery_engine_chat_engine.chat_app.chat_engine_metadata[0].dialogflow_agent))[0]
    }
  )
  filename = "${path.module}/output_config/environments.ts"
}

resource "local_file" "campaign_form" {
  content = templatefile("${path.module}/templates/campaign-form.component.html.tftpl", {
    campaigns_themes        = var.campaigns_themes,
    }
  )
  filename = "${path.module}/output_config/campaign-form.component.html"
}

resource "local_file" "aux_data" {
  content = templatefile("${path.module}/templates/transactions_aux_data.py.tftpl", {
    campaigns_themes        = var.campaigns_themes,
    campaigns_themes        = var.campaigns_themes,
    }
  )
  filename = "${path.module}/scripts/aux_data/transactions_aux_data.py"
}


resource "google_firestore_database" "database" {
  project         = var.project_id
  name            = "(default)"
  location_id     = var.region
  type            = "FIRESTORE_NATIVE"
  deletion_policy = "DELETE"
  depends_on      = [module.project_services]
}
