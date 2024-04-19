export PROJECT_ID=project-id-here  
gcloud config set project $PROJECT_ID  
gcloud auth application-default set-quota-project $PROJECT_ID
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  compute.googleapis.com \
  cloudresourcemanager.googleapis.com \
  iam.googleapis.com \
  container.googleapis.com \
  cloudapis.googleapis.com \
  cloudtrace.googleapis.com \
  containerregistry.googleapis.com \
  iamcredentials.googleapis.com \
  secretmanager.googleapis.com \
  firebase.googleapis.com

gcloud services enable \
  monitoring.googleapis.com \
  logging.googleapis.com \
  notebooks.googleapis.com \
  aiplatform.googleapis.com \
  storage.googleapis.com \
  datacatalog.googleapis.com \
  appengineflex.googleapis.com \
  translate.googleapis.com \
  admin.googleapis.com \
  docs.googleapis.com \
  drive.googleapis.com \
  sheets.googleapis.com \
  slides.googleapis.com \
  firestore.googleapis.com

export USER_PROJECT_OVERRIDE=true
export GOOGLE_BILLING_PROJECT=$PROJECT_ID

terraform init

terraform apply -var=project_id=$PROJECT_ID
