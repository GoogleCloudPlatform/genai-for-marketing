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
from . import utils_gcs
from . import utils_firebase
from . import utils_trendspotting as trendspotting
from . import utils_prompt
from . import bulk_email_util
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, UploadFile, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from googleapiclient.discovery import build
from google.cloud import bigquery
from google.cloud import datacatalog_v1
from google.cloud import discoveryengine
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from google.oauth2 import service_account
from proto import Message

import vertexai
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models

from vertexai.preview.language_models import TextGenerationModel as bison_latest
from vertexai.language_models import TextGenerationModel as bison_ga
from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.vision_models import Image

from google.cloud import secretmanager
import json
import base64

from .body_schema import (
    TextGenerateRequest,
    TextGenerateResponse,
    ImageGenerateRequest,
    ImageEditRequest,
    ImageGenerateResponse,
    TrendTopReponse,
    NewsSummaryRequest,
    NewsSummaryResponse,
    AudiencesRequest,
    AudiencesResponse,
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
    ContentCreationResponse,
    CampaignStatusUpdate,
    BulkEmailGenRequest,
    BulkEmailGenResponse,
    ExportGoogleDocRequest,
    ExportGoogleDocResponse,
    TexttoSpeechRequest,
    TexttoSpeechResponse
)

# Load configuration file
with open("/app/config.toml", "rb") as f:
    config = tomllib.load(f)
project_id = config["global"]["project_id"]
location = config["global"]["location"]
bucket_name = config["global"]["asset_bkt"]
domain = config["global"]["domain"]

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
llm_latest = bison_latest.from_pretrained(model_name="text-bison")
llm_ga = bison_ga.from_pretrained(model_name="text-bison@002")
gemini_llm = GenerativeModel("gemini-1.0-pro-001")

TEXT_MODEL_NAME = config["models"]["text_model_name"]

#translation
translate_client = translate.Client()

#texttospeech
texttospeech_client = texttospeech.TextToSpeechLongAudioSynthesizeClient()

# Image models
imagen = ImageGenerationModel.from_pretrained("imagegeneration@002")

# Workspace integration
# Fetch Secret Configuration
secret_client = secretmanager.SecretManagerServiceClient()
secret_name = config['global']['secret_name_workspace']
secret_response = secret_client.access_secret_version(name=secret_name)
workspace_cred = secret_response.payload.data.decode("UTF-8")
workspace_cred = json.loads(workspace_cred)
CREDENTIALS = service_account.Credentials.from_service_account_info(
    info=workspace_cred, 
    scopes=config["global"]["workspace_scopes"])
# drive_service = build('drive', 'v3', credentials=CREDENTIALS)
# docs_service = build('docs', 'v1', credentials=CREDENTIALS)
# sheets_service = build('sheets', 'v4', credentials=CREDENTIALS)
# slides_service = build('slides', 'v1', credentials=CREDENTIALS)

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

router = APIRouter(prefix="/marketing-api")
app = FastAPI(docs_url="/marketing-api/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# create-campaign
@router.post("/users/{user_id}/campaigns")
def create_campaign(user_id: str,data: CampaignCreateRequest
                    ) -> CampaignCreateResponse:
    """Campaing Creation and content generation with PaLM API
        Parameters:
            user_id: str
            campaign_name: str
            theme: str
            brief: dict = {
                "gender_select_theme":"Male",
                "age_select_theme":"20-30",
                "objective_select_theme":"Drive Awareness",
                "competitor_select_theme":"Fashion Forward"
                }
        Returns:
            id (str): Response of generated Campaign ID
            campaign_name:str
            workspace_asset: dict
        """
    
    gender_select_theme = data.brief.gender_select_theme
    age_select_theme = data.brief.age_select_theme
    objective_select_theme = data.brief.objective_select_theme
    competitor_select_theme = data.brief.competitor_select_theme
    async def generate_campaign() -> tuple:
            return await asyncio.gather(
                utils_prompt.async_predict_text_gemini(
                    BRAND_STATEMENT_PROMPT_TEMPLATE.format(
                        gender_select_theme, 
                        age_select_theme,
                        objective_select_theme,
                        competitor_select_theme,
                        BRAND_OVERVIEW)
                        ),
                utils_prompt.async_predict_text_gemini(
                    PRIMARY_MSG_PROMPT_TEMPLATE.format(
                        gender_select_theme, 
                        age_select_theme,
                        objective_select_theme,
                        competitor_select_theme,
                        BRAND_OVERVIEW)
                    ),
                utils_prompt.async_predict_text_gemini(
                    COMMS_CHANNEL_PROMPT_TEMPLATE.format(
                        gender_select_theme, 
                        age_select_theme,
                        objective_select_theme,
                        competitor_select_theme)
                    )) 
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
        workspace_asset = post_brief_create_upload(BriefCreateRequest(
            campaign_name=data.campaign_name,
            business_name=BUSINESS_NAME,
            brief_scenario=brief_scenario,
            brand_statement=brand_statement,
            primary_message=primary_message,
            comm_channels=comm_channels
            ))
    except Exception as e:
        print("Failed in Creating Content Asset")
        raise HTTPException(status_code=400, detail=str(e))
    else:
        campaign = Campaign(
            name=data.campaign_name,
            theme=data.theme,
            brief=data.brief,
            workspace_assets=workspace_asset
            )
        update_time,campaign_id = utils_firebase.create_campaign(
            user_id=user_id,
            campaign=campaign
            )
        print(update_time,campaign_id)
        return CampaignCreateResponse(
            id=campaign_id,
            campaign_name=data.campaign_name,
            theme=data.theme,
            workspace_assets=workspace_asset
            )

# List-campaigns
@router.get("/users/{user_id}/campaigns")
async def list_campaigns(user_id: str) -> CampaignListResponse:
    """
    List Existing Campaign for logged in user
    """
    list_of_campaigns = utils_firebase.list_campaigns(user_id=user_id)
    print(list_of_campaigns)
    return CampaignListResponse(results=list_of_campaigns)

# get-campaign
@router.get("/users/{user_id}/campaigns/{campaign_id}")
async def get_campaign(user_id: str,campaign_id:str) -> Campaign:
    """
    List Existing Campaign for logged in user
    """
    campaign_resp = utils_firebase.read_campaign(user_id=user_id,campaign_id=campaign_id)
    if campaign_resp == {}:
        raise HTTPException(
            status_code=400, 
            detail="Invalid user_id or campaign does not exists."
            )
    return Campaign(**campaign_resp)

# Update-campaign
@router.put("/users/{user_id}/campaigns/{campaign_id}")
async def update_campaign(user_id: str,campaign_id:str,data:Campaign):
    """
    Update Campiagn detail in backend storage
    """
    response = utils_firebase.update_campaign(
        user_id=user_id,
        campaign_id=campaign_id,
        data=data
        )
    print(response)
    return JSONResponse(
        content={'message': 'Successfully Updated'},
        status_code=200
        )

# Delete-campaign
@router.delete("/users/{user_id}/campaigns/{campaign_id}")
async def delete_campaign(user_id: str,campaign_id:str):
    """
    Delete Campiagn from backend storage
    """
    response = utils_firebase.delete_campaign(
        user_id=user_id,
        campaign_id=campaign_id
        )
    print(response)
    return JSONResponse(
        content={'message': 'Successfully Deleted Campaign'}, 
        status_code=200
        )

# Update-Status
@router.put("/users/{user_id}/campaigns/{campaign_id}/status/")
async def update_status(user_id: str,campaign_id:str,data:CampaignStatusUpdate):
    """
    Update Campiagn Creative Component Status in backend storage
    """
    response = utils_firebase.update_status(
        user_id=user_id,
        campaign_id=campaign_id,
        key=data.key,
        status=data.status
        )
    print(response)
    return JSONResponse(
        content={'message': 'Successfully Activated'},
        status_code=200
        )

@router.post(path="/generate-text")
def post_text_bison_generate(data: TextGenerateRequest,
                             ) -> TextGenerateResponse:
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
        raise HTTPException(
            status_code=400, 
            detail="Invalid model name. Options: ga | latest."
            )

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


@router.post(path="/generate-image")
def post_image_generate(data: ImageGenerateRequest,
                        ) -> ImageGenerateResponse:
    """Image generation with Imagen
    Parameters:
        prompt: str
        number_of_images: int = 1
    Returns:
        List of images with:
            id: image id
            images_base64_string (str): Image as base64 string
            image_size (int, int): Size of the image
            images_parameters (dict): Parameters used with the model
    """
    try:
        imagen_responses = imagen.generate_images(
            prompt=data.prompt,
            number_of_images=data.number_of_images,
            negative_prompt=data.negative_prompt)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        generated_images = []
        i=0
        for image in imagen_responses:
            generated_images.append(
                {   
                    "id": i ,
                    "images_base64_string": image._as_base64_string(),
                    "image_size": image._size,
                    "images_parameters": image.generation_parameters
                }
            )
            i=i+1

    return ImageGenerateResponse(
        generated_images=generated_images
    )


@router.post(path="/edit-image")
def post_image_edit(data: ImageEditRequest
                    ) -> ImageGenerateResponse:
    """Image editing with Imagen
    Parameters:
        prompt: str
        base_image_base64: str
        mask_base64: str | None = None
        number_of_images: int = 1
    Returns:
        List of images with:
            id: imageid
            images_base64_string (str): Image as base64 string
            image_size (int, int): Size of the image
            images_parameters (dict): Parameters used with the model
    """
    if not data.mask_base64:
        mask = None
    else:
        mask = Image(image_bytes=base64.b64decode(data.mask_base64))

    try:
        imagen_responses = imagen.edit_image(
            prompt=data.prompt,
            base_image=Image(image_bytes=base64.b64decode(data.base_image_base64)),
            mask=mask,
            number_of_images=data.number_of_images,
            negative_prompt=data.negative_prompt)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    else:
        generated_images = []
        i = 0
        for image in imagen_responses:
            generated_images.append(
                {   
                    "id" : i,
                    "images_base64_string": image._as_base64_string(),
                    "image_size": image._size,
                    "images_parameters": image.generation_parameters
                }
            )
            i=i+1

    return ImageGenerateResponse(
        generated_images=generated_images
    )


@router.get(path="/get-top-search-terms/{trends_date}")
def get_top_search_term(trends_date: str
                        ) -> TrendTopReponse:
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
            f"WHERE refresh_date = '{trends_date}' "
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


@router.post(path="/post-summarize-news")
def post_summarize_news(data: NewsSummaryRequest,request: Request
                        ) -> NewsSummaryResponse:
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
            summary = trendspotting.summarize_news_article(
                doc["page_content"],
                gemini_llm)
            summaries.append({
                "original_headline": doc["title"],
                "summary":summary,
                "url": doc["url"]
            })
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Something went wrong. Could not summarize news articles. {str(e)}")

    return NewsSummaryResponse(
        summaries=summaries
    )


@router.post(path="/post-audiences")
def post_audiences(data: AudiencesRequest) -> AudiencesResponse:
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
        audiences, gen_code, prompt = utils_codey.generate_sql_and_query(
            llm=llm_ga,
            datacatalog_client=datacatalog_client,
            prompt_template=prompt_nl_sql,
            query_metadata=query_metadata,
            question=data.question,
            project_id=project_id,
            dataset_id=dataset_id,
            tag_template_name=tag_template_name,
            bqclient=bq_client
        )
        crm_data = bulk_email_util.generate_information(audiences).to_dict('records')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return AudiencesResponse(
        audiences={"data":audiences,"crm_data":crm_data},
        gen_code=gen_code,
        prompt=prompt
    )


@router.get(path="/get-dataset-sample/{table_name}")
def get_dataset_sample(table_name: str
                       ) -> AudiencesSampleDataResponse:
    """Retrieve 3 rows of a BQ table
    Parameters:
        table_name: str
    Returns:
        table_sample: dict
    """

    if table_name not in ["customers", "events", "transactions"]:
        raise HTTPException(
            status_code=400,
            detail="Provide a valid table name."
        )

    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_name}` LIMIT 3"
    result_job = bq_client.query(query=query)
    result = []
    for row in result_job:
        result.append(dict(row.items()))

    return AudiencesSampleDataResponse(
        table_name=table_name,
        data=result
    )


@router.post(path="/post-consumer-insights")
def post_consumer_insights(data: ConsumerInsightsRequest
                           ) -> ConsumerInsightsResponse:
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
        llm_summary = search_results.summary.summary_text

        for search_result in search_results.results:
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
        results=results,
        llm_summary=llm_summary
    )


@router.post(path="/post-upload-file-drive/{folder_id}")
def post_upload_file_drive(folder_id: str,file: UploadFile):
    """Upload file to Google Drive
    Parameters:
        file: UploadFile
    Returns:
        file_id: str
    """
    
    try:
        file_id = utils_workspace.upload_to_folder(
            credentials = CREDENTIALS,
            f=file.file,
            folder_id=folder_id,
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

@router.post(path="/post-upload-file-gcs/{folder_id}")
def post_upload_file_gcs(folder_id: str,file: UploadFile):
    """Upload file to Google Drive
    Parameters:
        file: UploadFile
    Returns:
        file_path: str
    """
    
    try:
        file_path = utils_gcs.upload_to_gcs(
            project_id= project_id,
            bucket_name= bucket_name,
            file=file.file,
            destination_blob_name=f"{folder_id}/{file.filename}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong. Please try again.")
    finally:
        file.file.close()
    return file_path

@router.post(path="/creative-brief-create-upload")
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
            credentials = CREDENTIALS,
            folder_name=f"Marketing_Assets_{int(time.time())}",
            parent_folder_id=drive_folder_id)
        
        utils_workspace.set_permission(
            credentials = CREDENTIALS,
            file_id=new_folder_id,
            domain=domain)

        doc_id = utils_workspace.copy_drive_file(
            credentials = CREDENTIALS,
            drive_file_id=doc_template_id,
            parentFolderId=new_folder_id,
            copy_title=f"GenAI Marketing Brief")

        utils_workspace.update_doc(
            credentials = CREDENTIALS,
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
            detail="Something went wrong. Please try again."+str(e))

    return BriefCreateResponse(
        new_folder_id=new_folder_id,
        doc_id=doc_id
    )


@router.post(path="/creative-slides-upload")
def post_create_slides_upload(data: SlidesCreateRequest
                              ) -> SlidesCreateResponse:
    """Create Slides and upload charts from Google Sheets
    Parameters:
        folder_id: str
    Returns:
        slide_id: str
        sheet_id: str
    """

    try:
        slide_id = utils_workspace.copy_drive_file(
            credentials = CREDENTIALS,
            drive_file_id=slides_template_id,
            parentFolderId=data.folder_id,
            copy_title="Marketing Assets")
        
        sheet_id = utils_workspace.copy_drive_file(
            credentials = CREDENTIALS,
            drive_file_id=sheet_template_id,
            parentFolderId=data.folder_id,
            copy_title="GenAI Marketing Data Source")
        print(sheet_id)     

        utils_workspace.merge_slides(
            credentials = CREDENTIALS,
            presentation_id=slide_id,
            spreadsheet_id=sheet_id,
            spreadsheet_template_id=sheet_template_id,
            slide_page_id_list=slide_page_id_list
            )

    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail="Something went wrong. Please try again."+str(e)
        )

    return SlidesCreateResponse(
        slide_id=slide_id,
        sheet_id=sheet_id
    )

@router.post(path="/translate")
def translate_text(data: TranslateRequest
                   ) -> TranslateResponse:
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
        results = []
        i = 0
        while i*128 < len(text):
            if data.source_language_code == None:
                result = translate_client.translate(
                    text[i*128:i*128+128],
                    target_language=data.target_language_code
                    )['translatedText']
            else:
                result = translate_client.translate(
                    text[i*128:i*128+128],
                    source_language=data.source_language_code,
                    target_language=data.target_language_code,
                )['translatedText']
            results.extend(result)
            i+=1
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail="Something went wrong. Please try again."+str(e)
        )
    translated_text = ''.join(results)
    return TranslateResponse(
        translated_text=translated_text
    )

@router.post(path="/generate-content")
def generate_content(data: ContentCreationRequest
                     ) -> ContentCreationResponse:
    """Generate Content like Media , Ad or Emails
    Body:
        type: str | Email/Webpost/SocialMedia/AssetGroup
        theme: str
        context: str | None = None
        no_of_char: int = 500
        audience_age_range: str = '20-30'
        audience_gender:str = 'All'
        image_generate: bool = True
    Returns:
        text_content :str
        images : list
    """
    
    images = []
    generated_content = {}
    try:
        if data.type == 'Email':
            print("Generating Email..")
            generated_content["text"]=asyncio.run(utils_prompt.async_predict_text_gemini(
                        EMAIL_TEXT_PROMPT.format(
                            data.context,
                            data.theme
                        )
                        )
                    )
        elif data.type == 'Webpost':
            generated_content["text"]=asyncio.run(utils_prompt.async_predict_text_gemini(
                        WEBSITE_PROMPT_TEMPLATE.format(
                            data.theme,
                            data.context)))
        elif data.type == 'SocialMedia':
            generated_content["text"]=asyncio.run(utils_prompt.async_predict_text_gemini(
                        AD_PROMPT_TEMPLATE.format(
                            BUSINESS_NAME,
                            data.no_of_char,
                            data.audience_age_range,
                            data.audience_gender,
                            data.theme,
                            data.context,
                            )))
        elif data.type == 'AssetGroup':
            async def generate_brief() -> tuple:
                return await asyncio.gather(
                    utils_prompt.async_predict_text_gemini(
                        prompt=HEADLINE_PROMPT_TEMPLATE.format(
                            data.theme,
                            BRAND_OVERVIEW),
                        
                        max_output_tokens=256
                    ),
                    utils_prompt.async_predict_text_gemini(
                        prompt=LONG_HEADLINE_PROMPT_TEMPLATE.format(
                            data.theme,
                            BRAND_OVERVIEW)
                        
                    ),
                    utils_prompt.async_predict_text_gemini(
                        prompt=DESCRIPTION_PROMPT_TEMPLATE.format(
                            data.theme,
                            BRAND_OVERVIEW,
                            data.context))) 
    
            generated_tuple = asyncio.run(generate_brief())
            
            generated_content["headlines"] = generated_tuple[0] 
            generated_content["long_headlines"] = generated_tuple[1] 
            generated_content["description"] = generated_tuple[2]
            generated_content["scenario"] = data.theme
            generated_content["business_name"] = BUSINESS_NAME
            generated_content["call_to_action"] = "Shop Now"
            
        if data.image_generate == True:
            images = asyncio.run(utils_prompt.async_generate_image(
                    prompt=IMAGE_PROMPT_TAMPLATE.format(
                            data.theme,)
            ))
             
    except Exception as e:
            raise HTTPException(
            status_code=400, 
            detail="Something went wrong. Please try again."+str(e)
        )
    
    return ContentCreationResponse(
        generated_content=generated_content,
        images = images
    )


@router.post(path="/bulk-email-generate")
def post_bulk_email_generate(data: BulkEmailGenRequest) -> BulkEmailGenResponse:
    """
    Parameters:
        audience : list[dict]
        theme : str
        image_context: str
    Returns:
        persionlized_emails : list[dict]
    """
    
    try:
        emails = asyncio.run(bulk_email_util.generate_emails(number_of_emails=data.no_of_emails,
                                    theme=data.theme,
                                    audience_data=data.audience,
                                    image_context = data.image_context))
        
    except Exception as e:
            raise HTTPException(
            status_code=400, 
            detail="Something went wrong. Please try again."+str(e)
        )
    
    return BulkEmailGenResponse(
        persionalized_emails=emails
    )

@router.post(path="/export-google-doc")
def post_export_google_doc(data:ExportGoogleDocRequest) -> ExportGoogleDocResponse:
    """
    data:
        folder_id: str
        doc_name: str
        text: str
        image_prefix: str
        images: list
    Returns:
        doc_id: str
    """
    
    try:
        file_id = utils_workspace.create_doc(credentials = CREDENTIALS,
                                             folder_id=data.folder_id,
                                             doc_name=data.doc_name,
                                             text=data.text)
        i=0
        for img in data.images:
            file = utils_gcs.download_from_gcs(project_id=project_id,
                                               bucket_name=bucket_name,
                                               source_blob_name='/'.join(img.split('/')[1:]))
            utils_workspace.upload_to_folder(credentials= CREDENTIALS,
                                             f=file,
                                             folder_id=data.folder_id,
                                             upload_name=str(data.image_prefix)+"_"+str(i),
                                             mime_type='application/octet-stream'
                                             )
            i=i+1
        
    except Exception as e:
            raise HTTPException(
            status_code=400, 
            detail="Something went wrong. Please try again."+str(e)
        )
    
    return ExportGoogleDocResponse(
        doc_id = file_id
    )

@router.post(path="/texttospeech")
def text_to_speech(data: TexttoSpeechRequest
                   ) -> TexttoSpeechResponse:
    """ Text to Speech
    Body:
        text:str
        prefix: str
        language_code:str | None = None
        language_name: str | None = None
    Returns:
        audio_uri :str
    """
    output_gcs_uri = "gs://"+bucket_name+"/"+data.prefix+".wav"
    
    try:
        input = texttospeech.SynthesisInput(
        text=data.text
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        if data.language_code != None and data.language_name != None:
            voice = texttospeech.VoiceSelectionParams(
                language_code=data.language_code, name=data.language_name
            )
        else:
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US", name="en-US-Standard-A"
            )

        parent = f"projects/{project_id}/locations/{location}"

        request = texttospeech.SynthesizeLongAudioRequest(
            parent=parent,
            input=input,
            audio_config=audio_config,
            voice=voice,
            output_gcs_uri=output_gcs_uri,
        )

        operation = texttospeech_client.synthesize_long_audio(request=request)
        # Set a deadline for your LRO to finish. 300 seconds is reasonable, 
        # but can be adjusted depending on the length of the input.
        # If the operation times out, that likely means there was an error. 
        # In that case, inspect the error, and try again.
        result = operation.result(timeout=300)
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail="Something went wrong. Please try again."+str(e)
        )
    return TexttoSpeechResponse(
        audio_uri=output_gcs_uri
    )


app.include_router(router=router)