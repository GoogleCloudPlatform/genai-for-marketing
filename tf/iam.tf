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

module "genai_run_service_account" {
  source     = "terraform-google-modules/service-accounts/google"
  version    = "~> 3.0"
  project_id = var.project_id
  names      = ["genai-marketing-run"]
  project_roles = [
    "${var.project_id}=>roles/logging.logWriter",
    "${var.project_id}=>roles/artifactregistry.reader",
    "${var.project_id}=>roles/storage.objectViewer",
    "${var.project_id}=>roles/storage.objectUser",
    "${var.project_id}=>roles/aiplatform.admin",
    "${var.project_id}=>roles/secretmanager.secretAccessor",
    "${var.project_id}=>roles/bigquery.dataViewer",
    "${var.project_id}=>roles/bigquery.jobUser",
    "${var.project_id}=>roles/datastore.user",
  ]
}

resource "google_service_account_key" "sa_key" {
  service_account_id = module.genai_run_service_account.service_account.name
}