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

from google.cloud import datacatalog_v1

from datetime import datetime, timedelta
from . import utils_codey
import tomllib

from . import utils_trendspotting as trendspotting
from fastapi import FastAPI, HTTPException
from google.cloud import bigquery
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
    AudiencesSampleDataResponse
)

# Load configuration file
with open("/code/app/config.toml", "rb") as f:
    config = tomllib.load(f)
project_id = config["global"]["project_id"]
location = config["global"]["location"]
dataset_id = config["global"]["dataset_id"]
prompt_nl_sql = config["global"]["prompt_nl_sql"]
tag_name = config["global"]["tag_name"]

# Trendspotting
bq_client = bigquery.Client(project="rl-llm-dev")
datacatalog_client = datacatalog_v1.DataCatalogClient()

# Text models
llm_latest = bison_latest.from_pretrained(model_name="text-bison@latest")
llm_ga = bison_ga.from_pretrained(model_name="text-bison@001")

# Image models
imagen = ImageGenerationModel.from_pretrained("imagegeneration@002")

app = FastAPI()


@app.post(path="/generate-text")
def post_text_bison_generate(data: TextGenerateRequest) -> TextGenerateResponse:
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
def post_image_generate(data: ImageGenerateRequest) -> ImageGenerateResponse:
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
def post_image_edit(data: ImageEditRequest) -> ImageGenerateResponse:
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
def get_top_search_term(data: TrendTopRequest) -> TrendTopReponse:
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
def post_summarize_news(data: NewsSummaryRequest) -> NewsSummaryResponse:
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
def post_audiences(data: AudiencesRequest) -> AudiencesResponse:
    """Summarize news related to keyword(s)
    Parameters:

    Returns:
        
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
def get_audiences(data: AudiencesSampleDataRequest) -> AudiencesSampleDataResponse:
    """Summarize news related to keyword(s)
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


