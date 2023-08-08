# Generative AI for Marketing using Google Cloud

This repository contains the deployment guide for a demonstration of how to use generative AI from Google Cloud in marketing use cases. It provides step-by-step instructions on how to set up and use the generative AI tools, as well as examples of how they can be used to create marketing content, such as blog posts and social media posts.  

Supplementary Jupyter notebooks are also provided for reference purposes, to help users understand the concepts covered in the demo.

The following is the architecture of all the demos implemented in this application.  
![Architecture](/images/architecture.png "Architecture")


## Repository structure

```
.
├── app
└── notebooks
```

- [`/app`](https://github.com/leiterenato/genai-demos/tree/main/demo_genai_marketing/app): Source code for demo app.  
- [`/notebooks`](https://github.com/leiterenato/genai-demos/tree/main/demo_genai_marketing/notebooks): Sample notebooks demonstrating the concepts covered in this demonstration.  


## Demonstrations

The following demonstrations are provided in this repository:

**1. Marketing Insights**: Visualize Looker Dashboards with marketing data and create personalized marketing materials such as headlines, product descriptions, email campaigns, visuals, etc. This can help businesses to reach their target audience more effectively and improve their conversion rates.  
**2. Email Copy Generation**: Generate persuasive and engaging email messages that are designed to drive a desired outcome, such as increasing sales, generating leads, or building brand awareness. These emails include text and visuals.  
**3. Blog post generation**: Automatically create blog posts on a wide range of topics and in a variety of styles. These articles include text and visuals.  
**4. Trendspotting**: Identify emerging trends in the market by analyzing Google Trends data on a Looker Dashboard and summarizing news related to top search terms. This can help businesses to stay ahead of the competition and to develop products and services that meet the needs of their customers.  
**5. Audience and Insight finder**: Create a conversational interface with data by translating from natural language to SQL queries. This can help businesses to make better decisions by providing them with insights into their data accurately.  
**6. Content Search**: Improve the search experience for enterprise users with Gen App Builder. This can help businesses to find the information they need more quickly and easily.  
**7. Image Generation**: Create realistic images from text descriptions. This can be used for a variety of purposes, such as creating product mockups, generating marketing materials, or creating custom artwork.  
**8. Text Generation**: Create a variety of text content, such as blog posts, articles, and product descriptions. This can help businesses to save time and money on content creation, and it can also help them to produce higher-quality content.


## Notebooks

The following notebooks were created to elucidate the concepts discussed in the demonstration from this repository:
- [Getting Started](https://github.com/leiterenato/genai-demos/blob/main/demo_genai_marketing/notebooks/1_environment_setup.ipynb) (1_environment_setup.ipynb): This notebook is part of the deployment guide and helps with dataset preparation.
- [Data Q&A with PaLM API (Codey) and GoogleSQL](https://github.com/leiterenato/genai-demos/blob/main/demo_genai_marketing/notebooks/data_qa_with_sql.ipynb) (data_qa_with_sql.ipynb): Translate questions using natural language to GoogleSQL to interact with BigQuery.
- [News summarization with LangChain agents and Vertex AI PaLM text models](https://github.com/leiterenato/genai-demos/blob/main/demo_genai_marketing/notebooks/news_summarization_langchain_palm.ipynb) (news_summarization_langchain_palm.ipynb): Summarize news articles related to top search terms using LangChain agents and the ReAct concept.
- [News summarization with PaLM API](https://github.com/leiterenato/genai-demos/blob/main/demo_genai_marketing/notebooks/simple_news_summarization.ipynb) (simple_news_summarization.ipynb): News summarization related to top search terms using the PaLM API.


The following additional (external) notebooks provide supplementary information on the concepts discussed in this repository:
- [Tuning and deploy a foundation model](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/examples/tuning/getting_started_tuning.ipynb): This notebook demonstrates how to tune a model with your dataset to improve the model's response. This is useful for brand voice because it allows you to ensure that the model is generating text that is consistent with your brand's tone and style.
- [Document summarization techniques](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/examples/document-summarization/README.md): Two notebooks explaining different techniques to summarize large documents.
- [Document Q&A](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/examples/document-qa/README.md): Two notebooks explaining different techniques to do document Q&A on a large amount of documents.
- [GenApp Builder - Web search](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gen-app-builder/search-web-app): This demo illustrates how to search through a corpus of documents using Enterprise Search on Generative AI App Builder. Additional features include how to search the public Cloud Knowledge Graph using the Enterprise Knowledge Graph API.
- [GenApp Builder - Document search](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gen-app-builder/retrieval-augmented-generation): This demo illustrates how Enterprise Search and the Vertex AI PaLM API help ensure that generated content is grounded in validated, relevant and up-to-date information.
- [Getting Started with LangChain and Vertex AI PaLM API](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/examples/langchain-intro/intro_langchain_palm_api.ipynb): Use LangChain and Vertex AI PaLM API to generate text.


## Environment Setup

This section outlines the steps to configure the Google Cloud environment that is required in order to run the notebooks and demonstration provided in this repository.  

 - You use a user-managed instance of Vertex AI Workbench as your development environment and the primary interface to Vertex AI services.
 - You use BigQuery to store data from Marketing Platforms and Dataplex to store their metadata.
 - You use Enterprise Search (GenApp Builder) to create a search engine for an external website.


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

- Please deploy refer to this infobot doc to build your own infobot and get the html widget code from intgration section
- https://cloud.google.com/dialogflow/cx/docs/concept/generative-agent
- Please replace the infobot in the utils_config.py with your own infobot
- We used ads helper portal as our backend data sources and use LLMs to generate answers where there is no answer found

## Getting help

If you have any questions or if you found any problems with this repository, please report through GitHub issues.
