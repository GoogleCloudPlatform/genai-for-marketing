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

module "bigquery" {
  source                      = "terraform-google-modules/bigquery/google"
  version                     = "~> 7.0"
  dataset_id                  = var.dataset_name
  dataset_name                = var.dataset_name
  project_id                  = var.project_id
  location                    = var.location
  default_table_expiration_ms = null

  tables     = local.bq_tables
  depends_on = [module.project_services]
}

## Populating tables with scripts
resource "null_resource" "bq_tables_populate" {
  triggers = {
    bq_dataset = var.dataset_name
  }

  provisioner "local-exec" {
    working_dir = "scripts/"
    command     = "source venv/bin/activate; python3 -c 'from aux_data import data_gen; data_gen.generate_and_populate_dataset(PROJECT_ID=\"${var.project_id}\",DATASET_ID=\"${var.dataset_name}\",create_tables=False, min_records=${var.dataset_tables_min_records})'"
  }
  depends_on = [null_resource.py_venv, module.bigquery]
}


# Creating tag tempalte
resource "google_data_catalog_tag_template" "tag_template" {
  project         = var.project_id
  tag_template_id = var.tag_template_id
  region          = var.region
  display_name    = "Talk to data catalog template"

  fields {
    field_id     = "description"
    display_name = "Description"
    type {
      primitive_type = "STRING"
    }
    is_required = true
  }

  fields {
    field_id     = "is_primary_key"
    display_name = "is_primary_key"
    type {
      primitive_type = "BOOL"
    }
  }

  fields {
    field_id     = "is_foreign_key"
    display_name = "is_foreign_key"
    type {
      primitive_type = "BOOL"
    }
  }

  fields {
    field_id     = "data_type"
    display_name = "Data Type"
    type {
      primitive_type = "STRING"
    }
  }

  force_delete = "true"

  depends_on = [module.project_services]
}

## Tag columns using scripts
## Loading data from old scripts

resource "null_resource" "bq_tagging" {

  triggers = {
    bq_tables    = join(",", module.bigquery.table_ids)
    tag_template = google_data_catalog_tag_template.tag_template.id
  }

  provisioner "local-exec" {
    working_dir = "scripts/"
    command     = "source venv/bin/activate; python3 -c 'from aux_data import bq_tag_generation; bq_tag_generation.tag_metadata_from_bq(\"${var.project_id}\",\"${var.dataset_name}\",\"${google_data_catalog_tag_template.tag_template.name}\",\"${google_data_catalog_tag_template.tag_template.tag_template_id}\")'"
  }
  depends_on = [null_resource.py_venv, module.bigquery, google_data_catalog_tag_template.tag_template]

}
