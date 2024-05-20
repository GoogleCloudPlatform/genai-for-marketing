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
    "firebasehosting.googleapis.com",
    "discoveryengine.googleapis.com",
    "secretmanager.googleapis.com",
    "artifactregistry.googleapis.com",
    "firestore.googleapis.com"
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
