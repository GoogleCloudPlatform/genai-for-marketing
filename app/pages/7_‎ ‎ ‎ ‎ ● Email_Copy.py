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
Email Copy Generation: 
- Generate email messages that are designed to drive a desired outcome.
- These emails include text and visuals.
"""

import asyncio
import base64
import functools
import numpy as np
import pandas as pd
import streamlit as st
import tomllib
import vertexai

from google.cloud import translate_v2 as translate
from utils_campaign import generate_names_uuid_dict
from utils_image import IMAGEN_API_ENDPOINT, IMAGEN_ENDPOINT 
from utils_image import predict_large_language_model_sample
from vertexai.preview.language_models import TextGenerationModel


# Load configuration file
with open("./app_config.toml", "rb") as f:
    data = tomllib.load(f)

page_cfg = data["pages"]["7_email_copy"]

st.set_page_config(page_title=page_cfg["page_title"],
                   page_icon=page_cfg["page_icon"])

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path=page_cfg["sidebar_image_path"]
)

# Set project parameters
PROJECT_ID = data["global"]["project_id"]
LOCATION = data["global"]["location"]

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION)
llm = TextGenerationModel.from_pretrained(
    data["models"]["text"]["text_model_name"])
translate_client = translate.Client()

# Default Campaign key
CAMPAIGNS_KEY = data["pages"]["campaigns"]["campaigns_key"]

# External states
EMAIL_AUDIENCE_KEY = "TalkToData_insight_Result_Final_Query"

# State variables for email and image generation
PAGE_KEY_PREFIX = "EmailCopy"
AUDIENCE_DATAFRAME_KEY = f"{PAGE_KEY_PREFIX}_Audience_Dataframe"
SAMPLE_EMAILS_KEY = f"{PAGE_KEY_PREFIX}_Sample_Emails"
GENERATED_EMAILS_KEY = f"{PAGE_KEY_PREFIX}_Generated_Emails"

# Default values
EMAIL_TEXT_PROMPT = page_cfg["prompt_email_text"]
IMAGE_GENERATION_PROMPT = page_cfg["prompt_image_generation"]
THEMES_FOR_PROMPTS = page_cfg["prompt_themes"]
SAMPLE_EMAILS = page_cfg["sample_emails"]
AGE_BUCKET = page_cfg["age_bucket"]
MALE_NAMES = page_cfg["male_names"]
FEMALE_NAMES = page_cfg["female_names"]
LANGUAGES = page_cfg["languages"]


cols = st.columns([15, 85])
with cols[0]:
    st.image(page_cfg["page_title_image"])
with cols[1]:
    st.title(page_cfg["page_title"])

st.write(
    """
    This page provides a guided process for generating email copy. 
    The following is a brief list of emails 
    that can be used as a sample to generate email copies.
    """
)

if EMAIL_AUDIENCE_KEY in st.session_state: 
    sample_size = st.slider("Select a sample size", 1, 10, 3)
    audience_dataframe = st.session_state[EMAIL_AUDIENCE_KEY].copy()
else:      
    st.info(
    "Using an auto generated list of emails. "
    "To use a custom list of emails, please generate "
    "the audience first using the Audience Insights page. ")
    sample_size = st.slider("Select a sample size", 1, 10, 3)

    audience_dataframe = pd.DataFrame.from_dict({
        'email': SAMPLE_EMAILS, 
    })


flag_new = True
if AUDIENCE_DATAFRAME_KEY in st.session_state:
    first_email_key = st.session_state[AUDIENCE_DATAFRAME_KEY].at[0, 'email'] 
    first_email_df = audience_dataframe.at[0,'email']
    if first_email_key == first_email_df:
        audience_dataframe = st.session_state[AUDIENCE_DATAFRAME_KEY]
        flag_new = False

if flag_new:
    rng = np.random.default_rng(
        abs(hash(audience_dataframe.at[0,'email']) % (10 ** 8)))
    audience_dataframe['first_name'] = rng.choice(
        FEMALE_NAMES+MALE_NAMES, len(audience_dataframe['email']))
    audience_dataframe['language'] = rng.choice(
        LANGUAGES, len(audience_dataframe['email']))
    audience_dataframe['age_group'] = rng.choice(
        AGE_BUCKET, len(audience_dataframe['email']))
    audience_dataframe['gender'] = audience_dataframe['first_name'].map(
        lambda x: 'woman' if x in FEMALE_NAMES else 'man')
    audience_dataframe['city'] = np.full_like(
        audience_dataframe['email'], 'New York City') 
    st.session_state[AUDIENCE_DATAFRAME_KEY] = audience_dataframe

st.dataframe(audience_dataframe.head(sample_size))

async def email_generate(row: pd.Series, theme: str) -> pd.Series:
    prompt_row_no_lan = row.drop('language')

    email_prompt = EMAIL_TEXT_PROMPT.format(prompt_row_no_lan.to_string(),
                                            theme)
    loop = asyncio.get_running_loop()
    progress_text = f"Generating email text for {prompt_row_no_lan.first_name}"
    email_bar = st.progress(0, text=progress_text)
    generated_text = ""

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
    except:
        generated_response = None

    if generated_response and generated_response.text:
        generated_text = generated_response.text
    else:
        if theme == THEMES_FOR_PROMPTS[0]:
            generated_text = page_cfg["default_email_copy_0"]
        elif theme == THEMES_FOR_PROMPTS[1]:
            generated_text = page_cfg["default_email_copy_1"]
        elif theme == THEMES_FOR_PROMPTS[2]:
            generated_text = page_cfg["default_email_copy_2"]
        elif theme == THEMES_FOR_PROMPTS[3]:
            generated_text = page_cfg["default_email_copy_3"]

    email_bar.progress(
        0.3,
        text=f'Generating email image for {prompt_row_no_lan.first_name}')

    image_prompt = IMAGE_GENERATION_PROMPT.format(theme)
    email_bar.progress(
        0.6, 
        text=f'Generating email image for {prompt_row_no_lan.first_name}')

    imageb64 = "data:image/png;base64,"
    image_response = None

    image_response = await loop.run_in_executor(None, functools.partial(
        predict_large_language_model_sample,
        api_endpoint=IMAGEN_API_ENDPOINT,
        endpoint=IMAGEN_ENDPOINT,
        input={
            "prompt": image_prompt
        },
        parameters={
            'sampleCount': 4,
            'sampleImageSize': 256,
            'aspectRatio': "1:1"
        }))

    if image_response:
        imageb64 += image_response[0]["bytesBase64Encoded"]
    else:
        if theme == THEMES_FOR_PROMPTS[0]:
            with open(page_cfg["default_email_image_0"], 'rb') as fp:
                imageb64 += base64.b64encode(fp.read()).decode('utf-8')
        elif theme == THEMES_FOR_PROMPTS[1]:
            with open(page_cfg["default_email_image_1"], 'rb') as fp:
                imageb64 += base64.b64encode(fp.read()).decode('utf-8')
        elif theme == THEMES_FOR_PROMPTS[2]:
            with open(page_cfg["default_email_image_2"], 'rb') as fp:
                imageb64 += base64.b64encode(fp.read()).decode('utf-8')
        elif theme == THEMES_FOR_PROMPTS[3]:
            with open(page_cfg["default_email_image_3"], 'rb') as fp:
                imageb64 += base64.b64encode(fp.read()).decode('utf-8')

    email_bar.progress(
        0.9,
        text=f'Translating text for {prompt_row_no_lan.first_name}')
    translation = translate_client.translate(
        generated_text,
        source_language="en",
        target_language=row.language,
        format_="text"
    )['translatedText']
    email_bar.empty()
    st.toast(f"Email for :blue[{row.first_name}] :green[generated]", icon='✉️')
    return pd.Series(
        [row.first_name, row.email, generated_text, translation, imageb64],
        index=["first_name","email","text","translation","imageb64"]
    )

# --- Start of FORM
with st.form(PAGE_KEY_PREFIX+'Sample_Email_Form'):
    # st.write("**Choose a theme for the email**")
    theme = st.selectbox("**Choose a theme for the email**",
                         options=THEMES_FOR_PROMPTS)
    generate_samples_button = st.form_submit_button("Generate email samples")

async def generate_emails(number_of_emails:int, state_key: str):
    async_list = await asyncio.gather(
    *(email_generate(person[1], theme=str(theme)
    ) for person in audience_dataframe.head(number_of_emails).iterrows()))
    st.session_state[state_key] = pd.concat(async_list, axis=1).T
    st.success("All the emails have been generated")

if generate_samples_button:
    asyncio.run(generate_emails(number_of_emails=sample_size,
                                state_key=SAMPLE_EMAILS_KEY))

if SAMPLE_EMAILS_KEY in st.session_state:
    st.write("**Generated emails**")
    for row in st.session_state[SAMPLE_EMAILS_KEY].itertuples():
        with st.expander(f"To: {row.first_name} <{row.email}>",
                         expanded=False):
            tab1, tab2 = st.tabs(["English", "Translated"])

            with tab1:
                st.write(row.text)
            with tab2:
                st.write(row.translation)
            st.image(row.imageb64)


with st.form(PAGE_KEY_PREFIX+"_Bulk_Generate_Emails_Form"):
    st.write("**Bulk Generation**")
    number_of_bulk_emails = st.slider(
        "Number of emails to generate from the list.", 1, 50, 3)
    bulk_generate_button = st.form_submit_button("Generate")

if bulk_generate_button:
    asyncio.run(generate_emails(number_of_emails=number_of_bulk_emails,
                                state_key=GENERATED_EMAILS_KEY))

if (GENERATED_EMAILS_KEY in st.session_state and 
    CAMPAIGNS_KEY in st.session_state):
    campaigns_names = generate_names_uuid_dict().keys() 
    with st.form(PAGE_KEY_PREFIX+"_Link_To_Campaign"):
        st.write("**Choose a Campaign to link the results**")
        selected_name = st.selectbox("List of Campaigns", campaigns_names)
        link_to_campaign_button = st.form_submit_button()

    if link_to_campaign_button:
        selected_uuid = generate_names_uuid_dict()[selected_name]
        emails_copy = st.session_state[GENERATED_EMAILS_KEY].copy()
        st.session_state[CAMPAIGNS_KEY][selected_uuid].emails = emails_copy
        st.success(f"Emails linked to campaign {selected_name}")

