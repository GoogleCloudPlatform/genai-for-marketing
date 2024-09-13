# Infrastructure Manual Setup

This section outlines the steps to configure the Google Cloud environment that is required in order to run the code provided in this repository.  
You will be interacting with the following resources:
 - **BigQuery** - This is utilized to house data from Marketing Platforms, while Dataplex is employed to keep their metadata.  
 - **Vertex AI Search & Conversation** - This is used to construct a search engine for an external website.  
 - **Workspace (Google Slides, Google Docs and Google Sheets)** - This is used to visualize the resources generated by the user.

> **NOTE:** All commands below will be ran from [Cloud Shell](https://cloud.google.com/shell/docs/using-cloud-shell) directly from the Google Cloud Project.


### 1. Select a Google Cloud project

Navigate to the Google Cloud Console and [select or create a project](https://console.cloud.google.com/projectselector2) from the project selector page.  
> **NOTE:** This is just a DEMONSTRATION. You must be a the project owner in order to set up the environment requirements.

### 2. From Cloud Shell, Set Project, Location and Credentials
From a [Cloud Shell](https://cloud.google.com/shell/docs/using-cloud-shell) terminal, replace `<YOUR_PROJECT_ID>` and `<LOCATION>` to the project ID and location where your resources will be deployed.

> **NOTE:** Authenticate with the same user that has EDITOR/OWNER rights to this project.

 - Set your project id.  
 
```bash
export PROJECT_ID=<YOUR_PROJECT_ID>  
export LOCATION=<LOCATION>  
gcloud config set project $PROJECT_ID  
```

 - Follow the web flow instructions to acquire new Application Default Credentials (ADC). 
```bash 
gcloud auth application-default login 
```

 - Set the Quota Project
```bash
gcloud auth application-default set-quota-project $PROJECT_ID
```



### 3. Enable the required services

From [Cloud Shell](https://cloud.google.com/shell/docs/using-cloud-shell), run the following commands to enable the required Cloud APIs. 

> **NOTE:** Google Cloud enables a maximum batch size of 20 services at a time, hence, we'll break this down into two commands.

```bash 
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
```


```bash
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
```

### 4. Clone the Gen AI for Marketing repository
From Cloud Shell, execute the following command:

> git clone https://github.com/GoogleCloudPlatform/genai-for-marketing  


### 5. Update the configuration with information of your project

From the terminal, using your favorite editor, open the [configuration file](/backend_apis/app/config.toml) and include your project id (line 16) and location (line 17).


### 6. Prepare BigQuery and Dataplex
Navigate to [/installation_scripts](/installation_scripts), install the python packages and execute the following script.  

> **NOTE:** Make sure you have set the environmental variables `PROJECT_ID` and `LOCATION`.  

```bash
cd ./genai-for-marketing/installation_scripts  
pip3 install -r requirements.txt  
```

Run the following python script to create the **BigQuery** dataset and the **DataCatalog** TagTemplate.    

```bash
python3 1_env_setup_script.py  
```

If you receive a `409 POST error`, please check if the cdp_database already exists in Bigquery. 


### 7. Create a Vertex AI Search engine for a public website

Follow the steps below to create a search engine for a website using Vertex AI Search.
 - Enable the Vertex AI Agent Builder, BigQuery, Cloud Storage APIs. 

 ```bash
  gcloud services enable \
    discoveryengine.googleapis.com \
    cloudresourcemanager.googleapis.com \
    bigquery.googleapis.com \
    storage-component.googleapis.com
 ```

 - Activate Vertex AI Search [here](https://cloud.google.com/generative-ai-app-builder/docs/try-enterprise-search#activate).  

 - Create the website search engine as described [here](https://cloud.google.com/generative-ai-app-builder/docs/try-enterprise-search#create_a_search_app_for_website_data)

    > **NOTE:** Creation of your data store and app can take up to 5 minutes.
 - Once the datastore and app are created, then you can preview the search engine [here](https://cloud.google.com/generative-ai-app-builder/docs/try-enterprise-search#preview_your_app_for_website_data).

 - After your Vertex AI Search datastore is created, navigate back to the [`Apps`](https://console.cloud.google.com/gen-app-builder/engines) page and copy the ID of the datastore you just created.  
Example:  
![Vertex AI Search ID](./app/images/es_id.png)

Open the [configuration file - line 33](/backend_apis/app/config.toml) and include the datastore ID. 
**Don't forget to save the configuration file.**

**Important**: Alternatively, you can create a [search engine for structure or unstructured data](https://cloud.google.com/generative-ai-app-builder/docs/try-enterprise-search#before-you-begin).

### 8. Add your Looker Dashboards

In order to render your Looker Dashboards in the Marketing Insights and Campaing Performance pages, you need to update a HTML file with links to them.

1) For Marketing Insight dashboards, open the [marketing-insights.component.html file](/frontend/src/app/marketing-insights/marketing-insights.component.html) and include links to your Looker dashboards on lines `18` and `28`.  

Example:
 - Add a new line after line 18 (or replace line 18) and include the title and ID of your Looker Dashboard.
> <option value="Overview">Overview</option>

 - For each dashboard id/title you included the step above, include a link to it at the end of this file.
> <div *ngIf="overview" class="overviewcss">
>  <iframe width="1000" height="1000" src="https://googledemo.looker.com/embed/dashboards/2131?allow_login_screen=true" ></iframe>
> </div>

The `allow_login_screen=true` in the URL will open the authentication page from Looker to secure the access to your account.

3) Just like above, for Campaign Performance dashboards, open the [campaign-performance.component.html file](/frontend/src/app/campaign-performance/campaign-performance.component.html) and include links to your Looker dashboards on lines `27` and `37`.

**[Optional]** If you have your Google Ads and Google Analytics 4 accounts in production, you can deploy the [`Marketing Analytics Jumpstart`](https://github.com/GoogleCloudPlatform/marketing-analytics-jumpstart) solution to your project, build the Dashboards and link them to the demonstration UI.  


### 9. Create a Generative AI DataStore Agent

Next you will create a Generative AI Agent that will assist the users to answer questions about Google Ads, etc.  
- Follow the steps described in this [Documentation](https://cloud.google.com/dialogflow/vertex/docs/concept/data-store-agent) to build your own Datastore Agent.  
  - Execute these steps in the same project you deployed the above steps of this demo.  
- Enable [Dialogflow Messenger integration](https://cloud.google.com/dialogflow/cx/docs/concept/integration/dialogflow-messenger) and copy the `agent-id` from the HTML code snippet provided by the platform.  
  - The HTML code snippet looks like this: 
  ![HTML Code](/app/images/dialogflow-integration.png "HTML Code")  
- Open the [frontend/src/environments/environments.ts file](/frontend/src/environments/environments.ts#L3) and replace the variable `dialogFlowCxAgendId` with the `agent-id` on line `117`.  


### 10. Workspace integration

Follow the steps below to setup the Workspace integration with this demonstration.


#### 10.1. Create a service account and upload the content to Secret Manager
- Create a Service Account (SA) in the same project you are deploying the demo and download the JSON API Key. This SA doesn't need any roles / permissions.  
  - Follow this [documentation](https://cloud.google.com/iam/docs/service-accounts-create) to create the service account. Take note of the service account address; it will look like this: `name-of-the-sa@my-project.iam.gserviceaccount.com`.
  - Follow this [documentation](https://cloud.google.com/iam/docs/keys-create-delete#creating) to download the key JSON file with the service account credentials.  
- Upload the content of this Service Account to a Secret in Google Cloud Secret Manager.
  - Follow the steps in the [documentation](https://cloud.google.com/secret-manager/docs/create-secret-quickstart) to accomplish that
  - Open the [backend_apis/app/config.toml file](/backend_apis/app/config.toml) and replace the full path to your Secret in Secret Manager on line `21`. 


> **IMPORTANT**: For security reasons, **DO NOT** push your service account credentials to a public Github repository.

> **NOTE:** For the next steps, leave [backend_apis/app/config.toml file](/backend_apis/app/config.toml) open.


#### 10.2. Change the DOMAIN that folders will be shared with
This demonstration will create folders under Google Drive, Google Docs documents, Google Slides presentations and Google Sheets documents.  
When we create the Drive folder, we set the permission to all users under a specific domain.

 - Once again, open the [backend_apis/app/config.toml file](/backend_apis/app/config.toml) and change line `59` to the domain you want to share the folder (example: mydomain.com).
   > **NOTE:** This should be the same domain where you have Workspace set up.

Be aware that this configuration will share the folder with all the users in that domain.  
If this behavior is not desired, please explore different ways of sharing resources from [this](https://developers.google.com/drive/api/reference/rest/v3/permissions#resource:-permission) documentation  



#### 10.3. Google Drive
 - Navigate to [Google Drive](https://drive.google.com/) and create a folder.  
   - This folder will be used to host the templates and assets created in the demo.
 - Share this folder with the service account address you created in the previous step. Give `"Editor"` rights to the service account. The share will look like this:
![Share Drive](/app/images/workspace-drive.png "Share Drive")
 - Take note of the folder ID from the URL. Go into the folder you created and you will be able to find the ID in the URL. The URL will look like this:
 ![Drive ID](/app/images/workspace-drive0.png)
 - Add your folder ID to the configuration file on line `39` in the [backend_apis/app/config.toml file](/backend_apis/app/config.toml).

 - **IMPORTANT**: Also share this folder with people who will be using the code.


#### 10.4. Google Slides, Google Docs and Google Sheets
 - Copy the content of [templates](/templates) folder to this newly created folder.
 - For the Google Slides template (`Marketing Assets`): 
   - From the Google Drive folder open the file in Google Slides.  
   - In Google Slides, click on `File` and `Save as Google Slides`. Take note of the Slides ID from the URL.
   - Change the **Slides ID** on line `40` in the configuration file [backend_apis/app/config.toml file](/backend_apis/app/config.toml).
 - For the Google Docs template (`Gen AI for Marketing Google Doc Template`): 
   - From the Google Drive folder open the file in Google Docs. 
   - In Google Docs, click on `File` and `Save as Google Docs`. Take note of the Docs ID from the URL.
   - Change the **Docs ID** on line `41` in the configuration file [backend_apis/app/config.toml file](/backend_apis/app/config.toml).
 - For the Google Sheets template (`GenAI for Marketing`):  
   - From the Google Drive folder open the Google Sheets.
   - In Google Sheets, click in `File` and `Save as Google Sheets`. Take note of the Sheets ID from the URL.
   - Change the **Sheets ID** on line `42` in the configuration file [backend_apis/app/config.toml file](/backend_apis/app/config.toml).
 

### 11.  Deploy the APIs to Cloud Run and Firebase Hosting

#### 11.1. Cloud Run
 - Navigate to the [backend_apis](`genai-for-marketing/backend_apis/`) folder  

```bash
  cd ./genai-for-marketing/backend_apis/  
```

 - Open the [Dockerfile](/backend_apis/Dockerfile) and add your project id where indicated on line `20`.
 - Build and deploy the Docker image to Cloud Run.  

```bash
gcloud run deploy genai-marketing \
--source . \
--region us-central1 \
--allow-unauthenticated
```

- Open the [frontend/src/environments/environments.ts file - line 2](/frontend/src/environments/environments.ts) and include the URL to your newly created Cloud Run deployment.  
Example: `https://marketing-image-tlmb7xv43q-uc.a.run.app`  

#### 11.2. Firebase Hosting

**Enable Firebase**
 - Go to https://console.firebase.google.com/
 - Select "Add project" and enter your GCP project id. Make sure it is the same project you deployed the resources so far.
 - Add Firebase to one of your existing Google Cloud projects
 - Confirm Firebase billing plan
 - Continue and complete the configuration


#### 11.3. Firebase Hosting app setup
After you have a Firebase project, you can register your web app with that project.

In the center of the Firebase console's project overview page, click the Web icon (plat_web) to launch the setup workflow.

If you've already added an app to your Firebase project, click Add app to display the platform options.
 - Enter your app's nickname.
 - This nickname is an internal, convenience identifier and is only visible to you in the Firebase console.
 - Click Register app.
 - Copy the information to include in the configuration.

Open the [frontend environment file - line 4](/frontend/src/environments/environments.ts) and include the Firebase information.

#### 11.4. Build Angular Frontend
Angular is the framework for the Frontend. Execute the following commands to build your application.

```bash
npm install -g @angular/cli  
npm install --legacy-peer-deps  

cd ./genai-for-marketing/frontend  

ng build  
```

#### 11.5. Firebase Hosting Setup
Firebase Hosting is used to serve the frontend.

 - Install firebase tools
```bash
npm install -g firebase-tools  

firebase login --no-localhost  
```
Follow the steps presented in the console to login to Firebase.

 - Init hosting
```bash
cd frontend/dist/frontend  

firebase init hosting
```
First type your Firebase project and then type `browser` as the public folder.  
Leave the defaults for the rest of the questions.

 - Deploy hosting
```bash
firebase deploy --only hosting
```
Navigate to the created URL to access the Gen AI for Marketing app.


#### 11.6. Firestore database setup

Visit the following URL to create a database for Firestore.  
Replace `your-project-id` with your project ID.

https://console.cloud.google.com/datastore/setup?project=your-project-id
 - Choose "Native Mode (Recommended)" for the database mode.
 - Click Save


#### 11.7. Enable Firebase Authentication with Google

Visit the following URL to enable Firebase Authentication.  
Replace `your-project-id` with your project ID.
https://console.firebase.google.com/project/your-project-id/authentication/providers

 - Add a new provider by clicking on "Add new provider"
 - Choose "Google" and click "enable" and then "Save".