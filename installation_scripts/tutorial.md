# Setting up Generative AI for Marketing Solution

## Welcome!
Follow this instructions to deploy the Generative AI Marketing solution accelerator within your Project.

To see more details about the solution, components and architecture, please go to the main [README](https://github.com/GoogleCloudPlatform/genai-for-marketing/blob/main/README.md) file.

**Time to complete**: About 20 minutes

Click the **Start** button to move to the next step.

## Prerequisites
Before start please make sure you have the following prerequisites:
- A GCP Project, this can be a standalone project or within a GCP organization. If you need to create a new project please follow the instructions [here](https://cloud.google.com/resource-manager/docs/creating-managing-projects)
- In the Google Cloud console, navigate to the Vertex AI Search and Conversation console.
- Read and agree to the Terms of Service, then click Continue and activate the API.
- A user with permissions to execute the installation script with the following permissions at the project project level:
  - Project IAM Admin
  - Service Usage Admin
  - App Engine Admin
  - Service Account Admin
  - Dialogflow API Admin
  - Discovery Engine Admin
  - Vertex AI Administrator
  - BigQuery Admin
  - Storage Admin
  - Logging Admin

You can asign missing roles or view your current permissions [here](https://console.cloud.google.com/iam-admin/iam)

(Optional) If you are not executing this using cloud shell you will need to install the following:
- python 3.10 or higher
- virtualenv
- [gcloud](https://cloud.google.com/sdk/docs/install)

Make sure you set working project Id by executing: 
```bash
gcloud config set project <project_id>
```
Continue on to the next step to start the deployment process.

## Deployment

### (Optional) Advanced configuration
You can overwrite default parameters as regions or some specific values by editing the <walkthrough-editor-open-file
    filePath="cloud-shell-tutorials/tutorial.md">
    genai_marketing_automation.sh
</walkthrough-editor-open-file> script.

### Start the deployment
Start the deployment using the following command:
```bash
sh installation_scripts/genai_marketing_automation.sh
```

The shell script will prompt you for:
- Company name
- Your domain, ie.: "sample.com/somepath/*", "subdomian.sample.com"
- Your Project ID
- GDrive Folder Name (owned by you), ie: path/to/my/gdrive/folder
- Existing Looker URL
- Vertext Search application name, ie.: "my_app_name" 
- Vertext Conversation application name: "my_chat_app_name"

You can execute this command multiple times using the same parameters to avoid multiple resource creation.


## Post deployment

A few manual tasks are required in order to complete the deployment.

### Dialogflow CX datastore configuration

### (Optional) Domain Verification
The domain that was provided during the deployment process will need to be verified. in case you setup the app chat to use both (Website and Cloud Storage) Datastore
You need to follow the instructions:

1. You can go to Search and conversation [here](https://console.cloud.google.com/gen-app-builder/engines).
2. Click on Data Stores.
3. Select the Website data store (the one with the globe icon).
4. Follow the instructions in red.

Next, you will configure the Dialogflow CX datastore(s) using the following steps:

1. Go to Dialogflow CX [here](https://dialogflow.cloud.google.com/cx/projects)
2. Select your project and agent.
3. Select the Start Page in the Default Start Flow.
4. (Optional) Select your website data store from the data store list.
5. Select your unstructured data store using the GCS folder you provided.
6. Click on Save.

## Review your deployed enviroment

Here listed are all relevant resources that were created.
- [App Engine application](https://dialogflow.cloud.google.com/appengine/services)
- [Search and Conversation apps](https://dialogflow.cloud.google.com/gen-app-builder/engines)
- [BigQuery Datasets](https://dialogflow.cloud.google.com/bigquery)

For a more detailed information please refer to the main [README](https://github.com/GoogleCloudPlatform/genai-for-marketing/blob/main/README.md) file.