# Infrastructure Deployment
Terraform simplifies deploying Generative AI for Marketing. The Terraform deployment includes all necessary requirements.

*Note*: The Terraform Provider for Google Cloud is not able to generate some of the GenAI resources, `null_resource` is used to create some resources using the Google Cloud SDK.

You'll need to create a Google Cloud project and link a billing account before you begin. **It is strongly recommended you deploy Generative AI for Marketing in it's own fresh project.** Existing resources in a project may be impacted by the deployment, and the deployment itself may fail.

## Prerequisites:

Before executing Terraform, follow these steps to enable some services:

### Enable Firebase
Will be used for the frontend deployment

1. Go to https://console.firebase.google.com/.
2. Select "Create a project" and enter the name of your Google Cloud Platform project, then click "Continue". 
3. If you're using Firebase for the first time, you'll have to add Firebase to one of yor existing Google Cloud projects and confirm the Firebase billing plan.
4. When prompted to set up Google Analytics respond as you'd like.
5. Continue and complete.

### Enable Vertex AI Agent Builder
Required before starting using App Builder services.
1. Go to https://console.cloud.google.com/gen-app-builder/start
2. Click the button to accept TOS and enable.

### (Optional) Local Configuration

Cloud Shell is the recommend environment for running the deployment. If you are deploying from outside Cloud Shell, set up your Google Cloud SDK Credentials:

```shell
gcloud config set project <your_project_id>
gcloud auth application-default set-quota-project <your_project_id>
```

You'll also need to install [Terraform](https://developer.hashicorp.com/terraform/install) and the [`gcloud` CLI](https://cloud.google.com/sdk/docs/install).

*Note*: The deployment requires Terraform 1.7 or higher.

## Terraform Deployment

1. Clone the GitHub repo.

1. In [Cloud Shell](https://cloud.google.com/shell/docs/using-cloud-shell) navigate to the git repo root.

1. Run the following to start the Terraform deployment:
```sh
# Move to the infra folder.
cd infra/

export USER_PROJECT_OVERRIDE=true
export GOOGLE_BILLING_PROJECT=$(gcloud config get project)

terraform init
terraform apply -var=project_id=$(gcloud config get project)
```

### Terraform variables
You can change any of the default variables values in [variables.tf](variables.tf).

This terraform will generate all configurations files required in the frontend and backend_apis you need to change [variables.tf](variables.tf) values in order to change configuration if needed.

### After Terraform deployment
***Auth Provider***

You need to enable at least one authentication provider in Firebase, you can enable it using the following steps:
1. Go to https://console.firebase.google.com/project/your_project_id/authentication/providers (change the `your_project_id` value)
2. Click on Get Started (if needed)
3 Select Google and enable it
4. Set the name for the project and support email for project
5. Save

## Create Gdrive assets

### Create Gdrive assets
To create gdrive assets you need to execute the following script
```
echo "{}" >> gdrive_folder_results.json
python scripts/create_gdrive_folder.py --folder-name="genai-marketing-assets" --service-account-email=<cloud_run_backend_sa>
```
***Google Drive Configuration (Optional)***

If your Google Workspace has additional restrictions, you may need to grant permissions to the service account created during this execution. This will allow the service account to access and manage files within the designated folder.

1. Go to your folder [drive.google.com](drive.google.com)
2. Select the genai-marketing-assets folder
3. Click on the three dots menu at the right click
4. Select Share, then Share again
5. In the "Add people and groups" field, enter the email address of the service account that was provided as output from the Terraform configuration.
6. Set the permissions for the service account to Editor.
4. Clock Done to share the folder and grant permissions.

#### Update the config file
Before deploy the application you need to update the gdrive configuration values for `drive_folder_id` , `slides_template_id`, `doc_template_id` and `sheet_template_id` in the the *config.toml* file with the resulting *gdrive_folder_results.json* values.

## Application deployment
To deploy the backend of the application run the following command, you need to check terraform outputs values required for this step.
```
sh scripts/backend_deployment.sh --project $(gcloud config get project) --region <your_region> --sa <cloud_run_backend_sa>
```
Then to deploy the frontent you need to execute:
```
sh scripts/frontend_deployment.sh --project $(gcloud config get project)
```

## Review your enviroment
Once deployment is completed terraform will output relevants resoruces values.

Resulting example outputs:
```sh
backend_deployment = "https://genai-for-marketing-xxxxxxxx.a.run.app"
backend_service_account = "genai-marketing-run@your-project-id.iam.gserviceaccount.com"
frontend_deployment = "https://your-project-id.web.app"
```
You can use the app by accessing to the frontend_deployment URL.

### Deployed resources
This deployment creates all the resources described in the main [README.md](../README.md) file, the following is a list of the created resources:
- Required Google Cloud services
- [BiqQuery](https://console.cloud.google.com/bigquery) Dataset and tables (populating tables with sample data)
- Google Drive folder and templates files
- [Service Account](https://console.cloud.google.com/iam-admin) with the required permissions
- [Search engine and Chat engine](https://console.cloud.google.com/gen-app-builder) with datastores
- [Cloud Run](https://console.cloud.google.com/run) for backend APIs
- Firebase for frontend deployment

### Configuration files
This deployment uses the templates in the [templates/](templates/) diractory to replace all necessary configuration values for the application. After the deployment is complete, you can review the resulting values in the config.toml and enviroments.ts files.

## Known Issues


### Error creating service account key
```
Error creating service account key: googleapi: Error 400: Key creation is not allowed on this service account. 
```

**Resolution**: Disable the disableServiceAccountKeyCreation organization policy in your project.
```
gcloud resource-manager org-policies disable-enforce constraints/iam.disableServiceAccountKeyCreation --project $(gcloud config get project)
```

After this run the `terraform apply` command again. Note that fixing this may fix other issues with your deployment.

After the service account is successfully created, you should consider reenabling this organization policy:
```
gcloud resource-manager org-policies enable-enforce constraints/iam.disableServiceAccountKeyCreation --project $(gcloud config get project)
```

### Error creating Database
```
Error creating Database: googleapi: Error 400: Database ID '(default)' is not available in project 'your_project_id'. Please retry in 134 seconds.
```
**Resolution**: This issue occurred because you were repeatedly creating and deleting the Firestore database. To resolve this, you can either:

1. Wait:  Firestore has built-in mechanisms to handle this.  Wait a few minutes, and the system should automatically resolve the conflict.

2. Manual Deletion (If Necessary): If the problem persists, you may need to manually delete the Firestore database through the Google Cloud Console. Please note that this will erase all data within the database.