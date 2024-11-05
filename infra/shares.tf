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

resource "null_resource" "create_folder" {
  provisioner "local-exec" {
    working_dir = "scripts/"
    command     = "venv/bin/python3 create_gdrive_folder.py  --folder-name=${var.gdrive_folder_name}"
  }
  depends_on = [
    null_resource.py_venv,
    local_file.genai_marketing_infra
    ]
}

data "external" "gdrive_pointers" {
  program = ["cat", "${path.module}/output_config/gdrive_folder_results.json"]
  depends_on = [null_resource.create_folder]
}

locals {
  gdrive_pointers = data.external.gdrive_pointers.result
}

output "gdrive_pointers" {
  value = local.gdrive_pointers
}