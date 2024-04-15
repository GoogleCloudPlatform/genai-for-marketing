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


"""
A utility module for performing prompt engineering with the Vertex PaLM API.
"""


import asyncio
import functools
import vertexai
import tomllib

# Load configuration file
with open("/app/config.toml", "rb") as f:
    config = tomllib.load(f)
project_id = config["global"]["project_id"]
location = config["global"]["location"]

vertexai.init(project=project_id, location=location)

from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.vision_models import ImageGenerationModel

from vertexai.generative_models import GenerativeModel , GenerationConfig


async def async_predict_text_gemini(
        prompt: str,
        model_name: str="gemini-1.0-pro",
        max_output_tokens: int=2048,
        temperature: float=0.4,
        top_k: int=40,
        top_p: float=0.8
    )-> str:
    loop = asyncio.get_running_loop()
    llm = GenerativeModel(model_name)
    generated_response = None
    generation_config = GenerationConfig(
    temperature=temperature,
    top_p=top_p,
    top_k=top_k,
    candidate_count=1,
    max_output_tokens=max_output_tokens,
)
    try:
        generated_response = await loop.run_in_executor(
            None,
            functools.partial(
                llm.generate_content,
                    prompt, 
                    generation_config=generation_config))
    except Exception as e:
        print(e)

    if generated_response and generated_response.text:
        return generated_response.text
    return ""

async def async_predict_text_llm(
        prompt: str,
        pretrained_model: str,
        max_output_tokens: int=1024,
        temperature: float=0.4,
        top_k: int=40,
        top_p: float=0.8
    )-> str:
    loop = asyncio.get_running_loop()
    llm = TextGenerationModel.from_pretrained(pretrained_model)
    generated_response = None
   
    try:
        generated_response = await loop.run_in_executor(
            None,
            functools.partial(
                llm.predict,
                    prompt=prompt, 
                    temperature=temperature, 
                    max_output_tokens=max_output_tokens, 
                    top_k=top_k, top_p=top_p))
    except Exception as e:
        print(e)

    if generated_response and generated_response.text:
        return generated_response.text
    return ""

async def async_generate_image(prompt,number_of_images=4):
    loop = asyncio.get_running_loop()
    # Image models
    imagen = ImageGenerationModel.from_pretrained(config["models"]["image_model_name"])
    try:
        imagen_responses = await loop.run_in_executor(
            None,
            functools.partial(
                imagen.generate_images,
                    prompt=prompt, 
                    number_of_images=number_of_images))
    except Exception as e:
        print(str(e))
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
        return generated_images

