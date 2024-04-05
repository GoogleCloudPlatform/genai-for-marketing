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

from pydantic import BaseModel


class TextGenerateRequest(BaseModel):
    model: str = "latest"
    prompt: str
    temperature: float = 0.2
    top_k: int = 40
    top_p: float = 0.8
    max_output_tokens: int = 1024


class TextGenerateResponse(BaseModel):
    text: str
    safety_attributes: dict


class ImageGenerateRequest(BaseModel):
    prompt: str
    number_of_images: int = 1
    negative_prompt: str | None = None


class ImageResponse(BaseModel):
    id: int
    images_base64_string: str
    image_size: tuple
    images_parameters: dict


class ImageGenerateResponse(BaseModel):
    generated_images: list[ImageResponse]


class ImageEditRequest(BaseModel):
    prompt: str
    base_image_base64: str
    mask_base64: str | None = None
    number_of_images: int = 3
    negative_prompt: str | None = None


class TrendTopRequest(BaseModel):
    trends_date: str


class TrendTopReponse(BaseModel):
    top_search_terms: list[dict]


class NewsSummaryRequest(BaseModel):
    keywords: list[str]
    max_records: int
    max_days: int = 10


class NewsSummaryResponse(BaseModel):
    summaries: list[dict[str, str]]


class AudiencesRequest(BaseModel):
    question: str


class AudiencesResponse(BaseModel):
    audiences: dict
    gen_code: str
    prompt: str


class AudiencesSampleDataRequest(BaseModel):
    table_name: str


class AudiencesSampleDataResponse(BaseModel):
    data: list
    table_name: str


class ConsumerInsightsRequest(BaseModel):
    query: str


class ConsumerInsightsResponse(BaseModel):
    results: list
    llm_summary: str


class BriefCreateRequest(BaseModel):
    campaign_name: str
    business_name: str
    brief_scenario: str
    brand_statement: str
    primary_message: str
    comm_channels: str


class BriefCreateResponse(BaseModel):
    new_folder_id: str
    doc_id: str


class SlidesCreateRequest(BaseModel):
    folder_id: str


class SlidesCreateResponse(BaseModel):
    slide_id: str
    sheet_id: str

class CampaignBrief(BaseModel):
    gender_select_theme: str
    age_select_theme: str
    objective_select_theme: str
    competitor_select_theme: str

class CampaignCreateRequest(BaseModel):
    campaign_name: str
    theme: str
    brief: CampaignBrief
    
class CampaignCreateResponse(BaseModel):
    id:str
    campaign_name: str
    theme: str
    workspace_assets: BriefCreateResponse

class Campaign(BaseModel):
    name: str
    theme: str = ""
    brief: CampaignBrief | None = None
    emails: dict | None = None
    website_post: dict | None = None
    ads_threads: dict | None = None
    ads_insta: dict | None = None
    asset_classes_text: dict | None = None
    asset_classes_images: list | None = None
    workspace_assets: BriefCreateResponse | None = None
    trendspotting_summaries: list | None = None
    audiences: dict | None = None
    campaign_uploaded_images: dict | None = None
    status: str = "Active"

class CampaignList(BaseModel):
    id:str
    data:Campaign
    
class CampaignListResponse(BaseModel):
    results :list[CampaignList] =[]


class TranslateRequest(BaseModel):
    source_text:str
    source_language_code:str | None = None
    target_language_code:str 

class TranslateResponse(BaseModel):
    translated_text:str

class ContentCreationRequest(BaseModel):
    type: str
    theme: str
    context: str | None = None
    no_of_char: int = 500
    audience_age_range: str = '20-30'
    audience_gender:str = 'All'
    image_generate: bool = True

class ContentCreationResponse(BaseModel):
    generated_content:dict
    images: list = []

class CampaignStatusUpdate(BaseModel):
    key :str
    status: str

class BulkEmailGenRequest(BaseModel):
    theme:str
    audience:list
    image_context:str = None
    no_of_emails:int = 10

class PersionalizedEmail(BaseModel):
    email: str
    first_name: str
    text: str
    translation: str
    language: str = 'English'
    generated_image: str = None

class BulkEmailGenResponse(BaseModel):
    persionalized_emails: list[PersionalizedEmail]

class ExportGoogleDocRequest(BaseModel):
    folder_id: str
    doc_name: str
    text: str
    image_prefix: str
    images: list

class ExportGoogleDocResponse(BaseModel):
    doc_id: str

class TexttoSpeechRequest(BaseModel):
    text: str
    prefix: str
    language_code: str = None
    language_name: str = None

class TexttoSpeechResponse(BaseModel):
    audio_uri: str