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
import streamlit as st
from utils_campaign import CAMPAIGNS_KEY, generate_names_uuid_dict
import utils_config
import numpy as np
import pandas as pd
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from google.cloud import translate_v2 as translate
import utils_default_image_text

from utils_image import IMAGEN_API_ENDPOINT, IMAGEN_ENDPOINT, predict_large_language_model_sample

translate_client = translate.Client()


vertexai.init(
    project=utils_config.get_env_project_id(),
    location=utils_config.LOCATION)
llm = TextGenerationModel.from_pretrained("text-bison")

st.set_page_config(page_title="Email Copy",
                   page_icon="/app/images/favicon.png")

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path='/app/images/menu_icon_2.png'
)

# Set project parameters
PROJECT_ID = utils_config.get_env_project_id()
LOCATION = utils_config.LOCATION

# External states
EMAIL_AUDIENCE_KEY = "TalkToData_insight_Result_Final_Query"

# State variables for email and image generation
PAGE_KEY_PREFIX = "EmailCopy"
AUDIENCE_DATAFRAME_KEY = f"{PAGE_KEY_PREFIX}_Audience_Dataframe"
SAMPLE_EMAILS_KEY = f"{PAGE_KEY_PREFIX}_Sample_Emails"
GENERATED_EMAILS_KEY = f"{PAGE_KEY_PREFIX}_Generated_Emails"

EMAIL_TEXT_PROMPT = (
    "User information: {data}\n"
    "Theme: {theme}\n"
    "Using the user information, "
    "generate a personalized email "
    "with the theme mentioned above for the user") 

IMAGE_GENERATION_PROMPT = "Generate an image for an email copy for {theme}"

THEMES_FOR_PROMPTS = [
    "sales of new women's handbags at Cymbal",
    "introducing a new line of men's leather shoes",
    "new opening of Cymbal concept shoe store in NYC",
    "Cymbal shoes retail brand in NYC"]

SAMPLE_EMAILS = [
"user36410@sample_user36410.sample",
"user39537@sample_user39537.sample",
"user42905@sample_user42905.sample",
"user16185@sample_user16185.sample",
"user27153@sample_user27153.sample",
"user38115@sample_user38115.sample",
"user10294@sample_user10294.sample",
"user14325@sample_user14325.sample",
"user11798@sample_user11798.sample",
"user3917@sample_user3917.sample",
"user7486@sample_user7486.sample",	
"user654@sample_user654.sample",	
"user8239@sample_user8239.sample",	
"user27383@sample_user27383.sample",	
"user16127@sample_user16127.sample",	
"user6385@sample_user6385.sample",	
"user14330@sample_user14330.sample",	
"user17562@sample_user17562.sample",	
"user40714@sample_user40714.sample",	
"user25908@sample_user25908.sample",	
"user22574@sample_user22574.sample"]

AGE_BUCKET = ['young adult', 'middle-aged', 'senior']

MALE_NAMES = [
"James",
"Robert",
"John",
"Michael",
"David",
"William",
"Richard",
"Joseph",
"Thomas",
"Christopher",
"Charles",
"Daniel",
"Matthew",
"Anthony",
"Mark",
"Donald",
"Steven",
"Andrew",
"Paul",
"Joshua"]

FEMALE_NAMES = [
"Mary",
"Patricia",
"Jennifer",
"Linda",
"Elizabeth",
"Barbara",
"Susan",
"Jessica",
"Sarah",
"Karen",
"Lisa",
"Nancy",
"Betty",
"Sandra",
"Margaret",
"Ashley",
"Kimberly",
"Emily",
"Carol",
"Michelle"]

languageS =  ( 
    "es",
    "zh",
    "cs",
    "da",
    "fr",
    "el",
    "it",
    "ja",
    "pt")


cols = st.columns([15, 85])
with cols[0]:
    st.image('/app/images/email_icon.png')
with cols[1]:
    st.title('Email Copy')

st.write(
    """
    This page provides a guided process for generating email copy. 
    The following is a brief list of emails that can be used as a sample to generate email copies.
    """
)

if EMAIL_AUDIENCE_KEY in st.session_state: 
    sample_size = st.slider("Select a sample size", 1, 10, 3)
    audience_dataframe = st.session_state[EMAIL_AUDIENCE_KEY].copy()
else:      
    st.info(
    "Using an auto generated list of emails. "
    "To use a custom list of emails, please generate the audience first using the Audience Insights page. ")
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
        MALE_NAMES, len(audience_dataframe['email']))
        # FEMALE_NAMES+MALE_NAMES, len(audience_dataframe['email']))
    audience_dataframe['language'] = rng.choice(
        languageS, len(audience_dataframe['email']))
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

    email_prompt = EMAIL_TEXT_PROMPT.format(data=prompt_row_no_lan.to_string(), theme=theme)
    loop = asyncio.get_running_loop()
    progress_text = f"Generating email text for {prompt_row_no_lan.first_name}"
    email_bar = st.progress(0, text=progress_text)

    try:
        generated_response = await loop.run_in_executor(None, functools.partial(
            llm.predict,
            prompt=email_prompt,
            temperature=0.2,
            max_output_tokens=1024,
            top_k = 40,
            top_p = 0.8
            ))
    except:
        if theme == THEMES_FOR_PROMPTS[0]:
            generated_text = utils_default_image_text.EMAIL_COPY_TEXT_0
        elif theme == THEMES_FOR_PROMPTS[1]:
            generated_text = utils_default_image_text.EMAIL_COPY_TEXT_1
        elif theme == THEMES_FOR_PROMPTS[2]:
            generated_text = utils_default_image_text.EMAIL_COPY_TEXT_2
        elif theme == THEMES_FOR_PROMPTS[3]:
            generated_text = utils_default_image_text.EMAIL_COPY_TEXT_3
    else:
        if generated_response and generated_response.text:
            generated_text = generated_response.text
        else:
            if theme == THEMES_FOR_PROMPTS[0]:
                generated_text = utils_default_image_text.EMAIL_COPY_TEXT_0
            elif theme == THEMES_FOR_PROMPTS[1]:
                generated_text = utils_default_image_text.EMAIL_COPY_TEXT_1
            elif theme == THEMES_FOR_PROMPTS[2]:
                generated_text = utils_default_image_text.EMAIL_COPY_TEXT_2
            elif theme == THEMES_FOR_PROMPTS[3]:
                generated_text = utils_default_image_text.EMAIL_COPY_TEXT_3

    email_bar.progress(0.3, text=f'Generating email image for {prompt_row_no_lan.first_name}')

    image_prompt = IMAGE_GENERATION_PROMPT.format(theme=theme)
    email_bar.progress(0.6, text=f'Generating email image for {prompt_row_no_lan.first_name}')

    try:
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
    except:
        if theme == THEMES_FOR_PROMPTS[0]:
            with open('/app/images/email_image_0.png', 'rb') as fp:
                imageb64 = base64.b64encode(fp.read()).decode('utf-8')
                imageb64 = "data:image/png;base64,"+imageb64
        elif theme == THEMES_FOR_PROMPTS[1]:
            with open('/app/images/email_image_1.png', 'rb') as fp:
                imageb64 = base64.b64encode(fp.read()).decode('utf-8')
                imageb64 = "data:image/png;base64,"+imageb64
        elif theme == THEMES_FOR_PROMPTS[2]:
            with open('/app/images/email_image_2.png', 'rb') as fp:
                imageb64 = base64.b64encode(fp.read()).decode('utf-8')
                imageb64 = "data:image/png;base64,"+imageb64
        elif theme == THEMES_FOR_PROMPTS[3]:
            with open('/app/images/email_image_3.png', 'rb') as fp:
                imageb64 = base64.b64encode(fp.read()).decode('utf-8')
                imageb64 = "data:image/png;base64,"+imageb64
    else:
        if image_response:
            imageb64 = "data:image/png;base64,"+image_response[0]["bytesBase64Encoded"]
        else:
            if theme == THEMES_FOR_PROMPTS[0]:
                with open('/app/images/email_image_0.png', 'rb') as fp:
                    imageb64 = base64.b64encode(fp.read()).decode('utf-8')
                    imageb64 = "data:image/png;base64,"+imageb64
            elif theme == THEMES_FOR_PROMPTS[1]:
                with open('/app/images/email_image_1.png', 'rb') as fp:
                    imageb64 = base64.b64encode(fp.read()).decode('utf-8')
                    imageb64 = "data:image/png;base64,"+imageb64
            elif theme == THEMES_FOR_PROMPTS[2]:
                with open('/app/images/email_image_2.png', 'rb') as fp:
                    imageb64 = base64.b64encode(fp.read()).decode('utf-8')
                    imageb64 = "data:image/png;base64,"+imageb64
            elif theme == THEMES_FOR_PROMPTS[3]:
                with open('/app/images/email_image_3.png', 'rb') as fp:
                    imageb64 = base64.b64encode(fp.read()).decode('utf-8')
                    imageb64 = "data:image/png;base64,"+imageb64

    email_bar.progress(0.9, text=f'Translating text for {prompt_row_no_lan.first_name}')
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
    theme = st.selectbox("**Choose a theme for the email**", options=THEMES_FOR_PROMPTS)
    generate_samples_button = st.form_submit_button("Generate email samples")

async def generate_emails(number_of_emails:int, state_key: str):
    async_list = await asyncio.gather(
    *(email_generate(person[1], theme=str(theme)
    ) for person in audience_dataframe.head(number_of_emails).iterrows()))
    st.session_state[state_key] = pd.concat(async_list, axis=1).T
    st.success("All the emails have been generated")

if generate_samples_button:
    asyncio.run(generate_emails(number_of_emails=sample_size, state_key=SAMPLE_EMAILS_KEY))

if SAMPLE_EMAILS_KEY in st.session_state:
    st.write("**Generated emails**")
    for row in st.session_state[SAMPLE_EMAILS_KEY].itertuples():
        with st.expander(f"To: {row.first_name} <{row.email}>", expanded=False):
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
    asyncio.run(generate_emails(number_of_emails=number_of_bulk_emails, state_key=GENERATED_EMAILS_KEY))

if GENERATED_EMAILS_KEY in st.session_state and CAMPAIGNS_KEY in st.session_state:
    campaigns_names = generate_names_uuid_dict().keys() 
    with st.form(PAGE_KEY_PREFIX+"_Link_To_Campaign"):
        st.write("**Choose a Campaign to link the results**")
        selected_name = st.selectbox("List of Campaigns", campaigns_names)
        link_to_campaign_button = st.form_submit_button()

    if link_to_campaign_button:
        selected_uuid = generate_names_uuid_dict()[selected_name]
        st.session_state[CAMPAIGNS_KEY][selected_uuid].emails = st.session_state[GENERATED_EMAILS_KEY].copy()
        st.success(f"Emails linked to campaign {selected_name}")

