# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import tomllib
import asyncio
from . import utils_codey
from . import utils_search
from . import utils_workspace
from . import utils_firebase
from . import utils_trendspotting as trendspotting
from . import utils_prompt
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse
from googleapiclient.discovery import build
from google.cloud import bigquery
from google.cloud import datacatalog_v1
from google.cloud import discoveryengine
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
from proto import Message
import vertexai
from vertexai.preview.language_models import TextGenerationModel as bison_latest
from vertexai.language_models import TextGenerationModel as bison_ga
from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.vision_models import Image

from .body_schema import (
    TextGenerateRequest,
    TextGenerateResponse,
    ImageGenerateRequest,
    ImageEditRequest,
    ImageGenerateResponse,
    TrendTopRequest,
    TrendTopReponse,
    NewsSummaryRequest,
    NewsSummaryResponse,
    AudiencesRequest,
    AudiencesResponse,
    AudiencesSampleDataRequest,
    AudiencesSampleDataResponse,
    ConsumerInsightsRequest,
    ConsumerInsightsResponse,
    BriefCreateRequest,
    BriefCreateResponse,
    SlidesCreateRequest,
    SlidesCreateResponse,
    CampaignCreateRequest,
    CampaignCreateResponse,
    CampaignListResponse,
    Campaign,
    TranslateRequest,
    TranslateResponse,
    ContentCreationRequest,
    ContentCreationResponse
)

# Load configuration file
with open("/code/app/config.toml", "rb") as f:
    config = tomllib.load(f)
project_id = config["global"]["project_id"]
location = config["global"]["location"]

vertexai.init(project=project_id, location=location)
# Vertex AI Search Client
search_client = discoveryengine.SearchServiceClient()
vertexai_search_datastore = config["global"]["vertexai_search_datastore"]

# Audiences
dataset_id = config["global"]["dataset_id"]
prompt_nl_sql = config["global"]["prompt_nl_sql"]
tag_name = config["global"]["tag_name"]

# Trendspotting
bq_client = bigquery.Client(project=project_id)
datacatalog_client = datacatalog_v1.DataCatalogClient()

# Text models
llm_latest = bison_latest.from_pretrained(model_name="text-bison@latest")
llm_ga = bison_ga.from_pretrained(model_name="text-bison@001")
TEXT_MODEL_NAME = config["models"]["text_model_name"]

# Image models
imagen = ImageGenerationModel.from_pretrained("imagegeneration@002")

# Workspace integration
CREDENTIALS = service_account.Credentials.from_service_account_file(
    filename=config["global"]["service_account_json_key"], 
    scopes=config["global"]["workspace_scopes"])
drive_service = build('drive', 'v3', credentials=CREDENTIALS)
docs_service = build('docs', 'v1', credentials=CREDENTIALS)
sheets_service = build('sheets', 'v4', credentials=CREDENTIALS)
slides_service = build('slides', 'v1', credentials=CREDENTIALS)

drive_folder_id = config["global"]["drive_folder_id"]
slides_template_id = config["global"]["slides_template_id"]
doc_template_id = config["global"]["doc_template_id"]
sheet_template_id = config["global"]["sheet_template_id"]
slide_page_id_list = config["global"]["slide_page_id_list"]

#prompts
BRAND_OVERVIEW = config["prompts"]["prompt_brand_overview"]
BRAND_STATEMENT_PROMPT_TEMPLATE =config["prompts"]["prompt_brand_statement_template"]
PRIMARY_MSG_PROMPT_TEMPLATE = config["prompts"]["prompt_primary_msg_template"]
COMMS_CHANNEL_PROMPT_TEMPLATE = config["prompts"]["prompt_comms_channel_template"]
BUSINESS_NAME = config["prompts"]["prompt_business_name"]
EMAIL_TEXT_PROMPT = config["prompts"]["prompt_email_text"]
IMAGE_GENERATION_PROMPT = config["prompts"]["prompt_image_generation"]
WEBSITE_PROMPT_TEMPLATE = config["prompts"]["prompt_website_template"]
IMAGE_PROMPT_TAMPLATE = config["prompts"]["prompt_image_template"]
AD_PROMPT_TEMPLATE = config["prompts"]["ad_prompt_template"]
HEADLINE_PROMPT_TEMPLATE = config["prompts"]["headline_prompt_template"]
LONG_HEADLINE_PROMPT_TEMPLATE = config["prompts"]["load_headline_prompt_template"]
DESCRIPTION_PROMPT_TEMPLATE = config["prompts"]["description_prompt_template"]


app = FastAPI()

@app.get(path="/")
def root():
    return "Root Get Response!!"

# create-campaign
@app.post("/campaigns")
def create_campaign(data: CampaignCreateRequest,request: Request) -> CampaignCreateResponse:
    """Campaing Creation and content generation with PaLM API
        Parameters:
            campaign_name: str
            theme: str
            brief: dict = {"gender_select_theme":"Male","age_select_theme":"20-30",objective_select_theme:"Drive Awareness","competitor_select_theme":"Fashion Forward"}
        Returns:
            id (str): Response of generated Campaign ID
            campaign_name:str
            workspace_asset: dict
        """
    headers = request.headers
    jwt = headers.get('Authorization')
    user_id = utils_firebase.verify_auth_token(jwt)
    if user_id == '000':
        raise HTTPException(status_code=401, detail="Token Expired")
    
    gender_select_theme = data.brief.gender_select_theme
    age_select_theme = data.brief.age_select_theme
    objective_select_theme = data.brief.objective_select_theme
    competitor_select_theme = data.brief.competitor_select_theme
    async def generate_campaign() -> tuple:
            return await asyncio.gather(
                utils_prompt.async_predict_text_llm(
                    BRAND_STATEMENT_PROMPT_TEMPLATE.format(
                        gender_select_theme, 
                        age_select_theme,
                        objective_select_theme,
                        competitor_select_theme,
                        BRAND_OVERVIEW),
                    TEXT_MODEL_NAME),
                utils_prompt.async_predict_text_llm(
                    PRIMARY_MSG_PROMPT_TEMPLATE.format(
                        gender_select_theme, 
                        age_select_theme,
                        objective_select_theme,
                        competitor_select_theme,
                        BRAND_OVERVIEW),
                    TEXT_MODEL_NAME),
                utils_prompt.async_predict_text_llm(
                    COMMS_CHANNEL_PROMPT_TEMPLATE.format(
                        gender_select_theme, 
                        age_select_theme,
                        objective_select_theme,
                        competitor_select_theme),
                    TEXT_MODEL_NAME)) 
    try:
        generated_tuple = asyncio.run(generate_campaign())
        print(generated_tuple)
        brand_statement = generated_tuple[0] 
        primary_message = generated_tuple[1]
        comm_channels = generated_tuple[2]
        brief_scenario = (
                    f'Targeting gender: {gender_select_theme}, '
                    f'Age group: {age_select_theme}, '
                    f'Campaign objective: {objective_select_theme}, '
                    f'Competitor: {competitor_select_theme}') 
        workspace_asset = post_brief_create_upload(BriefCreateRequest(campaign_name=data.campaign_name,business_name=BUSINESS_NAME,brief_scenario=brief_scenario,brand_statement=brand_statement,primary_message=primary_message,comm_channels=comm_channels))
    except Exception as e:
        print("Failed in Creating Content Asset")
        raise HTTPException(status_code=400, detail=str(e))
    else:
        campaign = Campaign(name=data.campaign_name,theme=data.theme,brief=data.brief,workspace_assets=workspace_asset)
        update_time,campaign_id = utils_firebase.create_campaign(user_id=user_id,campaign=campaign)
        print(update_time,campaign_id)
        return CampaignCreateResponse(id=campaign_id,campaign_name=data.campaign_name,theme=data.theme,workspace_assets=workspace_asset)

# List-campaign
@app.get("/campaigns")
async def list_campaign(request: Request) -> CampaignListResponse:
    """
    List Existing Campaign for logged in user
    """
    headers = request.headers
    token = headers.get('Authorization')
    user_id = utils_firebase.verify_auth_token(token)
    if user_id == '000':
        raise HTTPException(status_code=401, detail="Token Expired")
   
    list_of_campaigns = utils_firebase.list_campaigns(user_id=user_id)
    print(list_of_campaigns)
    return CampaignListResponse(results=list_of_campaigns)

# Update-campaign
@app.put("/campaigns/{campaign_id}")
async def update_campaign(campaign_id:str,data:Campaign, request: Request):
    """
    Update Campiagn detail in backend storage
    """
    headers = request.headers
    token = headers.get('Authorization')
    user_id = utils_firebase.verify_auth_token(token)
    if user_id == '000':
        raise HTTPException(status_code=401, detail="Token Expired")
    
    response = utils_firebase.update_campaign(user_id=user_id,campaign_id=campaign_id,data=data)
    print(response)
    return JSONResponse(content={'message': 'Successfully Updated'}, status_code=200)

# Delete-campaign
@app.delete("/campaigns/{campaign_id}")
async def delete_campaign(campaign_id:str,request: Request):
    """
    Delete Campiagn from backend storage
    """
    headers = request.headers
    token = headers.get('Authorization')
    user_id = utils_firebase.verify_auth_token(token)
    if user_id == '000':
        raise HTTPException(status_code=401, detail="Token Expired")
   
    response = utils_firebase.delete_campaign(user_id=user_id,campaign_id=campaign_id)
    print(response)
    return JSONResponse(content={'message': 'Successfully Deleted Campaign'}, status_code=200)

@app.post(path="/generate-text")
def post_text_bison_generate(data: TextGenerateRequest,request: Request) -> TextGenerateResponse:
    """Text generation with PaLM API
    Parameters:
        model: str = "latest"
            [Options] "latest" | "ga"
        prompt: str
        temperature: float = 0.2
        top_k: int = 40
        top_p: float = 0.8
        max_output_tokens: int = 1024
    Returns:
        text (str): Response from the LLM
        safety_attributes: Safety attributes from LLM
    """
   
    if data.model == "latest":
        llm = llm_latest
    elif data.model == "ga":
        llm = llm_ga
    else:
        raise HTTPException(status_code=400, detail="Invalid model name. Options: ga | latest.")

    try:
        llm_response = llm.predict(
            prompt=data.prompt,
            max_output_tokens=data.max_output_tokens,
            temperature=data.temperature,
            top_k=data.top_k,
            top_p=data.top_p)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return TextGenerateResponse(
            text=llm_response.text,
            safety_attributes=llm_response.safety_attributes
        )


@app.post(path="/generate-image")
def post_image_generate(data: ImageGenerateRequest,request: Request) -> ImageGenerateResponse:
    """Image generation with Imagen
    Parameters:
        prompt: str
        number_of_images: int = 1
    Returns:
        List of images with:
            images_base64_string (str): Image as base64 string
            image_size (int, int): Size of the image
            images_parameters (dict): Parameters used with the model
    """
    try:
        imagen_responses = imagen.generate_images(
            prompt=data.prompt,
            number_of_images=data.number_of_images)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        generated_images = []
        for image in imagen_responses:
            generated_images.append(
                {
                    "images_base64_string": image._as_base64_string(),
                    "image_size": image._size,
                    "images_parameters": image.generation_parameters
                }
            )

    return ImageGenerateResponse(
        generated_images=generated_images
    )


@app.post(path="/edit-image")
def post_image_edit(data: ImageEditRequest,request: Request) -> ImageGenerateResponse:
    """Image editing with Imagen
    Parameters:
        prompt: str
        base_image_bytes: bytes
        mask_bytes: bytes | None = None
        number_of_images: int = 1
    Returns:
        List of images with:
            images_base64_string (str): Image as base64 string
            image_size (int, int): Size of the image
            images_parameters (dict): Parameters used with the model
    """
    try:
        imagen_responses = imagen.edit_image(
            prompt=data.prompt,
            base_image=Image(image_bytes=data.base_image_bytes),
            mask=Image(image_bytes=data.mask_bytes),
            number_of_images=data.number_of_images
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        generated_images = []
        for image in imagen_responses:
            generated_images.append(
                {
                    "images_base64_string": image._as_base64_string(),
                    "image_size": image._size,
                    "images_parameters": image.generation_parameters
                }
            )

    return ImageGenerateResponse(
        generated_images=generated_images
    )


@app.get(path="/get-top-search-terms")
def get_top_search_term(data: TrendTopRequest,request: Request) -> TrendTopReponse:
    """Get top search terms from Google Trends
    Parameters:
        trends_date: str
            Make sure the format is "YYYY-MM-DD".
    Returns:
        top_search_terms: list[dict[int, str]]
    """
    try:
        query = (
            "SELECT term, rank "
            "FROM `bigquery-public-data.google_trends.top_terms` "
            f"WHERE refresh_date = '{data.trends_date}' "
            "GROUP BY 1,2 "
            "ORDER by rank ASC"
        )
        query_job = bq_client.query(query, location="US")
        trends = [
            {"rank": i[1], "term":i[0]}
                for i in query_job.result()
        ]
    except Exception as e:
        message = "Date must use the format YYY-MM-DD. " + str(e)
        raise HTTPException(status_code=400, detail=message)
    else:
        return TrendTopReponse(
            top_search_terms=trends
        )


@app.post(path="/post-summarize-news")
def post_summarize_news(data: NewsSummaryRequest,request: Request) -> NewsSummaryResponse:
    """Summarize news related to keyword(s)
    Parameters:
        keywords: list[str]
        max_records: int
        max_days: int = 10
    Returns:
        summaries: list[dict[str, str]]
    """

    # Step 1 - Retrieve documents with keywords from GDELT
    # We look at the last 5 days to retrieve News Articles
    end_date = datetime.now()
    start_date = end_date - timedelta(data.max_days)

    try:
        documents = trendspotting.get_relevant_documents(
            data.keywords,
            start_date.strftime('%Y%m%d%H%M%S'),
            end_date.strftime('%Y%m%d%H%M%S'),
            max_records=data.max_records)
    except:
        raise HTTPException(
            status_code=400, 
            detail="No articles found. Try different keywords.")

    try:
        summaries = []
        for doc in documents:
            summary = trendspotting.summarize_news_article(doc["page_content"], llm_ga)
            summaries.append({
                "original_headline": doc["title"],
                "summary":summary,
                "url": doc["url"]
            })
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Something went wrong. "
                    "Could not summarize news articles. {str(e)}")

    return NewsSummaryResponse(
        summaries=summaries
    )


@app.post(path="/post-audiences")
def post_audiences(data: AudiencesRequest,request: Request) -> AudiencesResponse:
    """Transform a question in NL to SQL and query BQ.
    Parameters:
        question: Question to be asked to BQ.
    Returns:
        audiences: dict with emails
        gen_code: SQL code
    """
    # Audiences
    tag_template_name = (f'projects/{project_id}/locations/'
                        f'{location}/tagTemplates/{config["global"]["tag_name"]}')
    query_metadata = (
        f'SELECT * FROM `{project_id}.{dataset_id}.INFORMATION_SCHEMA.TABLES`'
        ' WHERE table_name NOT LIKE "%metadata%"')

    try:
        audiences, gen_code = utils_codey.generate_sql_and_query(
            llm=llm_latest,
            datacatalog_client=datacatalog_client,
            prompt_template=prompt_nl_sql,
            query_metadata=query_metadata,
            question=data.question,
            project_id=project_id,
            dataset_id=dataset_id,
            tag_template_name=tag_template_name,
            bqclient=bq_client
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return AudiencesResponse(
        audiences=audiences,
        gen_code=gen_code
    )


@app.get(path="/get-dataset-sample")
def get_dataset_sample(data: AudiencesSampleDataRequest,request: Request) -> AudiencesSampleDataResponse:
    """Retrieve 3 rows of a BQ table
    Parameters:
        table_name: str
    Returns:
        table_sample: dict
    """

    if data.table_name not in ["customers", "events", "transactions"]:
        raise HTTPException(
            status_code=400,
            detail="Provide a valid table name."
        )

    query = f"SELECT * FROM `{project_id}.{dataset_id}.{data.table_name}` LIMIT 3"
    result_query = bq_client.query(query=query).to_dataframe()

    return AudiencesSampleDataResponse(
        table_name=data.table_name,
        table_sample=result_query.to_dict()
    )


@app.get(path="/post-consumer-insights")
def post_consumer_insights(data: ConsumerInsightsRequest,request: Request) -> ConsumerInsightsResponse:
    """Query Vertex AI Search and return top 10 results.
    Parameters:
        query: str
    Returns:
        results: list
    """
    
    datastore_location = "global"
    results = []
    try:
        search_results = utils_search.search(
            search_query=data.query,
            project_id=project_id,
            location=datastore_location,
            search_engine_id=vertexai_search_datastore,
            serving_config_id="default_config",
            search_client=search_client)
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail="Something went wrong. Please try again.")
    else:
        for search_result in search_results:
            search_result_dict = Message.to_dict(search_result)
            document = search_result_dict.get("document", {})
            struct_data = document.get("derived_struct_data",{})
            title = struct_data.get("title", "")
            link = struct_data.get("link", "")
            snippets = struct_data.get("snippets", [])
            if len(snippets) > 0:
                snippet = snippets[0].get("snippet", "")
                html_snippet = snippets[0].get("htmlSnippet", "")
                result = {
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "html_snippet": html_snippet
                }
                results.append(result)

    return ConsumerInsightsResponse(
        results=results
    )


@app.post(path="/post-upload-file-drive")
def post_upload_file_drive(file: UploadFile,request: Request):
    """Upload file to Google Drive
    Parameters:
        file: UploadFile
    Returns:
        file_id: str
    """
    
    try:
        file_id = utils_workspace.upload_to_folder(
            drive_service=drive_service,
            f=file.file,
            folder_id=drive_folder_id,
            upload_name=file.filename,
            mime_type=file.content_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. Please try again.")
    finally:
        file.file.close()
    return file_id


@app.post(path="/creative-brief-create-upload")
def post_brief_create_upload(data: BriefCreateRequest) -> BriefCreateResponse:
    """Create a creative brief document and upload to Google Drive
    Parameters:
        campaign_name: str
        business_name: str
        brief_scenario: str
        brand_statement: str
        primary_message: str
        comm_channels: str
    Returns:
        new_folder_id: str
        doc_id: str
    """
    try:
        print("Creating document Assets..")
        new_folder_id = utils_workspace.create_folder_in_folder(
            drive_service=drive_service,
            folder_name=f"Marketing_Assets_{int(time.time())}",
            parent_folder_id=drive_folder_id)
        
        utils_workspace.set_permission(
            drive_service=drive_service,
            file_id=new_folder_id)

        doc_id = utils_workspace.copy_drive_file(
            drive_service=drive_service,
            drive_file_id=doc_template_id,
            parentFolderId=new_folder_id,
            copy_title=f"GenAI Marketing Brief")

        utils_workspace.update_doc(
            docs_service=docs_service,
            document_id=doc_id,
            campaign_name=data.campaign_name,
            business_name=data.business_name,
            scenario=data.brief_scenario,
            brand_statement=data.brand_statement,
            primary_msg=data.primary_message,
            comms_channel=data.comm_channels)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, 
            detail="Something went wrong. Please try again.")

    return BriefCreateResponse(
        new_folder_id=new_folder_id,
        doc_id=doc_id
    )


@app.post(path="/creative-slides-upload")
def post_create_slides_upload(data: SlidesCreateRequest,request: Request) -> SlidesCreateResponse:
    """Create Slides and upload charts from Google Sheets
    Parameters:
        folder_id: str
    Returns:
        slide_id: str
        sheet_id: str
    """

    try:
        slide_id = utils_workspace.copy_drive_file(
            drive_file_id=slides_template_id,
            parentFolderId=data.folder_id,
            copy_title="Marketing Assets")
        
        sheet_id = utils_workspace.copy_drive_file(
            drive_file_id=sheet_template_id,
            parentFolderId=data.folder_id,
            copy_title="GenAI Marketing Data Source")     

        utils_workspace.merge_slides(
            presentation_id=slide_id,
            spreadsheet_id=sheet_id,
            spreadsheet_template_id=sheet_template_id,
            slide_page_id_list=sheet_template_id)

    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail="Something went wrong. Please try again."
        )

    return SlidesCreateResponse(
        slide_id=slide_id,
        sheet_id=sheet_id
    )

@app.post(path="/translate")
def translate_text(data: TranslateRequest,request: Request) -> TranslateResponse:
    """Translate Text
    Body:
        source_text:str
        source_language_code:str | None = None
        target_language_code:str 
    Returns:
        translated_text :str
    """
    text = data.source_text
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    try:
        translate_client = translate.Client()
        if data.source_language_code == None:
            translated_text = translate_client.translate(
                text,
                target_language=data.target_language_code
                )['translatedText']
        else:
            translated_text = translate_client.translate(
                text,
                source_language=data.source_language_code,
                target_language=data.target_language_code,
            )['translatedText']

    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail="Something went wrong. Please try again."+str(e)
        )

    return TranslateResponse(
        translated_text=translated_text
    )

@app.post(path="/generate-content")
def generate_content(data: ContentCreationRequest,request: Request) -> TranslateResponse:
    """Generate Content like Media , Ad or Emails
    Body:
        type: str | Email/Webpost/SocialMedia/AssetGroup
        theme: str
        context: str | None = None
        image_generate: bool = True
    Returns:
        text_content :str
        images : list
    """
    headers = request.headers
    token = headers.get('Authorization')
    user_id = utils_firebase.verify_auth_token(token)
    if user_id == '000':
        raise HTTPException(status_code=401, detail="Token Expired")
    images = []
    text_content = ''
    try:
        if data.type == 'Email':
            text_content=utils_prompt.async_predict_text_llm(
                        EMAIL_TEXT_PROMPT.format(
                            data.theme,
                            data.context),
                        TEXT_MODEL_NAME)
        elif data.type == 'Webpost':
            text_content=utils_prompt.async_predict_text_llm(
                        WEBSITE_PROMPT_TEMPLATE.format(
                            data.theme,
                            data.context),
                        TEXT_MODEL_NAME)
        elif data.type == 'SocialMedia':
            text_content=utils_prompt.async_predict_text_llm(
                        AD_PROMPT_TEMPLATE.format(
                            data.theme,
                            data.context),
                        TEXT_MODEL_NAME)
        elif data.type == 'AssetGroup':
            async def generate_brief() -> tuple:
                return await asyncio.gather(
                    utils_prompt.async_predict_text_llm(
                        prompt=HEADLINE_PROMPT_TEMPLATE.format(
                            data.theme,
                            BRAND_OVERVIEW),
                        pretrained_model=TEXT_MODEL_NAME,
                        max_output_tokens=256
                    ),
                    utils_prompt.async_predict_text_llm(
                        prompt=LONG_HEADLINE_PROMPT_TEMPLATE.format(
                            data.theme,
                            BRAND_OVERVIEW),
                        pretrained_model=TEXT_MODEL_NAME,
                    ),
                    utils_prompt.async_predict_text_llm(
                        prompt=DESCRIPTION_PROMPT_TEMPLATE.format(
                            data.theme,
                            BRAND_OVERVIEW),
                        pretrained_model=TEXT_MODEL_NAME)) 
    
            generated_tuple = asyncio.run(generate_brief())
            
            text_content = "Headline: " + generated_tuple[0] + "\n Long Headline:" + generated_tuple[1] +"\n Description"+ generated_tuple[2]
        if data.image_generate == True:
            images = utils_prompt.async_generate_image(
                    prompt=IMAGE_PROMPT_TAMPLATE.format(
                            data.theme,)
            )
             
    except Exception as e:
            raise HTTPException(
            status_code=400, 
            detail="Something went wrong. Please try again."+str(e)
        )
    
    return ContentCreationResponse(
        text_content=text_content,
        images = images
    )