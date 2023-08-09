# Generative AI for Marketing using Google Cloud

This repository includes a deployment guide showcasing the application of Google Cloud's generative AI for marketing scenarios. It offers detailed, step-by-step guidance for setting up and utilizing the generative AI tools, including examples of their use in crafting marketing materials like blog posts and social media content.

Additionally, supplementary Jupyter notebooks are provided to aid users in grasping the concepts explored in the demonstration.

The architecture of all the demos that are implemented in this application is as follows.    
![Architecture](/app/images/architecture.png "Architecture")


## Repository structure

```
.
├── app
└── notebooks
```

- [`/app`](https://github.com/leiterenato/genai-demos/tree/main/demo_genai_marketing/app): Source code for demo app.  
- [`/notebooks`](https://github.com/leiterenato/genai-demos/tree/main/demo_genai_marketing/notebooks): Sample notebooks demonstrating the concepts covered in this demonstration.   


## Demonstrations

In this repository, the following demonstrations are provided:  

**Marketing Insights**: Utilize Looker Dashboards to access and visualize marketing data, enabling the creation of tailored marketing materials such as headlines, product descriptions, email campaigns, and visuals. These features can empower businesses to connect with their target audience more efficiently, thereby improving conversion rates.  
**Audience and Insight finder**: Conversational interface that translates natural language into SQL queries. By offering precise insights into data, it assists businesses in making more informed decisions.
**Trendspotting**: Identify emerging trends in the market by analyzing Google Trends data on a Looker Dashboard and summarizing news related to top search terms. This can help businesses to stay ahead of the competition and to develop products and services that meet the needs of their customers.  
**Content Search**: Improve the search experience for enterprise users with Gen App Builder. This can help businesses to find the information they need more quickly and easily.  
**Content Generation**: Craft compelling and captivating email content, website articles, social media updates, and assets for PMax, all aimed at achieving specific goals such as boosting sales, gathering leads, or enhancing brand recognition. This encompasses both textual and visual elements.
**Workspace integration**: Transfer the assets you've generated earlier to Workspace.  


## Notebooks

The notebooks listed below were developed to explain the concepts exposed in this repository:  
- [Getting Started](/notebooks/1_environment_setup.ipynb) (1_environment_setup.ipynb): This notebook is part of the deployment guide and helps with dataset preparation.
- [Data Q&A with PaLM API and GoogleSQL](/notebooks/data_qa_with_sql.ipynb) (data_qa_with_sql.ipynb): Translate questions using natural language to GoogleSQL to interact with BigQuery.
- [News summarization with LangChain agents and Vertex AI PaLM text models](/notebooks/news_summarization_langchain_palm.ipynb) (news_summarization_langchain_palm.ipynb): Summarize news articles related to top search terms using LangChain agents and the ReAct concept.
- [News summarization with PaLM API](/notebooks/simple_news_summarization.ipynb) (simple_news_summarization.ipynb): News summarization related to top search terms using the PaLM API.


The following additional (external) notebooks provide supplementary information on the concepts discussed in this repository:
- [Tuning and deploy a foundation model](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/examples/tuning/getting_started_tuning.ipynb): This notebook demonstrates how to tune a model with your dataset to improve the model's response. This is useful for brand voice because it allows you to ensure that the model is generating text that is consistent with your brand's tone and style.
- [Document summarization techniques](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/examples/document-summarization/README.md): Two notebooks explaining different techniques to summarize large documents.
- [Document Q&A](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/examples/document-qa/README.md): Two notebooks explaining different techniques to do document Q&A on a large amount of documents.
- [GenApp Builder - Web search](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gen-app-builder/search-web-app): This demo illustrates how to search through a corpus of documents using Enterprise Search on Generative AI App Builder. Additional features include how to search the public Cloud Knowledge Graph using the Enterprise Knowledge Graph API.
- [GenApp Builder - Document search](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gen-app-builder/retrieval-augmented-generation): This demo illustrates how Enterprise Search and the Vertex AI PaLM API help ensure that generated content is grounded in validated, relevant and up-to-date information.
- [Getting Started with LangChain and Vertex AI PaLM API](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/examples/langchain-intro/intro_langchain_palm_api.ipynb): Use LangChain and Vertex AI PaLM API to generate text.


# Environment Setup

This section outlines the steps to configure the Google Cloud environment that is required in order to run the notebooks and demonstration provided in this repository.  
You will be interacting with the following resources:
 - A user-managed instance of Vertex AI Workbench serves as your development setting and the main interface to Vertex AI services.  
 - BigQuery is utilized to house data from Marketing Platforms, while Dataplex is employed to keep their metadata.  
 - Enterprise Search and Infobot (GenApp Builder) are used to construct a search engine for an external website.  
 - Workspace (Google Slides, Google Docs and Google Sheets) are used to visualized the resources generated by you.


### Select a Google Cloud project

In the Google Cloud Console, on the project selector page, [select or create a Google Cloud project](https://console.cloud.google.com/projectselector2/home/dashboard?_ga=2.77230869.1295546877.1635788229-285875547.1607983197&_gac=1.82770276.1635972813.Cj0KCQjw5oiMBhDtARIsAJi0qk2ZfY-XhuwG8p2raIfWLnuYahsUElT08GH1-tZa28e230L3XSfYewYaAlEMEALw_wcB). **As this is a DEMONSTRATION, you need to be a project owner in order to set up the environment.**


### Enable the required services

From [Cloud Shell](https://cloud.google.com/shell/docs/using-cloud-shelld.google.com/shell/docs/using-cloud-shell), run the following commands to enable the required Cloud APIs:

```bash
export PROJECT_ID=<YOUR_PROJECT_ID>
 
gcloud config set project $PROJECT_ID
 
gcloud services enable \
  cloudbuild.googleapis.com \
  compute.googleapis.com \
  cloudresourcemanager.googleapis.com \
  iam.googleapis.com \
  container.googleapis.com \
  cloudapis.googleapis.com \
  cloudtrace.googleapis.com \
  containerregistry.googleapis.com \
  iamcredentials.googleapis.com \
  monitoring.googleapis.com \
  logging.googleapis.com \
  notebooks.googleapis.com \
  aiplatform.googleapis.com \
  storage.googleapis.com \
  datacatalog.googleapis.com \
  appengineflex.googleapis.com \
  translate.googleapis.com
```

**Note**: When you work with Vertex AI user-managed notebooks, be sure that all the services that you're using are enabled and white-listed.

### Configure Vertex AI Workbench

Create a user-managed notebooks instance from the command line.
 
**Note**: Make sure that you're following these steps in the same project as before.
 
In Cloud Shell, enter the following command.  
 - For `<YOUR_INSTANCE_NAME>`, enter a name starting with a lower-case letter followed by lower-case letters, numbers or dash sign.  
 - For `<YOUR_LOCATION>`, add a zone (for example, `us-central1-a` or `europe-west4-a`).

```bash
PROJECT_ID=$(gcloud config list --format 'value(core.project)')
INSTANCE_NAME=<YOUR_INSTANCE_NAME>
LOCATION=<YOUR_LOCATION>
gcloud notebooks instances create $INSTANCE_NAME \
     --vm-image-project=deeplearning-platform-release \
     --vm-image-family=common-cpu-notebooks \
     --machine-type=n1-standard-4 \
     --location=$LOCATION
```

Vertex AI Workbench creates a user-managed notebook instance based on the properties that you specified and then automatically starts the instance. When the instance is ready to use, Vertex AI Workbench activates an **Open JupyterLab** link next to the instance name in the [Vertex AI Workbench Cloud Console](https://console.cloud.google.com/vertex-ai/workbench/list/instances) page. To connect to your user-managed notebooks instance, click **Open JupyterLab**.

On Jupyterlab `Launcher Page`, click on `Terminal` to start a new terminal by clicking the Terminal icon.  
Clone the repository to your notebook instance:

> git clone https://github.com/leiterenato/genai-demos.git


### Prepare BigQuery and Dataplex

Open notebook [`/genai-for-marketing/notebooks/1_environment_setup.ipynb`](https://github.com/leiterenato/genai-demos/blob/main/demo_genai_marketing/notebooks/1_environment_setup.ipynb) and follow the instructions in it.  
It will execute the following steps:
 - Install dependecies to run the notebook
 - Create a dataset on BigQuery
 - Load CDP data to BigQuery
 - Create Tag Template on Dataplex
 - Tag dataset columns
 - Test the deployment

Make sure all the steps executed successfully.


### Create an Enterprise Search engine for a public website

Follow the steps below to create a search engine for a website using Enterprise Search.
 - Make sure the Enterprise Search APIs are enabled [here](https://cloud.google.com/generative-ai-app-builder/docs/try-enterprise-search#before-you-begin) and you activated Generative AI App Builder [here](https://cloud.google.com/generative-ai-app-builder/docs/try-enterprise-search#activate).
 - Create and preview the website search engine [here](https://cloud.google.com/generative-ai-app-builder/docs/try-enterprise-search#create_a_website_search_engine) and [here](https://cloud.google.com/generative-ai-app-builder/docs/try-enterprise-search#preview_the_website_search_engine).

After you finished creating the Enterprise Search datastore, navigate back to the [`Apps`](https://console.cloud.google.com/gen-app-builder/engines) page and copy the ID of the datastore you just created.  
Example:  
![Enterprise Search ID](./app/images/es_id.png)

Open this [configuration file - line 33](./app/utils_config.py) and paste the ID of your newly created datastore in the `DATASTORES` dictionary.  
The resulting code should look like this:  

```
# Enterprise Search datastores and location
DATASTORES = {
    'google-ads-support_1688070625722': 'default_config'
}
```

If you have multiple datastores, you can include them in this dictionary using the same format.  
**Don't forget to save the configuration file.**


### Add your Looker Dashboards

In order to render your Looker Dashboards in the UI, you need to update a configuration file with the links to them.

Open this [configuration file - line 27](./app/utils_config.py) and paste the name and link of your Looker Dashboards in the `DASHBOARDS` dictionary.  
The resulting code should look like this: 

```
# Looker Dashboards
# The link of the looker Dashboard must follow this format:
# https://<LOOKER INSTANCE URL>/embed/dashboards/<DASHBOARD NUMBER>?allow_login_screen=true
DASHBOARDS = {
    # Sample Dashboard link
    # 'Overview': 'https://mydomain.looker.com/embed/dashboards/2131?allow_login_screen=true'
}
```

The `allow_login_screen=true` will open the authentication page from Looker to secure the access to your account.

**[Optional]** If you have your Google Ads and Google Analytics 4 accounts in production, you can deploy our [`Marketing Data Engine`](https://github.com/GoogleCloudPlatform/marketing-data-engine/tree/main) solution to your project, build the Dashboards and link them to the demonstration UI.  


### Deploy the demonstration to AppEngine

 - On Jupyterlab `Launcher Page`, click on `Terminal` to start a new terminal by clicking the Terminal icon.  
 - Navigate to `demo_genai_marketing` folder  

> cd demo_genai_marketing

 - Open the [`app.yaml`](./app.yaml) configuration file and include your service account (Compute Engine default service account) in line 19:

 ```
 service_account: <REPLACE WITH YOUR SERVICE ACCOUNT ADDRESS>
 ```

The service account has the following format: `PROJECT_NUMBER-compute@developer.gserviceaccount.com`

You can check the available service accounts by running the following command:  
> gcloud iam service-accounts list

 - Deploy the solution to AppEngine

> gcloud app deploy

Wait for the application to be deployed and open the link generated by AppEngine.

### Add your infobot

- Please refer to this infobot Colab to build your own infobot and get the html widget code from intgration section
- https://codelabs.developers.google.com/codelabs/dialogflow-generator#0
- Please replace the infobot in the utils_config.py with your own infobot
- We used ads helper websites as our backend data sources and use LLMs to generate answers where there is no answer found
- If you have quesionts, please refer to this doc https://cloud.google.com/dialogflow/cx/docs/concept/generative-agent

## Getting help

If you have any questions or if you found any problems with this repository, please report through GitHub issues.

## How to use workspace integration on Review & Activation page
- Enable the workspace APIs that you need for the project - Drive API, Slides API, Docs API, and Sheets API
  - You can refer to this doc: https://developers.google.com/workspace/guides/enable-apis
- Generate an empty Service Account in the project
  - Follow this doc to generate a service account: https://cloud.google.com/iam/docs/service-accounts-create
  - Follow this doc to dowload key json of the service account: https://cloud.google.com/iam/docs/keys-create-delete#creating
  - In utils.config, change SERVICE_ACCOUNT_JSON_KEY to point to your json key
- Create a Google Drive folder and include this service account as Admin
  - Once you do that, repace DRIVE_FOLDER_ID in untils.config with the actual google drive id
- Share this drive with people who need to access the template folder
- Create 3 templates 
  - Google slides template: 
    - Once you do that, repace SLIDES_TEMPLATE_ID in untils.config with the actual google slide id
  - Google doc template: 
    - Once you do that, repace DOC_TEMPLATE_ID in untils.config with the actual google doc id
  - Create doogle sheet template and some data points and charts in it.
    - Once you do that, repace SHEET_TEMPLATE_ID in untils.config with the actual google sheet id
    - Add the slide page ids where you want to insert charts in SLIDE_PAGE_ID_LIST in uitils.config. If the order of the charts is not what you want, feel free to rearrange them in the SLIDE_PAGE_ID_LIST.
