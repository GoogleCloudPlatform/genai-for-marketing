#!/bin/bash
#
# Performs an automated installation of the Generative AI for Marketing solution accelerator
# Modify the Globals variables prior to running this script
#################################

# Global variables
#################################
PROJECT_ID="project-001"          # ID of the project where you want to deploy
LOCATION="us-central1"            # Name of the region 
DATASET_NAME="naga_test"          # BigQuery Dataset Name for creation
SEARCH_APP_NAME="naga_test"       # Vertex Search App Name for creation
CHAT_BOT_NAME="naga_test_chat"    # Vertex Conversation app Name for creation
COMPANY_NAME="naga_test"          # Your company name 
EXISTING_LOOKER_URI=""            # your Existing Looker dashboard URl. leave it empty if you don't have
SERVICE_ACCOUNT="genai-markting-sa"    # Service account name for creation
YOUR_DOMAIN="google.com"               # Your domain name. eg user@company.com then company.com 
GDRIVE_FOLDER_NAME="genai-marketing-assets"      # Google drive folder name for creation

# do not modify below here

SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com"   # Do not modify this


gcloud config set project $PROJECT_ID   # Setting the Project in Gcloud

PROJECT_NUMBER=`gcloud projects describe $PROJECT_ID --format="value(projectNumber)"`     # Getting the project Number  

# Enabling the services
gcloud services enable run.googleapis.com cloudbuild.googleapis.com compute.googleapis.com cloudresourcemanager.googleapis.com iam.googleapis.com container.googleapis.com cloudapis.googleapis.com cloudtrace.googleapis.com containerregistry.googleapis.com iamcredentials.googleapis.com
gcloud services enable monitoring.googleapis.com logging.googleapis.com notebooks.googleapis.com aiplatform.googleapis.com storage.googleapis.com datacatalog.googleapis.com appengineflex.googleapis.com translate.googleapis.com admin.googleapis.com docs.googleapis.com drive.googleapis.com sheets.googleapis.com slides.googleapis.com

if [ ! -d "genai_for_marketing_automation" ]; then   # Checking the Virtualenv folder exists or not
   python3 -m venv genai_for_marketing_automation    # Creating virtualenv  
fi

source genai_for_marketing_automation/bin/activate   # activate Virtualenv

if [ ! -d "genai-for-marketing" ]; then   # Checking the github code folder exists or not
  git clone https://github.com/GoogleCloudPlatform/genai-for-marketing   # cloning the genai-for-marketing code from github
else
  rm -rf genai-for-marketing
  git clone https://github.com/GoogleCloudPlatform/genai-for-marketing

fi

# Updating the Project and Location details in app config and override files
sed -i "s|project_id = \"\"|project_id = '${PROJECT_ID}'|" genai-for-marketing/app/app_config.toml
sed -i "s|location = \"us-central1\"|location = '${LOCATION}'|" genai-for-marketing/app/app_config.toml
sed -i "s|project_id = \"\"|project_id = '${PROJECT_ID}'|" genai-for-marketing/app/override.toml
sed -i "s|location = \"us-central1\"|location = '${LOCATION}'|" genai-for-marketing/app/override.toml


# installing required python packages
pip install -U google-cloud-datacatalog google-cloud-storage google-cloud-bigquery numpy google-api-python-client google.cloud google.auth google-cloud-discoveryengine google-cloud-dialogflow-cx

# copy the BigQuery template data to current directory
if [ ! -d "aux_data" ]; then
   cp -rf genai-for-marketing/notebooks/aux_data .
fi

#-----BigQuery Setup -----
python3 genai_marketing_env_setup.py $PROJECT_ID $LOCATION $DATASET_NAME

# Update the BigQuery Details in config files 
sed -i "s|dataset_id = \"\"|dataset_id = \"${DATASET_NAME}\"|g" genai-for-marketing/app/app_config.toml
sed -i "s|dataset_id = \"\"|dataset_id = \"${DATASET_NAME}\"|g" genai-for-marketing/app/override.toml
sed -i "s|tag_name = \"\"|tag_name = \"llmcdptemplate\"|g" genai-for-marketing/app/app_config.toml
sed -i "s|tag_name = \"\"|tag_name = \"llmcdptemplate\"|g" genai-for-marketing/app/override.toml


# gcloud auth application-default login
# gcloud auth application-default set-quota-project $PROJECT_ID

python3 genai_marketing_search_app_creation.py --project="${PROJECT_ID}" --app-name="${SEARCH_APP_NAME}" --company-name="${COMPANY_NAME}" --uris="cloud.goole.com/*"

SEARCH_DATASTORE_ID=`jq -r '.SEARCH_DATASTORE_ID' < marketingEnvValue.json`

sed -i "s|# datastores.<datastore ID> = 'default_config'|datastores.${SEARCH_DATASTORE_ID} = 'default_config'|g" genai-for-marketing/app/app_config.toml
sed -i "s|datastores.example = 'default_config'|datastores.${SEARCH_DATASTORE_ID} = 'default_config'|g" genai-for-marketing/app/override.toml

python3 Create_GDrive_folder.py --folder_name="${GDRIVE_FOLDER_NAME}" --service_account_email="${SERVICE_ACCOUNT_EMAIL}"

SERVICE_ACCOUNT_CHECK=`gcloud iam service-accounts list --format=json | jq .[].email | grep "${SERVICE_ACCOUNT_EMAIL}" | wc -l`

if [[ SERVICE_ACCOUNT_CHECK -eq 0 ]]; then
    gcloud iam service-accounts create ${SERVICE_ACCOUNT} --display-name="${SERVICE_ACCOUNT}"
fi
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" --role="roles/logging.logWriter" --condition=None
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" --role="roles/artifactregistry.reader" --condition=None
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" --role="roles/storage.objectViewer" --condition=None

if [ ! -f genai-for-marketing/app/credentials.json ]; then
  gcloud iam service-accounts keys create genai-for-marketing/app/credentials.json --iam-account=${SERVICE_ACCOUNT_EMAIL}
fi

if [ ! -f credentials.json ]; then
   gcloud iam service-accounts keys create credentials.json --iam-account="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
fi
export GOOGLE_APPLICATION_CREDENTIALS=credentials.json
python3 genai_marketing_conversation_app_creation.py --project="${PROJECT_ID}" --location="global" --app-name="${CHAT_BOT_NAME}" --company-name="${COMPANY_NAME}" --uris="support.google.com/google-ads/*" 

CHAT_AGENT_ID=`jq -r '.AGENT_ENGINE_NAME' < marketingEnvValue.json | cut -d'/' -f6`
AGENT_LANGUAGE_CODE=`jq -r '.AGENT_LANGUAGE_CODE' < marketingEnvValue.json`

sed -i "s|  agent-id=\"\"|  agent-id=\"${CHAT_AGENT_ID}\"|g" genai-for-marketing/app/app_config.toml
sed -i "s|  project-id=\"\"|  project-id=\"${PROJECT_ID}\"|g" genai-for-marketing/app/app_config.toml
sed -i "s|  language-code=\"\"|  language-code=\"${AGENT_LANGUAGE_CODE}\"|g" genai-for-marketing/app/app_config.toml

sed -i "s|  agent-id=\"\"|  agent-id=\"${CHAT_AGENT_ID}\"|g" genai-for-marketing/app/override.toml
sed -i "s|  project-id=\"\"|  project-id=\"${PROJECT_ID}\"|g" genai-for-marketing/app/override.toml
sed -i "s|  language-code=\"\"|  language-code=\"${AGENT_LANGUAGE_CODE}\"|g" genai-for-marketing/app/override.toml

if [[ $EXISTING_LOOKER_URI != "" ]];then
   sed -i "s|dashboards.Overview = 'https://googledemo.looker.com/embed/dashboards/2131?allow_login_screen=true|dashboards.Overview = '${EXISTING_LOOKER_URI}'|" genai-for-marketing/app/app_config.toml
   sed -i "s|dashboards.Overview = ''|dashboards.Overview = '${EXISTING_LOOKER_URI}'|" genai-for-marketing/app/app_config.toml
fi

sed -i "s|domain = \"<YOUR DOMAIN>\"|domain = \"${YOUR_DOMAIN}\"|" genai-for-marketing/app/override.toml

GDRIVE_FOLDER_ID=`jq -r '.GDRIVE_FOLDER_ID' < marketingEnvValue.json`
MarketingPptID=`jq -r '.MarketingPptID' < marketingEnvValue.json`
MarketingDocID=`jq -r '.MarketingDocID' < marketingEnvValue.json`
MarketingExcelID=`jq -r '.MarketingExcelID' < marketingEnvValue.json`

sed -i "s|drive_folder_id = ''|drive_folder_id = '${GDRIVE_FOLDER_ID}'|" genai-for-marketing/app/app_config.toml
sed -i "s|slides_template_id = ''|slides_template_id = '${MarketingPptID}'|" genai-for-marketing/app/app_config.toml
sed -i "s|doc_template_id = ''|doc_template_id = '${MarketingDocID}'|" genai-for-marketing/app/app_config.toml
sed -i "s|sheet_template_id = ''|sheet_template_id = '${MarketingExcelID}'|" genai-for-marketing/app/app_config.toml
sed -i "s|service_account: <REPLACE WITH YOUR SERVICE ACCOUNT ADDRESS>|service_account: '${PROJECT_NUMBER}-compute@developer.gserviceaccount.com'|" genai-for-marketing/app.yaml
sed -i "s|service_account_json_key = '/credentials/credentials.json'|service_account_json_key = '/app/credentials.json'|" genai-for-marketing/app/app_config.toml
sed -i "s|service_account_json_key = \"\"|service_account_json_key = \"/app/credentials.json\"|" genai-for-marketing/app/override.toml

#---override.toml---
sed -i "s|drive_folder_id = \"\"|drive_folder_id = \"${GDRIVE_FOLDER_ID}\"|" genai-for-marketing/app/override.toml
sed -i "s|slides_template_id = \"\"|slides_template_id = \"${MarketingPptID}\"|" genai-for-marketing/app/override.toml
sed -i "s|doc_template_id = \"\"|doc_template_id = \"${MarketingDocID}\"|" genai-for-marketing/app/override.toml
sed -i "s|sheet_template_id = \"\"|sheet_template_id = \"${MarketingExcelID}\"|" genai-for-marketing/app/override.toml

cat >> genai-for-marketing/app.yaml <<EOL

network:
  name: projects/${PROJECT_ID}/global/networks/default
  subnetwork_name: default
EOL

cd genai-for-marketing && gcloud app deploy --quiet