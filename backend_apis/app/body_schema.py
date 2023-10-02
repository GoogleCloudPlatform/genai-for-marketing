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


class ImageResponse(BaseModel):
    images_base64_string: str
    image_size: tuple
    images_parameters: dict


class ImageGenerateResponse(BaseModel):
    generated_images: list[ImageResponse]


class ImageEditRequest(BaseModel):
    prompt: str
    base_image_bytes: str
    mask_bytes: str | None = None
    number_of_images: int = 1


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


class AudiencesSampleDataRequest(BaseModel):
    table_name: str


class AudiencesSampleDataResponse(BaseModel):
    table_sample: dict
    table_name: str


class ConsumerInsightsRequest(BaseModel):
    query: str


class ConsumerInsightsResponse(BaseModel):
    results: list

