# GenAI for Marketing - Backend APIs

We developed a comprehensive set of APIs, utilizing Python and FastAI, which encapsulate all features available in the GenAI for Marketing repository. This implementation paves the way for streamlined data interactions and enhanced functionality, enabling you to deploy the solution in your environment.

You are empowered to extend these APIs, intertwining them with your specific policies pertaining to security, access, and authentication to bolster a secure, seamless, and individualized interaction with the data and services available. Our offering merges practicality with customization, ensuring that your specific requirements are catered to with precision and reliability.

## List of APIs developed in this repository

**Text generation with Vertex AI PaLM API (text-bison)** (path="/generate-text")
 - Generate text with PaLM API (text-bison) latest or 001.

**Image generation with Vertex Imagen API** (path="/generate-image")
 - Generate images with the Vertex Imagen API.

**Image editing with Vertex Imagen API** (path="/edit-image")
 - Edit images with a prompt and a mask.

**Get top search terms from Google Trends** (path="/get-top-search-terms")
 - Retrieve top search terms from Google trends

**Summarize news articles related to keywords** (path="/post-summarize-news")
 - Retrieve N news articles with keyword(s) using the GDELT API and summarize them.

**From natural language to SQL** (path="/post-audiences")
 - Transform a question using natural language to SQL and query BigQuery.

**Query sample data** (path="/get-dataset-sample")
 - Query BigQuery and return 3 lines of a given table

**Query Vertex AI Search** (path="/post-consumer-insights")
 - Query Vertex AI Search with using input and return to 10 results.

**Upload file to Google Drive** (path="/post-upload-file-drive")
 - Given an uploaded file using a form, upload it to Google Drive.

**Create Brief document and upload to Drive** (path="/creative-brief-create-upload")
 - Create a folder in Drive with correct permissions, copy the Creative Brief to Drive and update its contents with the generated text.

**Create Slides and populate with Charts** (path="/creative-slides-upload")
 - Create a Google Slides from a template and populate with information from Google Sheets.


## How to deploy this APIs to Google Cloud Run

Using the same Vertex AI managed notebook you created in this README file, navigate to the `backend_apis` folder, build the docker image and deploy to Cloud Run.  
Here are the steps:

> cd ./genai-for-marketing/backend_apis  
> gcloud builds submit --region=us-central1 --tag gcr.io/<YOUR PROJECT ID>/genai-marketing-apis  
> gcloud run deploy genai-marketing-apis --image gcr.io/<YOUR PROJECT ID>/genai-marketing-apis --allow-unauthenticated --region us-central1  

Replace <YOUR PROJECT ID> with the id of your project.   
This is just one example on how to deploy this container to Cloud Run on an endpoint that accepts unauthenticated requests. Change to your requirements.  