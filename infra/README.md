# Infrastructure Deployment
Terraform simplifies deploying Generative AI for Marketing. The Terraform deployment includes all necessary requirements.

*Note*: The Terraform Provider for Google Cloud is not able to generate some of the GenAI resources, `null_resource` is used to create some resources using the Google Cloud SDK.

You'll need to create a Google Cloud project and link a billing account before you begin. **It is strongly recommended you deploy Generative AI for Marketing in its own, new project.** Existing resources in a project may be impacted by the deployment, and the deployment itself may fail.

These instructions have been tested as run by a Google Cloud user with the [Owner role](https://cloud.google.com/iam/docs/understanding-roles#basic) for the project, installation may not work if the installing user does not have the Owner role.

In certain Google Cloud Organizations, organization policies may block installation steps. The [Known Issues](#known-issues) section provides help changing these policies, which requires the [Organization Administrator Role](https://cloud.google.com/resource-manager/docs/access-control-org#using_predefined_roles).

Make sure you have sufficient free space in your terminal environment before you begin installation--4GB is recommended. Having insufficient free space can cause installation steps to fail in a state that makes recovery especially difficult. This is especially important when installing the frontend, which requires a large number of npm packages.

If you encounter problems during deployment see the [Known Issues](#known-issues) section for workarounds to common issues.

## Step 0 - Prerequisites:
> [!CAUTION]
Before executing Terraform, follow these steps to enable some services:


### Enable Firebase
The frontend of Generative AI for Marketing is hosted on Firebase. Before beginning deployment, you need to enable Firebase.

1. Go to https://console.firebase.google.com/.
2. Select "Create a project" and enter the name of your Google Cloud Platform project, then click "Continue".
3. If you're using Firebase for the first time, you'll have to add Firebase to one of yor existing Google Cloud projects and confirm the Firebase billing plan.
4. When prompted to set up Google Analytics respond as you'd like.
5. Continue and complete.

### Enable Vertex AI Agent Builder
The chat agent and search features of Generative AI for Marketing require Vertex AI Agent Builder.
1. Go to https://console.cloud.google.com/gen-app-builder/start .
2. Click the button to accept TOS and enable.

### (Optional) Local Configuration

Cloud Shell is the recommend environment for running the deployment. If you are deploying from outside Cloud Shell, set up your Google Cloud SDK Credentials:

```shell
PROJECT_ID=<your_project_id>
gcloud config set project $PROJECT_ID
gcloud auth application-default login --scopes='https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/drive,openid,https://www.googleapis.com/auth/userinfo.email'
gcloud auth application-default set-quota-project $PROJECT_ID
```

You'll also need to install [Terraform](https://developer.hashicorp.com/terraform/install) and the [`gcloud` CLI](https://cloud.google.com/sdk/docs/install).

> [!IMPORTANT]
>  The deployment requires Terraform 1.9 or higher.

### Ensure Workspace is Set Up and You Have Access

Generative AI for Marketing requires your organization has [Google Workspace](https://workspace.google.com/lp/business/) set up and you have an account before proceeding.

## Step 1 - Terraform Deployment

1. Clone the GitHub repo.

1. In [Cloud Shell](https://cloud.google.com/shell/docs/using-cloud-shell) navigate to the git repo root.

1. Run `gcloud config set project <your_project_id>` to ensure you're installing into the expected project.

1. In the cloned project root, choose one of the provided variables sample. I.E. Automotive or Fashion. Copy the example in terraform.tfvars and adjust the needed variables.
> [!IMPORTANT]
You need at least to populate correctly the **project_id** variable

> [!TIP]
The file `terraform.tfvars` contains a lot of tweaks which  will make this demo more aderent to your needs.
We suggest to not modify all the variables all at once.
You can run this terraform and the following steps as many time as you need.

```bash
cd infra/
cp terraform.tfvars.automotive.sample terraform.tfvars
nano terraform.tfvars
```

1. run the following to start the Terraform deployment:
```bash
# Init plan and Apply your terraform.
terraform init
terraform plan
terraform apply
```

When `terraform apply` completes successfully, you'll see a message `Apply complete!` along with outputs specifying config values. Save this output somewhere, you'll need these values later.

## Step 2 - Firebase Auth Provider

After the Terraform deployment successfully completes, enable at least one authentication provider in Firebase. You can enable it using the following steps:

1. Go to https://console.firebase.google.com/project/your_project_id/authentication/providers (change the `your_project_id` value in this URL to your project ID).
2. Click on Get Started (if needed).
3. Select Google and flip the enable switch on.
4. Set the name for the project and the support email.
5. Click the "Save" button.

## Step 3 - Setup Google Drive

Generative AI for Marketing Uses Google Drive to store created marketing materials. This step creates a Google Drive folder, populates it with templates for the marketing materials, and then returns Google Drive IDs for these templates (you'll need these later). You'll then give the Generative AI for Marketing application access to the Google Drive folder.

### Grant Backend Service Account Google Drive Access

In most Workspace setups, the Generative AI for Marketing application needs to be granted access to the Google Drive folder you just created. To do this,  [share the folder](https://support.google.com/drive/answer/7166529?hl=en&co=GENIE.Platform%3DDesktop#zippy=%2Cshare-with-specific-people) with the service account created for the application backend during the Terraform installation. This will allow the service account to access and manage files within the designated folder.

1. In your web browser, open [drive.google.com](https://drive.google.com/drive/my-drive).
2. Find the folder created in the previous step (default is genai-marketing-assets).
3. Click on the three dots menu at the far right of the row with the folder.
4. Highlight "Share" in the menu that pops up, then click "Share" in the submenu.
5. In the "Add people, groups, and calendar events" field, enter the email address of the service account (`cloud_run_backend_sa`) that was provided as output from the `terraform apply`.
6. Set the permissions for the service account to "Editor".
4. Clock "Send" to share the folder and grant permissions. If a popup appears asking for confirmation, click "Share anyway".

## Step 4 - Application Deployment

### Vertex AI Agent Builder Datastores.
The automated deployment process created all resources to enable the use of Vertex AI Search service with a Dialogflow CX Agent. However, additional steps are required to complete the process of providing the chat agent with data to use on the Frontend:

1. **Indexing Data:** Two data stores were created during the automation deployment; `Website` type for indexing information from your already existing website (if applicable) and `Unstructured data` type for indexing information from files like PDFs into Google Cloud Storage (GCS), this is what we'll be doing.  To learn more about Agent Builder data stores, see [here](https://console.cloud.google.com/gen-app-builder/data-stores).

    > **IMPORTANT:** Indexing data from a website requires domain verification of your website in order to use the advanced features. Domain verification is **out of scope for this demo** but you can find the steps [here](https://cloud.google.com/generative-ai-app-builder/docs/domain-verification).

   Follow steps below:

    1.  **GCS Bucket Creation:** Create a GCS bucket if you don't have one already. The following steps create a GCS bucket with uniform level access. Change the value of `BUCKET_LOCATION` otherwise it will be deployed to `us-central1`.

        ```bash
        export PROJECT_ID=$(gcloud config get project)
        export BUCKET_NAME="$PROJECT_ID-vais-unstructured-data"
        export BUCKET_LOCATION="us-central1"
        export STORAGE_CLASS="STANDARD"

        gcloud config set project $PROJECT_ID
        gcloud storage buckets create gs://$BUCKET_NAME --project=$PROJECT_ID --default-storage-class=$STORAGE_CLASS --location=$BUCKET_LOCATION --uniform-bucket-level-access
        ```

    1.  **Copying Data:** We need to copy over some PDFs - Alphabet Earnings Reports from 2004 to 2023 -  into the newly created bucket using `gsutil`.


        ```
        gsutil -m cp -r "gs://cloud-samples-data-us-central1/gen-app-builder/search/alphabet-investor-pdfs" "gs://$BUCKET_NAME/data"
        ```

        You can also download the folder manually and upload it to your storage account.

    1.  **Indexing Data Store:** Follow instructions [here](https://cloud.google.com/dialogflow/vertex/docs/concept/data-store#cloud-storage) to index the data store with the PDF documents we just copied over.

2. **Add Datastore to Dialogflow CX:** Once the pdf documents are copied over to your GCS bucket and indexed, you need to connect Dialogflow CX agent to your data store. Follow the steps below to do that.
    - **Connect Agent to Data:** Go to your [Dialogflow CX agent](https://dialogflow.cloud.google.com/cx) and click on **Build > Default Start Flow > Start Page**.
    - Under **Data stores**, click on **Edit Data Store** and select your indexed data store from the drop down of type: **Unstructured documents**.
    - Click **Save**.
    - **Test your agent**, from Dialogflow CX UI, to make sure it responds with the right data. Otherwise, ensure you followed all steps above.

3. **Publish Agent:** In order to access your chat agent from the GAIM Frontend, you will need to publish it. Follow steps below:
    - Click on **Publish**.
    - Under **Access**, ensure `Unauthenticated API (anonymous access)` is checked
    - Set your UI style  as **Side Panel**.
    - Finally, click on **Enable the Unauthenticated API**. This will generate some HTML code that can be added to your website to display your agent. You can ignore this as the provided Frontend already has the Chat UI done for you.
    - Now, click **Done** and exit.

### Backend Deployment
To deploy the backend of the application run the following command from the `/infra` folder. You need to use values output by `terraform apply` (`region` and `cloud_run_backend_sa`, both without quotes and removing `<` and `>`) for this step.

```
sh scripts/backend_deployment.sh --project $(gcloud config get project) --region <region> --sa <cloud_run_backend_sa>
```
In a fresh project, you'll be asked to create an Artifact Registry Docker repoitory. Enter `Y` to confirm.

The backend deployment pushes the backend APIs into a Cloud Run container that will be called by the frontend UI. The APIs are implemented in Python using [FastAPI](https://fastapi.tiangolo.com/).


### Frontend Deployment

The frontend is an Angular application deployed in Firebase.

Please validate that you're logged in with the correct account, and if not, log out and then log in again with the firebase commandline.

```
# To list your existing logins.
firebase login:list
```


Then to deploy the frontend you need to execute from the `/infra` folder:
```
sh scripts/frontend_deployment.sh --project $(gcloud config get project)
```

Once this script completes, Generative AI for Marketing is Deployed!

## Wrapping Up

### Review Your Enviroment

When frontend deployment is complete, the 'Hosting URL' printed in the terminal is your link to the UI. You can also see this value in the `frontend_deployment` value output by `terraform apply`.

The backend is located at the address in the `backend_deployment` value in the `terraform apply` output. It should look something like "https://genai-for-marketing-xxxxxxxx.a.run.app". If you append `/marketing-api/docs` (i.e., "https://genai-for-marketing-xxxxxxxx.a.run.app/marketing-api/docs") to this URL you can access the FastAPI interface for exploring the backend APIs.

### Deployed Resources
The deployment creates all the resources described in the main [README.md](../README.md) file, the following is a list of the created resources:
- Required Google Cloud services
- [BiqQuery](https://console.cloud.google.com/bigquery) Dataset and tables (populating tables with sample data)
- Google Drive folder and templates files
- [Service Account](https://console.cloud.google.com/iam-admin) with the required permissions
- [Search engine and Chat engine](https://console.cloud.google.com/gen-app-builder) with datastores
- [Cloud Run](https://console.cloud.google.com/run) for backend APIs
- Firebase for frontend deployment


## Known Issues

Workarounds for known issues.

Note that some of the workarounds require modifying [organization policies](https://cloud.google.com/resource-manager/docs/organization-policy/creating-managing-policies), which can only be done by a user with the [`orgpolicy.policyAdmin`](https://cloud.google.com/iam/docs/understanding-roles#orgpolicy.policyAdmin) role. If you have an Google Cloud organization administrator, you should work with them on issues requiring organization policy changes.

### Errors During Terraform Deployment

#### `Error creating service account key`

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

#### `Error setting IAM policy for cloud service`
```
Error setting IAM policy for cloudrun service: googleapi: Error 400: One or more users named in the policy do not belong to a permitted customer, perhaps due to an organization policy.
```

**Resolution**: Disable the iam.allowedPolicyMemberDomains organizational policy in your project.

First, you need to create a policy file, replace the `<your_project_number>` with your project number:
```yaml
# policy.yaml
name: projects/<your_project_number>/policies/iam.allowedPolicyMemberDomains
spec:
  rules:
  -  allowAll: true
  inheritFromParent: true
```
and then apply the policy:
```
`gcloud org-policies set-policy policy.yaml`
```
After this run the `terraform apply` command again. It may take a few minutes for the policy change to take effect, if you keep getting errors wait a few minutes and retry. Once the error is resolved, you should reenable this organization policy:
```
gcloud resource-manager org-policies delete constraints/iam.allowedPolicyMemberDomains --project $(gcloud config get project)

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
