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


resource "random_string" "random" {
  length  = 4
  special = false
  lower   = true
  upper   = false
}

locals {
  data_store_id    = "${var.search_app_name}_datastore_${random_string.random.result}"
  search_engine_id = "${var.search_app_name}_search_engine_${random_string.random.result}"

  chat_engine_id        = "${var.search_app_name}_chat_engine_${random_string.random.result}"
  website_data_store_id = "${var.search_app_name}_web_datastore_${random_string.random.result}"
  storage_data_store_id = "${var.search_app_name}_storage_datastore_${random_string.random.result}"
}


resource "google_discovery_engine_data_store" "search_datastore" {
  project                     = var.project_id
  location                    = var.genai_location
  data_store_id               = local.data_store_id
  display_name                = "tf-test-structured-datastore"
  industry_vertical           = "GENERIC"
  content_config              = "PUBLIC_WEBSITE"
  solution_types              = ["SOLUTION_TYPE_SEARCH"]
  create_advanced_site_search = false
}

resource "google_discovery_engine_search_engine" "search_app" {
  project        = var.project_id
  engine_id      = local.search_engine_id
  collection_id  = "default_collection"
  location       = var.genai_location
  display_name   = local.search_engine_id
  data_store_ids = [google_discovery_engine_data_store.search_datastore.data_store_id]
  search_engine_config {
  }
}

// Creating target site
resource "null_resource" "genai_marketing_search_target_site" {
  triggers = {
    search_app = google_discovery_engine_search_engine.search_app.id
  }
  provisioner "local-exec" {
    command = "cp -rf ../installation_scripts/genai_marketing_search_app_creation.py aux_data/"
  }
  provisioner "local-exec" {
    command = "source venv/bin/activate; python3 -c 'from aux_data import genai_marketing_search_app_creation; genai_marketing_search_app_creation.create_target_site(\"${var.project_id}\",\"${var.genai_location}\",\"${google_discovery_engine_data_store.search_datastore.data_store_id}\",\"${join(",", var.datastore_uris)}\")'"
  }
  depends_on = [null_resource.py_venv, google_discovery_engine_search_engine.search_app]
}

resource "google_discovery_engine_data_store" "website_datastore" {
  project           = var.project_id
  location          = var.genai_location
  data_store_id     = local.website_data_store_id
  display_name      = local.website_data_store_id
  industry_vertical = "GENERIC"
  content_config    = "PUBLIC_WEBSITE"
  solution_types    = ["SOLUTION_TYPE_CHAT"]
}

resource "google_discovery_engine_data_store" "storage_datastore" {
  project           = var.project_id
  location          = var.genai_location
  data_store_id     = local.storage_data_store_id
  display_name      = local.storage_data_store_id
  industry_vertical = "GENERIC"
  content_config    = "CONTENT_REQUIRED"
  solution_types    = ["SOLUTION_TYPE_CHAT"]
}

resource "google_discovery_engine_chat_engine" "chat_app" {
  project           = var.project_id
  engine_id         = local.chat_engine_id
  collection_id     = "default_collection"
  location          = var.genai_location
  display_name      = "Chat engine"
  industry_vertical = "GENERIC"
  data_store_ids = [
    google_discovery_engine_data_store.website_datastore.data_store_id,
  google_discovery_engine_data_store.storage_datastore.data_store_id]
  common_config {
    company_name = var.company_name
  }
  chat_engine_config {
    agent_creation_config {
      business              = var.company_name
      default_language_code = "en"
      time_zone             = "America/Los_Angeles"
    }
  }
}