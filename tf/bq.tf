
locals {
  bq_tables = [for t in local.tables : {
    table_id           = t.name,
    schema             = file(t.schema),
    time_partitioning  = null,
    range_partitioning = null,
    expiration_time    = null,
    clustering         = [],
    labels             = {}
  }]
}

module "bigquery" {
  source                      = "terraform-google-modules/bigquery/google"
  version                     = "~> 7.0"
  dataset_id                  = var.dataset_name
  dataset_name                = var.dataset_name
  project_id                  = var.project_id
  location                    = var.location
  default_table_expiration_ms = 3600000

  tables = local.bq_tables
}

## Populating tables with scripts
resource "null_resource" "bq_tables_populate" {
  triggers = {
    bq_dataset = var.dataset_name
  }

  provisioner "local-exec" {
    command = "source venv/bin/activate; python3 -c 'from aux_data import data_gen; data_gen.generate_and_populate_dataset(PROJECT_ID=\"${var.project_id}\",DATASET_ID=\"${var.dataset_name}\",create_tables=False)'"
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
}

## Tag columns using scripts
## Loading data from old scripts
#TODO

resource "null_resource" "bq_tagging" {

  triggers = {
    bq_tables    = join(",", module.bigquery.table_ids)
    tag_template = google_data_catalog_tag_template.tag_template.id
  }

  provisioner "local-exec" {
    command = "source venv/bin/activate; python3 -c 'from aux_data import bq_tag_generation; bq_tag_generation.create_template_and_tag_bq(\"${var.project_id}\",\"${var.dataset_name}\",\"${google_data_catalog_tag_template.tag_template.tag_template_id}\",\"${var.location}\")'"
  }
  depends_on = [null_resource.py_venv, module.bigquery, google_data_catalog_tag_template.tag_template]

}
