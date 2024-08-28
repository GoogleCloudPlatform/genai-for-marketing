# Generative AI for Marketing using Google Cloud

This repository provides a deployment guide showcasing the application of Google Cloud's Generative AI for marketing scenarios. It offers detailed, step-by-step guidance for setting up and utilizing the Generative AI tools, including examples of their use in crafting marketing materials like blog posts and social media content.

Additionally, supplementary Jupyter notebooks are provided to aid users in grasping the concepts explored in the demonstration.

The architecture of all the demos that are implemented in this application is as follows.    
![Architecture](/app/images/architecture.png "Architecture")


## Repository structure

```
.
├── app
└── backend_apis
└── frontend
└── notebooks
└── templates
└── infra
```

- [`/app`](/app): Architecture diagrams.  
- [`/backend_apis`](/backend_apis): Source code for backend APIs.  
- [`/frontend`](/frontend): Source code for the front end UI.  
- [`/notebooks`](/notebooks): Sample notebooks demonstrating the concepts covered in this demonstration.  
- [`/templates`](/templates): Workspace Slides, Docs and Sheets templates used in the demonstration.  
- [`/infra`](/infra): Infrastructure deployment.


## Demonstrations

In this repository, the following demonstrations are provided:  

* **Marketing Insights**: Utilize Looker Dashboards to access and visualize marketing data, powered by Looker dashboards, marketers can access and visualize marketing data to build data driven marketing campaigns. These features can empower businesses to connect with their target audience more efficiently, thereby improving conversion rates.  
* **Audience and Insight finder**: Conversational interface that translates natural language into SQL queries. This democratizes access to data for non-SQL users removing any bottleneck for marketing teams.  
* **Trendspotting**: Identify emerging trends in the market by analyzing Google Trends data on a Looker dashboard and summarize news related to top search terms. This can help businesses to stay ahead of the competition and to develop products and services that meet the needs and interests of their customers.  
* **Content Search**: Improve search experience for internal or external content with Vertex AI Search for business users.  
* **Content Generation**: Reduce time for content generation with Vertex Foundation Models. Generate compelling and captivating email copy, website articles, social media posts, and assets for PMax. All aimed at achieving specific goals such as boosting sales, generating leads, or enhancing brand awareness. This encompasses both textual and visual elements using Vertex language & vision models.  
* **Workspace integration**: Transfer the insights and assets you've generated earlier to Workspace and visualize in Google Slides, Docs and Sheets.


## Notebooks and code samples

The notebooks listed below were developed to explain the concepts exposed in this repository:  
- [Getting Started](/notebooks/1_environment_setup.ipynb) (/notebooks/1_environment_setup.ipynb): This notebook is part of the deployment guide and helps with dataset preparation.
- [Data Q&A with PaLM API and GoogleSQL](/notebooks/data_qa_with_sql.ipynb) (/notebooks/data_qa_with_sql.ipynb): Translate questions using natural language to GoogleSQL to interact with BigQuery.
- [News summarization with LangChain agents and Vertex AI PaLM text models](/notebooks/news_summarization_langchain_palm.ipynb) (news_summarization_langchain_palm.ipynb): Summarize news articles related to top search terms using LangChain agents and the ReAct concept.
- [News summarization with PaLM API](/notebooks/simple_news_summarization.ipynb) (simple_news_summarization.ipynb): News summarization related to top search terms using the PaLM API.
- [Imagen fine tuning](/notebooks/Imagen_finetune.ipynb) (Imagen_finetune.ipynb): Fine tune Imagen model.

The following additional (external) notebooks provide supplementary information on the concepts discussed in this repository:
- [Tuning and deploy a foundation model](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/tuning/tuning_text_bison.ipynb): This notebook demonstrates how to tune a model with your dataset to improve the model's response. This is useful for brand voice because it allows you to ensure that the model is generating text that is consistent with your brand's tone and style.
- [Document summarization techniques](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/language/use-cases/document-summarization): Two notebooks explaining different techniques to summarize large documents.
- [Document Q&A](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/language/use-cases/document-qa): Two notebooks explaining different techniques to do document Q&A on a large amount of documents.
- [Vertex AI Search - Web search](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/search/web-app): This demo illustrates how to search through a corpus of documents using Vertex AI Search. Additional features include how to search the public Cloud Knowledge Graph using the Enterprise Knowledge Graph API.
- [Vertex AI Search - Document search](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/search/retrieval-augmented-generation): This demo illustrates how Vertex AI Search and the Vertex AI PaLM API help ensure that generated content is grounded in validated, relevant and up-to-date information.
- [Getting Started with LangChain and Vertex AI PaLM API](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/language/orchestration/langchain/intro_langchain_palm_api.ipynb): Use LangChain and Vertex AI PaLM API to generate text.

## Config.toml

The configuration file acts as a control center for a marketing content generation, providing the necessary settings, prompts, and data to automate the creation of personalized and brand-consistent marketing materials.  

The following are the key sections and their functions:

#### **Global:**

- Sets core project settings (project ID, location).
- Specifies credentials for Workspace access.
- Identifies BigQuery datasets and Vertex AI resources.
- Defines Workspace document templates and folders.
- Sets the GCS bucket for asset storage.
- Defines Workspace API scopes (permissions). 

#### **Prompts:**

- Provides detailed brand information (name, vision, mission, etc.) to guide content generation.
- Defines prompt templates for various types of content (brand statement, primary message, communication channel, email, web post, ad, headlines, descriptions).
- Includes placeholders ({}) for dynamic content insertion.  

#### **Models:** 

- Specifies the names of AI models to use for text and image generation.  

#### **Data Sample:**

- Provides sample data and options (age buckets, names, languages) for personalizing content.  


# Environment Setup
You have two options to deploy the solution:

1. Automated Deployment (Recommended): Navigate to the [infra](infra/) folder. This folder contains Terraform code and scripts designed to automate the entire deployment process for you. Follow the instructions provided within the folder to initiate the automated deployment.

2. Manual Setup: If you prefer a hands-on approach, you can opt for [manual setup](manual-setup.md). Detailed instructions are available on how to configure the solution components step-by-step.


## Getting help

If you have any questions or if you found any problems with this repository, please report through GitHub issues.
