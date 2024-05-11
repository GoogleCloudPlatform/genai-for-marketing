# Terraform deployment
Terraform deployment simpliefies the deployment of this solution and can be used as blueprint of the solution, it includes all requirements in order to deploy in a single terraform scripts the.

*Note*: Current version of the Terraform Google Cloud provider has not been updated to generate some of the GenAI resources, this soultion uses null_resource to create some resources using Google Cloud SDK.

## Prerequisites:

Previous to execute terraform you need to enable some services using the following steps:

### Enable Firebase
Will be used for the frontend deployment

1. Go to https://console.firebase.google.com/
2. Select add project and load your Google Cloud Platform project
3. Add Firebase to one of your existing Google Cloud projects
4. Confirm Firebase billing plan
5. Continue and complete

### Enable Vertex AI Agent Builder
Required before start using App Builder services
1. Go to https://console.cloud.google.com/gen-app-builder/start
2. Accept TOS


## Terraform deployment

From [Cloud Shell](https://cloud.google.com/shell/docs/using-cloud-shell) run the following commands:

*Note*: This deployment requires Terraform 1.7 or higher

```sh
# move to the tf folder
cd tf/

export USER_PROJECT_OVERRIDE=true
export GOOGLE_BILLING_PROJECT=<your_project_id>

terraform init
terraform apply -var=project_id=<your_project_id>
```

### Terraform variables
You can change any of the default variables values in [variables.tf](variables.tf).

This terraform will generate all configurations files required in the frontend and backend_apis you need to change [variables.tf](variables.tf) values in order to change configuration if needed.

### After Terraform deployment
You need to enable at least one authentication provider in Firebase, you can enable it using the following steps:
1. Go to https://console.firebase.google.com/project/your_project_id/authentication/providers (change the `your_project_id` value)
2. Select Google and enable it
3. Set the name for the project and support email for project
4. Save

## Check your deployment
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
This deployment uses the tempaltes in the [templates/](templates/) diractory to replace all necessary configuration values for the application. After the deployment is complete, you can review the resulting values in the config.tomal and enviroments.ts files.
