# Generative AI for Marketing Using Google Cloud

**Resources enabling generative AI-powered marketing use cases on Google Cloud.**

This repository showcases the application of Google Cloud's Generative AI to marketing scenarios. It contains detailed, step-by-step [instructions to deploy a solution](#deployment) implementing marketing-centric Generative AI capabilities, including capabilities to craft marketing materials like blog posts and social media content. [This video](https://youtu.be/F8bppBkpCiI?si=MZNryO5D5cezJMlX&t=755) walks through the functionality in the solution.

The architecture of the deployed solution:
![Architecture](/app/images/architecture.png "Architecture")

Additionally, [supplementary Jupyter notebooks](#notebooks-and-code-samples) are provided to aid users in grasping the concepts explored in the solution.

## Table of Contents

- [Repository Structure](#repository-structure)
- [Demonstrations](#demonstrations)
- [Deployment](#deployment)
- [Notebooks and Code Samples](#notebooks-and-code-samples)
- [Configuration](#configuration)
- [Getting Help](#getting-help)



## Repository Structure

```
.
├── app
└── backend_apis
└── frontend
└── notebooks
└── templates
└── infra
```

- [`/app`](/app): Architecture diagrams and images.
- [`/backend_apis`](/backend_apis): Source code for backend APIs.  
- [`/frontend`](/frontend): Source code for the frontend UI.  
- [`/infra`](/infra): Scripts and configuration for deploying the solution.
- [`/notebooks`](/notebooks): Notebooks demonstrating and explaining how to use Google Cloud's Generative AI for marketing scenarios, including scenarios included in the solution.
- [`/templates`](/templates): Workspace Slides, Docs and Sheets templates used in the solution.  

## Demonstrations

The deployed solution supports the following demonstrations:

* **Marketing Insights**: Utilize Looker Dashboards to access and visualize marketing data. Marketers can access and visualize marketing data to build data-driven marketing campaigns, empowering businesses to connect with their target audience more efficiently, thereby improving conversion rates.  
* **Audience and Insight Finder**: Conversational interface that translates natural language into SQL queries, democratizing access to data for non-SQL users thus removing bottlenecks for marketing teams.  
* **Trendspotting**: Identify emerging trends in the market by analyzing Google Trends data on a Looker dashboard, and summarize news related to top search terms. This can help businesses to stay ahead of the competition and develop products and services that meet the needs and interests of their customers.  
* **Content Search**: Improve search experience for internal or external content with [Vertex AI Search](https://cloud.google.com/enterprise-search) for business users.  
* **Content Generation**: Reduce time for content generation with [Vertex Foundation Models](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models). Generate compelling and captivating email copy, website articles, social media posts, and assets for PMax. All aimed at achieving specific goals such as boosting sales, generating leads, or enhancing brand awareness. This encompasses both textual and visual elements using Vertex language & vision models.  
* **Workspace Integration**: Transfer the insights and assets you generate to [Google Workspace](https://workspace.google.com/), and visualize in Google Slides, Docs and Sheets.

## Deployment

Follow the instructions in the [deployment guide](/infra/README.md) to deploy with Terraform.

[This video](https://www.youtube.com/watch?v=EOY5B5HBxIY) walks through the automated deployment process.

## Notebooks and Code Samples

The notebooks listed below were developed to explain the concepts featured in this solution:  
- [Data Q&A with PaLM API and GoogleSQL](/notebooks/data_qa_with_sql.ipynb) (/notebooks/data_qa_with_sql.ipynb): Translate questions from natural language to GoogleSQL to interact with BigQuery.
- [News Summarization with LangChain Agents and Vertex AI PaLM Text Models](/notebooks/news_summarization_langchain_palm.ipynb) (news_summarization_langchain_palm.ipynb): Summarize news articles related to top search terms using LangChain agents and the ReAct concept.
- [News Summarization with PaLM API](/notebooks/simple_news_summarization.ipynb) (simple_news_summarization.ipynb): News summarization related to top search terms.
- [Imagen Fine Tuning](/notebooks/Imagen_finetune.ipynb) (Imagen_finetune.ipynb): Fine tune Imagen model.

The following additional (external) notebooks provide supplementary information on the concepts discussed in this repository:
- [Tuning Gemini](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/tuning): Examples of how to tune Gemini with your dataset to improve the model's response. This is useful for brand voice because it allows you to ensure that the model is generating text that is consistent with your brand's tone and style.
- [Document Summarization Techniques](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/language/use-cases/document-summarization): Two notebooks explaining different techniques to summarize large documents.
- [Document Q&A](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/language/use-cases/document-qa): Two notebooks explaining different techniques to do document Q&A on a large amount of documents.
- [Vertex AI Search - Web Search](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/search/web-app): This demo illustrates how to search through a corpus of documents using Vertex AI Search. Additional features include how to search the public Cloud Knowledge Graph using the Enterprise Knowledge Graph API.
- [Vertex AI Search - Document Search](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/search/retrieval-augmented-generation): This demo illustrates how Vertex AI Search and the Vertex AI PaLM API help ensure that generated content is grounded in validated, relevant and up-to-date information.
- [Getting Started with LangChain and Vertex AI PaLM API](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/orchestration/intro_langchain_gemini.ipynb): Getting Started with LangChain + Vertex AI Gemini API.


## Configuration

Some of the solution's behavior can be changed by adjusting configuration.

### Pre-Deployment Configuration

When deploying the Google Cloud Generative AI for Marketing solution, various settings for the deployment are pulled from the [`infra/variables.tf`](infra/variables.tf) file. 

If your deployment needs do not match the default deployment, some of your deployment needs might be met by adjusting the defaults in `variables.tf` prior to beginning deployment.

Make changes to `variables.tf` prior to running `terraform init`, making changes afterwards may result in unexpected behavior including irrecoverable deployment failures.

### Config.toml

When deploying, after `terraform apply` completes successfully, there will be a file called `config.toml` in [`backend_apis/app`](/backend_apis/app). `config.toml` is generated from [`infra/templates/config.toml.tftpl`](infra/templates/config.toml.tftpl).

`config.toml`  acts as a control center for a marketing content generation, providing the necessary settings, prompts, and data to automate the creation of personalized and brand-consistent marketing materials.

You can adjust some of the values in `config.toml` to change the behavior of your deployment. If you adjust the values in `config.toml`, [rerun the backend deployment](/infra/README.md#backend-deployment) ([`infra/scripts/backend_deployment.sh`](infra/scripts/backend_deployment.sh)) to push the updated config to the backend

The following are the key sections of `config.toml` and their functions:

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

### Adding Looker Dashboards

You can display your own Looker Dashboards in the Marketing Insights and Campaign Performance pages. 

For Marketing Insights, edit [/frontend/src/app/marketing-insights/marketing-insights.component.html](/frontend/src/app/marketing-insights/marketing-insights.component.html) and for Campaign Performance edit [/frontend/src/app/marketing-insights/marketing-insights.component.html](/frontend/src/app/marketing-insights/marketing-insights.component.html). The procedure is the same for both of these files:

#### 1. Add the Dashboard Name to the Dropdown

1. Find the line `<select class="select-theme-dropdowns" name="state" ngModel (ngModelChange)="onClick($event)">`. If you are on a fresh deployment, the line below is `<option value="Overview">Overview</option>`.
2. Add another similarly formatted line: `<option value="Display Name in Dropdown">newdash</option>`, where `value` is what will be displayed in the UI and inside the `>` and `<` is the identifier you'll use below to link to the dashboard. In this case we're adding a dashboard that will be identified as "Display Name in Dropdown" and below we'll link this dashboard using the `newdash` identifier.

#### 2. Add the Dashboard Link

On a fresh deployment at the bottom of the file, you'll see something like this:
```html
<div *ngIf="overview" class="overviewcss">
  <iframe width="1000" height="1000" src="https://googledemo.looker.com/embed/dashboards/2131?allow_login_screen=true" ></iframe>
</div>
```

At the end of the file, add three similar lines for each dashboard, replacing the following:
1. Set `*ngIF=` to the identifier of the new dashboard that you specified in the dropdown. E.g. `<div *ngIf="newdash" class="overviewcss">`.
2. Set the `src=` to the embed link to your dashboard. The `allow_login_screen=true` in the URL will open the authentication page from Looker to secure the access to your account. E.g., `<iframe width="1000" height="1000" src="https://googledemo.looker.com/embed/dashboards/YOURDASH?allow_login_screen=true" ></iframe>`


#### Marketing Analytics Jumpstart

If you have your Google Ads and Google Analytics 4 accounts in production, you can deploy the [`Marketing Analytics Jumpstart`](https://github.com/GoogleCloudPlatform/marketing-analytics-jumpstart) solution, build the Dashboards, and link them into these pages in the Generative AI for Marketing UI.

## Getting Help

If you have any questions or if you found any problems with this repository, please report through GitHub issues.
