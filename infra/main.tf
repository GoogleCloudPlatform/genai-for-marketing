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

module "project_services" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "~> 17.0"

  project_id  = var.project_id
  enable_apis = true

  activate_apis               = local.services
  disable_services_on_destroy = false
}


## Creating venv for python scripts
resource "null_resource" "py_venv" {
  triggers = {
    bq_dataset = var.dataset_name
  }

  provisioner "local-exec" {
    working_dir = "scripts/"
    command     = "[ ! -d \"venv\" ] && python3 -m venv venv; source venv/bin/activate;pip install -r requirements.txt"
  }

}
