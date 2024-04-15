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
Email Generation: 
- Generate email messages that are designed to drive a desired outcome.
- These emails include text and visuals.
"""

import asyncio
import functools
import numpy as np
import pandas as pd
import vertexai
import tomllib
import io
import base64
from PIL import Image

from google.cloud import translate_v2 as translate
from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.vision_models import ImageGenerationModel


# Load configuration file
with open("/app/config.toml", "rb") as f:
    config = tomllib.load(f)
project_id = config["global"]["project_id"]
location = config["global"]["location"]

vertexai.init(
    project=project_id,
    location=location)
llm = TextGenerationModel.from_pretrained(
    config["models"]["text_model_name"])
imagen = ImageGenerationModel.from_pretrained(config["models"]["image_model_name"])
translate_client = translate.Client()

# Default values
EMAIL_TEXT_PROMPT = config["prompts"]["prompt_email_text"]
AGE_BUCKET = config["data_sample"]["age_bucket"]
MALE_NAMES = config["data_sample"]["male_names"]
FEMALE_NAMES = config["data_sample"]["female_names"]
LANGUAGES = config["data_sample"]["languages"]
LANGUAGES_MAP = config["data_sample"]["languages_map"]

IMAGE_PROMPT = config["prompts"]["prompt_image_generation"]

def generate_information(data : list) -> pd.DataFrame:
    df = pd.DataFrame.from_dict(data)
    rng = np.random.default_rng(
        abs(hash(df.at[0,'email']) % (10 ** 8)))
    df['first_name'] = rng.choice(
        FEMALE_NAMES+MALE_NAMES, len(df['email']))
    df['language'] = rng.choice(
        LANGUAGES, len(df['email']))
    df['age_group'] = rng.choice(
        AGE_BUCKET, len(df['email']))
    df['gender'] = df['first_name'].map(
        lambda x: 'woman' if x in FEMALE_NAMES else 'man')
    df['city'] = np.full_like(
        df['email'], 'New York City') 
    return df

async def email_generate(row: pd.Series, theme: str, image_context: str) -> pd.Series:
    prompt_row = row['first_name']
    
    email_prompt = EMAIL_TEXT_PROMPT.format(prompt_row,
                                            theme)
    loop = asyncio.get_running_loop()
    progress_text = f"Generating email text for {prompt_row}"
    print(progress_text)
    generated_text = ""
    generated_images = []

    try:
        generated_response = await loop.run_in_executor(
            None, 
            functools.partial(
                llm.predict,
                prompt=email_prompt,
                temperature=0.2,
                max_output_tokens=1024,
                top_k = 40,
                top_p = 0.8
                ))
    except Exception as e:
        generated_response = None
        print("Error")
        print(str(e))

    if generated_response and generated_response.text:
        generated_text = generated_response.text
    else:
        generated_text = "No text was generated for this email."

    if "language" in row and row.language != "en":
        translation = translate_client.translate(
            generated_text,
            source_language="en",
            target_language=row.language,
            format_="text"
        )['translatedText']
    else:
        translation = generated_text
    if image_context != None and image_context != '':
        try:
            prompt_image = IMAGE_PROMPT
            
            imagen_responses = await loop.run_in_executor(
                None,
                functools.partial(
                    imagen.generate_images,
                        prompt=prompt_image.format(
                            image_context
                            ), 
                        number_of_images=1))
        except Exception as e:
            print(prompt_image.format(
                            image_context
                            ))
            print(str(e))
        else:
            for image in imagen_responses:
                generated_images.append(
                    {
                        "images_base64_string": image._as_base64_string(),
                    }
                )
    if len(generated_images) > 0 :
        generated_image = generated_images[0]["images_base64_string"]
        buffer = io.BytesIO()
        imgdata = base64.b64decode(generated_image)
        img = Image.open(io.BytesIO(imgdata))
        new_img = img.resize((250, 250))
        new_img.save(buffer, format="PNG")
        generated_image = base64.b64encode(buffer.getvalue())
    else:
        generated_image = ''

    return pd.Series(
        [row.first_name, row.email, generated_text, translation,LANGUAGES_MAP[row.language],generated_image],
        index=["first_name","email","text","translation","language","generated_image"]
    )

async def generate_emails(
        number_of_emails:int,
        theme: str,
        audience_data: list,
        image_context:str
    ):
        audience_dataframe = pd.DataFrame.from_dict(audience_data)
        async_list = await asyncio.gather(
        *(email_generate(person[1], theme=str(theme),image_context=image_context
        ) for person in audience_dataframe.head(number_of_emails).iterrows()))
        #print(async_list)
        df = pd.concat(async_list,axis=1).T.to_dict('records')
        return df


