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

resource "null_resource" "gdrive_folder" {
  triggers = {
    bq_dataset = var.dataset_name
  }

  provisioner "local-exec" {
    command = "cp -rf ../installation_scripts/Create_GDrive_folder.py aux_data/;"
  }

  provisioner "local-exec" {
    command = "[ ! -e create_gdrive_folder_results.json ] && echo \"{}\" >> create_gdrive_folder_results.json"
  }

  provisioner "local-exec" {
    command = "source venv/bin/activate; python3 aux_data/Create_GDrive_folder.py --folder_name=\"${var.gdrive_folder_name}\" --service_account_email=\"${module.genai_run_service_account.email}\""
  }
  depends_on = [null_resource.py_venv, module.genai_run_service_account]
}

data "local_file" "create_gdrive_folder_results_json" {
  filename   = "${path.module}/create_gdrive_folder_results.json"
  depends_on = [null_resource.gdrive_folder]
}

locals {
  gdrive_resuts = jsondecode(data.local_file.create_gdrive_folder_results_json.content)
}