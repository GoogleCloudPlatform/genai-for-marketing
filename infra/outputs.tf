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

locals {
  infra_ouput = {
    project_id             = var.project_id,
    region                 = var.region
    backend_deployment_url = google_cloud_run_service.backend.status[0].url,
    cloud_run_backend_sa   = module.genai_run_service_account.email,
    frontend_deployment    = "https://${var.project_id}.web.app",
    firebase_config = {
      api_key             = data.google_firebase_web_app_config.app_front.api_key,
      auth_domain         = data.google_firebase_web_app_config.app_front.auth_domain,
      project_id          = var.project_id,
      storage_bucket      = lookup(data.google_firebase_web_app_config.app_front, "storage_bucket", ""),
      messaging_sender_id = lookup(data.google_firebase_web_app_config.app_front, "messaging_sender_id", ""),
      api_id              = google_firebase_web_app.app_front.app_id,
      measurement_id      = lookup(data.google_firebase_web_app_config.app_front, "measurement_id", ""),
    },

    dialogflow_cx_agent_id = google_discovery_engine_chat_engine.chat_app.chat_engine_metadata[0].dialogflow_agent
  }
}

output "genai_marketing_infra" {
  value = local.infra_ouput
}

resource "local_file" "genai_marketing_infra" {
  content  = jsonencode(local.infra_ouput)
  filename = "${path.module}/output_config/genai_marketing_infra.json"
}
