# Infrastructure Deployment
Terraform simplifies deploying Generative AI for Marketing. The Terraform deployment includes all necessary requirements.

*Note*: The Terraform Provider for Google Cloud is not able to generate some of the GenAI resources, `null_resource` is used to create some resources using the Google Cloud SDK.

You'll need to create a Google Cloud project and link a billing account before you begin. **It is strongly recommended you deploy Generative AI for Marketing in it's own fresh project.** Existing resources in a project may be impacted by the deployment, and the deployment itself may fail.

## Step 0 - Prerequisites:

Before executing Terraform, follow these steps to enable some services:

### Enable Firebase
Will be used for the frontend deployment

1. Go to https://console.firebase.google.com/.
2. Select "Create a project" and enter the name of your Google Cloud Platform project, then click "Continue". 
3. If you're using Firebase for the first time, you'll have to add Firebase to one of yor existing Google Cloud projects and confirm the Firebase billing plan.
4. When prompted to set up Google Analytics respond as you'd like.
5. Continue and complete.

### Enable Vertex AI Agent Builder
Required before starting using Vertex AI Agent Builder services.
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

### Ensure Workspace is Set Up and You Have Access

Generative AI for Marketing requires your organization has Workspace set up and you have an account before proceeding.

## Step 1 - Terraform Deployment

1. Clone the GitHub repo.

1. In [Cloud Shell](https://cloud.google.com/shell/docs/using-cloud-shell) navigate to the git repo root.

1. In the cloned project root, run the following to start the Terraform deployment:
```sh
# Move to the infra folder.
cd infra/

export USER_PROJECT_OVERRIDE=true
export GOOGLE_BILLING_PROJECT=$(gcloud config get project)

terraform init
terraform apply -var=project_id=$(gcloud config get project)
```

When `terraform apply` completes successfully, you'll see a message `Apply complete!` along with outputs specifying config values. Save this output somewhere, you'll need these values later.

TODO: More details about what to do with the output variables from terraform apply.

### Terraform Variables
TODO: explain this better.

You can change any of the default variables values in [variables.tf](variables.tf).

This terraform will generate all configurations files required in the frontend and backend_apis you need to change [variables.tf](variables.tf) values in order to change configuration if needed.

## Step 2 - Firebase Auth Provider

After the Terraform deployment successfully completes, enable at least one authentication provider in Firebase. You can enable it using the following steps:
1. Go to https://console.firebase.google.com/project/your_project_id/authentication/providers (change the `your_project_id` value).
2. Click on Get Started (if needed).
3. Select Google and flip the enable switch on.
4. Set the name for the project and the support email.
5. Click the "Save" button.

## Step 3 - Setup Google Drive
(TODO: explain this better)

### Create Folder and Upload Files
Execute the following script from the `infra` subfolder:

TODO: better instructions around `cloud_run_backend_sa`, it comes out of the terraform apply.
TODO: explain better what happens here. the folder needs to be created, yes? do the templates also need to be created?
```
echo "{}" >> gdrive_folder_results.json
python scripts/create_gdrive_folder.py --folder-name="genai-marketing-assets" --service-account-email=<cloud_run_backend_sa>
```
### Grant Backend Service Account Google Drive Access

TODO: fix this after determining how the values output by the terraform apply are handled.

In most Workspace setups, the Generative AI for Marketing application needs to be granted access to the Google Drive folder you just created. To do this,  [share the folder](https://support.google.com/drive/answer/7166529?hl=en&co=GENIE.Platform%3DDesktop#zippy=%2Cshare-with-specific-people) with the service account created for the application backend during the Terraform installation. This will allow the service account to access and manage files within the designated folder.

1. In your web browser, open [drive.google.com](https://drive.google.com/drive/my-drive).
2. Find the folder created in the previous step (default is genai-marketing-assets).
3. Click on the three dots menu at the far right of the row with the folder.
4. Highlight "Share" in the menu that pops up, then click "Share" in the submenu.
5. In the "Add people, groups, and calendar events" field, enter the email address of the service account (`cloud_run_backend_sa`) that was provided as output from the Terraform configuration.
6. Set the permissions for the service account to "Editor".
4. Clock "Send" to share the folder and grant permissions. If a popup appears asking for confirmation, click "Share anyway".

## Step 4 - Application Deployment

#### Update `config.toml`

TODO: explain this better, like what the config file is. 

Configuration for the backend of the application is stored in `backend_apis/app/config.toml`. Edit this file and update it with values generated during the deployment process. These instructions use `nano` but use whatever editor you prefer. From the `/infra` directory:

1. Run `cat gdrive_folder_results.json` and copy the output to somewhere outside of your Cloud Shell window. You'll see configuration values for `drive_folder_id` , `slides_template_id`, `doc_template_id` and `sheet_template_id`. These will go into `config.toml`.
1. Run `nano ../backend_apis/app/config.toml`
1. Press ctrl+w to find `drive_folder_id` and you'll see where to enter the 4 configuration values.
1. After updating the configuration values, press ctrl+x to exit then Y to save and enter to confim.

## Application Deployment
To deploy the backend of the application run the following command from the `/infra` folder. You need to use values output by `terraform apply` for this step.

TODO: make this less unpleasant to do with the values output by terraform apply.

TODO: change to use an SA besides the compute engine default and grant it the necessary permissions. 
```
sh scripts/backend_deployment.sh --project $(gcloud config get project) --region <your_region> --sa <cloud_run_backend_sa>
```

In a fresh project, you'll be asked to create an Artifact Registry Docker repoitory. Enter `Y` to confirm.

Then to deploy the frontent you need to execute:
```
sh scripts/frontend_deployment.sh --project $(gcloud config get project)
```

## Review Your Enviroment
Once deployment is completed terraform will output relevants resoruces values.

Resulting example outputs:
```sh
backend_deployment = "https://genai-for-marketing-xxxxxxxx.a.run.app"
backend_service_account = "genai-marketing-run@your-project-id.iam.gserviceaccount.com"
frontend_deployment = "https://your-project-id.web.app"
```
You can use the app by accessing to the frontend_deployment URL.

### Deployed Resources
This deployment creates all the resources described in the main [README.md](../README.md) file, the following is a list of the created resources:
- Required Google Cloud services
- [BiqQuery](https://console.cloud.google.com/bigquery) Dataset and tables (populating tables with sample data)
- Google Drive folder and templates files
- [Service Account](https://console.cloud.google.com/iam-admin) with the required permissions
- [Search engine and Chat engine](https://console.cloud.google.com/gen-app-builder) with datastores
- [Cloud Run](https://console.cloud.google.com/run) for backend APIs
- Firebase for frontend deployment

### Configuration Files
This deployment uses the templates in the [templates/](templates/) diractory to replace all necessary configuration values for the application. After the deployment is complete, you can review the resulting values in the config.toml and enviroments.ts files.

## Known Issues

Workarounds for known issues.

Note that some of the workarounds require modifying [organization policies](https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-policies), which can only be done by a user with the [`orgpolicy.policyAdmin`](https://cloud.google.com/iam/docs/understanding-roles#orgpolicy.policyAdmin) role. If you have an Google Cloud organization administrator, you should work with them on issues requiring organization policy changes.

### Errors During Terraform Deployment

#### `Error creating service account key`

TODO: also look into enable/disable of disableServiceAccountCreation (not Key) constraints/iam.disableServiceAccountCreation
```
Error creating service account key: googleapi: Error 400: Key creation is not allowed on this service account. 
```

**Resolution**: Disable the disableServiceAccountKeyCreation organization policy in your project.
```
gcloud resource-manager org-policies disable-enforce constraints/iam.disableServiceAccountKeyCreation --project $(gcloud config get project)
```

After this run the `terraform apply` command again. Note that fixing this may fix other errors that were raised during deployment.

After the service account is successfully created, you should consider reenabling this organization policy:
```
gcloud resource-manager org-policies enable-enforce constraints/iam.disableServiceAccountKeyCreation --project $(gcloud config get project)
```

#### `Error applying IAM policy for cloud service`
```
Error setting IAM policy for cloudrun service: googleapi: Error 400: One or more users named in the policy do not belong to a permitted customer, perhaps due to an organization policy.
```

**Resolution**: Disable the iam.allowedPolicyMemberDomains organizational policy in your project.
```
TODO: provide command
```

After this run the `terraform apply` command again. Once the error is resolved, you should reenable this organization policy:
```
TODO: provide command
```

#### `Error creating Database`
```
Error creating Database: googleapi: Error 400: Database ID '(default)' is not available in project 'your_project_id'. Please retry in 134 seconds.
```
**Resolution**: This issue occurred because you were repeatedly creating and deleting the Firestore database. To resolve this, you can either:

1. Wait:  Firestore has built-in mechanisms to handle this.  Wait a few minutes, and the system should automatically resolve the conflict.

2. Manual Deletion (If Necessary): If the problem persists, you may need to manually delete the Firestore database through the Google Cloud Console. Please note that this will erase all data within the database.

### Errors Setting Up Google Drive

#### `FileNotFoundError`
```
FileNotFoundError: [Errno 2] No such file or directory: PATH_TO_SOME_FILE
```

**Resolution**: When running `create_gdrive_folder.py`, make sure you are running from the `infra` subdirectory.