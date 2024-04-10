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
  services = [
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "compute.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "container.googleapis.com",
    "cloudapis.googleapis.com",
    "cloudtrace.googleapis.com",
    "containerregistry.googleapis.com",
    "iamcredentials.googleapis.com",
    "dialogflow.googleapis.com",
    "monitoring.googleapis.com",
    "logging.googleapis.com",
    "notebooks.googleapis.com",
    "aiplatform.googleapis.com",
    "storage.googleapis.com",
    "datacatalog.googleapis.com",
    "appengineflex.googleapis.com",
    "translate.googleapis.com",
    "admin.googleapis.com",
    "docs.googleapis.com",
    "drive.googleapis.com",
    "sheets.googleapis.com",
    "slides.googleapis.com",
    "firebase.googleapis.com",
    "firestore.googleapis.com",
    "discoveryengine.googleapis.com",
    "secretmanager.googleapis.com"

  ]
  tables = [
    {
      name   = "customers",
      schema = "${path.module}/bq-schemas/customers.json"
    },
    {
      name   = "events",
      schema = "${path.module}/bq-schemas/events.json"
    },
    {
      name   = "metadata",
      schema = "${path.module}/bq-schemas/metadata.json"
    },
    {
      name   = "transactions",
      schema = "${path.module}/bq-schemas/transactions.json"
    }
  ]
}
