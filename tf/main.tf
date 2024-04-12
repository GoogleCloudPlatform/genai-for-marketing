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

## Creating venv for python scripts
resource "null_resource" "py_venv" {
  triggers = {
    bq_dataset = var.dataset_name
  }

  provisioner "local-exec" {
    command = "cp -rf ../notebooks/aux_data . ;[ ! -d \"venv\" ] && python3 -m venv venv; source venv/bin/activate;pip install google-cloud-datacatalog google-cloud-storage google-cloud-bigquery numpy google-api-python-client google.cloud google.auth google-cloud-discoveryengine google-cloud-dialogflow-cx"
  }

}
