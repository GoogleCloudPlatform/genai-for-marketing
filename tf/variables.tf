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

variable "project_id" {
  type = string
}

variable "location" {
  default     = "US"
  type        = string
  description = "Location of the resources"
}

variable "genai_location" {
  default     = "global"
  type        = string
  description = "Location of the resources"
}

variable "region" {
  default     = "us-central1"
  type        = string
  description = "Location of the resources"
}

variable "dataset_name" {
  type        = string
  default     = "genai_marketing"
  description = "BigQuery dataset name"
}

variable "tag_template_id" {
  type    = string
  default = "llmcdptemplate"
}

variable "search_app_name" {
  type        = string
  default     = "genai_marketing"
  description = "Vertex Search app name"
}

variable "chat_bot_name" {
  type        = string
  default     = "genai_marketing"
  description = "Vertex Conversation app name"
}

variable "genai_marketing_service_account" {
  type        = string
  default     = "genai-marketing-sa"
  description = "Service account name"

}
variable "existing_looker_uri" {
  type        = string
  default     = ""
  description = "Existing looker dashboard uri"
}

variable "company_name" {
  type        = string
  default     = "Google"
  description = "Company name"
}
variable "domain" {
  type        = string
  default     = "google.com"
  description = "Your company domain"

}
variable "gdrive_folder_name" {
  type        = string
  default     = "genai-marketing-assets"
  description = "Google drive folder name"
}

variable "datastore_uris" {
  type    = list(string)
  default = ["cloud.google.com/*"]
}

variable "datastore_storage_folder" {
  type    = string
  default = "gs://cloud-samples-data/gen-app-builder/search/alphabet-investor-pdfs/*"
}