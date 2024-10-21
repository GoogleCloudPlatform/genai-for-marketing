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
    "${var.project_id}=>roles/iam.serviceAccountTokenCreator",
    "${var.project_id}=>roles/iam.serviceAccountUser",
    "${var.project_id}=>roles/iam.serviceAccountOpenIdTokenCreator",
    "${var.project_id}=>roles/iam.serviceAccountKeyAdmin",
    "${var.project_id}=>roles/iam.workloadIdentityUser"
  ]
  depends_on = [module.project_services]
}

# IAM Binding to ensure build service account have the requireds roles to build the backend_api

data "google_project" "project" {
  project_id = var.project_id
}

locals {
  cb_roles = [
    "roles/storage.objectViewer", 
    "roles/logging.logWriter", 
    "roles/artifactregistry.writer",
    "roles/iam.serviceAccountTokenCreator",
    "roles/iam.serviceAccountUser",
    "roles/iam.serviceAccountOpenIdTokenCreator",
    "roles/iam.serviceAccountKeyAdmin",
    "roles/iam.workloadIdentityUser"
    ]
}
resource "google_project_iam_member" "cb_roles" {
  count   = length(local.cb_roles)
  project = var.project_id
  role    = local.cb_roles[count.index]
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}
