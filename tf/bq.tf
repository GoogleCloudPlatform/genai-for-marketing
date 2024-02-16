
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
  source  = "terraform-google-modules/bigquery/google"
  version = "~> 7.0"
  dataset_id                  = var.dataset_name
  dataset_name                = var.dataset_name
  project_id                  = var.project_id
  location                    = var.location
  default_table_expiration_ms = 3600000

  tables = local.bq_tables
}

## Creating dataset tables

## Populating tables with scripts
## Loading data from old scripts
#TODO

resource "null_resource" "bq_tables_populate" {
  # Changes to any instance of the cluster requires re-provisioning
  triggers = {
    bq_tables = join(",", module.bigquery.table_ids)
  }

  provisioner "local-exec" {
    # Bootstrap script called with private_ip of each node in the cluster
    command = "echo  'TODO execute pupulate scripts'"
  }
}


# Creating tag tempalte
resource "google_data_catalog_tag_template" "tag_template" {
    project = var.project_id
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

  force_delete = "false"
}

## Tag columns using scripts
## Loading data from old scripts
#TODO


resource "null_resource" "bq_tagging" {
  # Changes to any instance of the cluster requires re-provisioning
  triggers = {
    bq_tables = join(",", module.bigquery.table_ids)
  }

  provisioner "local-exec" {
    # Bootstrap script called with private_ip of each node in the cluster
    command = "echo  'TODO execute pupulate scripts'"
  }
}
