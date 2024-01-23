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
import random
import numpy as np
import pandas as pd
import streamlit as st
import vertexai

from google.cloud import translate_v2 as translate
from utils_campaign import generate_names_uuid_dict
from utils_config import GLOBAL_CFG, MODEL_CFG, PAGES_CFG
from utils_image import IMAGEN_API_ENDPOINT, IMAGEN_ENDPOINT 
from utils_image import render_image_edit_prompt 
from utils_image import predict_large_language_model_sample
from utils_streamlit import reset_page_state
from vertexai.preview.language_models import TextGenerationModel


page_cfg = PAGES_CFG["7_email_copy"]

st.set_page_config(page_title=page_cfg["page_title"],
                   page_icon=page_cfg["page_icon"])

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path=page_cfg["sidebar_image_path"]
)

# Set project parameters
PROJECT_ID = GLOBAL_CFG["project_id"]
LOCATION = GLOBAL_CFG["location"]

llm = TextGenerationModel.from_pretrained(
    MODEL_CFG["text"]["text_model_name"])
translate_client = translate.Client()

# Default Campaign key
CAMPAIGNS_KEY = PAGES_CFG["campaigns"]["campaigns_key"]

# State variables for email and image generation
PAGE_KEY_PREFIX = "EmailCopy"
AUDIENCE_DATAFRAME_KEY = f"{PAGE_KEY_PREFIX}_Audience_Dataframe"
SAMPLE_EMAILS_KEY = f"{PAGE_KEY_PREFIX}_Sample_Emails"
GENERATED_EMAILS_KEY = f"{PAGE_KEY_PREFIX}_Generated_Emails"
IMAGE_TO_EDIT_KEY = f"{PAGE_KEY_PREFIX}_Image_To_Edit"
EDITED_IMAGES_KEY = f"{PAGE_KEY_PREFIX}_Edited_Images"
EDIT_IMAGE_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Edit_Image_Prompt"
MASK_IMAGE_KEY = f"{PAGE_KEY_PREFIX}_Mask_Image"
SELECTED_IMAGE_KEY = f"{PAGE_KEY_PREFIX}_Selected_Image" 
FILE_UPLOADER_KEY = f"{PAGE_KEY_PREFIX}_File_Uploader"
IMAGE_OPTION_KEY = f"{PAGE_KEY_PREFIX}_Image_Option"
IMAGES_KEY = f"{PAGE_KEY_PREFIX}_Images"
THEME_KEY = f"{PAGE_KEY_PREFIX}_Theme"
UUID_KEY = f"{PAGE_KEY_PREFIX}_UUID"

# Default values
EMAIL_TEXT_PROMPT = page_cfg["prompt_email_text"]
IMAGE_GENERATION_PROMPT = page_cfg["prompt_image_generation"]
THEMES_FOR_PROMPTS = PAGES_CFG["campaigns"]["prompt_themes"]
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

def generate_information(df: pd.DataFrame) -> pd.DataFrame:
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
    st.session_state[AUDIENCE_DATAFRAME_KEY] = df
    return df

async def email_generate(row: pd.Series, theme: str,
                         images: list=[]) -> pd.Series:
    prompt_row_no_lan = row.drop('language', errors='ignore')

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
    except Exception as e:
        generated_response = None
        print("Error")
        print(str(e))

    if generated_response and generated_response.text:
        generated_text = generated_response.text
    elif theme in THEMES_FOR_PROMPTS and "default_email_copy" in page_cfg:
        index = THEMES_FOR_PROMPTS.index(theme)
        generated_text = page_cfg["default_email_copy"][index]
    else:
        generated_text = "No text was generated for this email."


    email_bar.progress(
        0.3,
        text=f'Generating email image for {prompt_row_no_lan.first_name}')

    image_prompt = IMAGE_GENERATION_PROMPT.format(theme)
    email_bar.progress(
        0.6, 
        text=f'Generating email image for {prompt_row_no_lan.first_name}')

    imageb64 = "data:image/png;base64,"
    image_response = None

    if images:
        imageb64 = random.choice(images)
    else:
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
        elif theme in THEMES_FOR_PROMPTS:
            index = THEMES_FOR_PROMPTS.index(theme)
            with open(page_cfg["local_email_image"][index], 'rb') as fp:
                imageb64 += base64.b64encode(fp.read()).decode('utf-8')

    email_bar.progress(
        0.9,
        text=f'Translating text for {prompt_row_no_lan.first_name}')
    if "language" in row and row.language != "en":
        translation = translate_client.translate(
            generated_text,
            source_language="en",
            target_language=row.language,
            format_="text"
        )['translatedText']
    else:
        translation = generated_text
    email_bar.empty()
    st.toast(f"Email for :blue[{row.first_name}] :green[generated]", icon='✉️')
    return pd.Series(
        [row.first_name, row.email, generated_text, translation, imageb64],
        index=["first_name","email","text","translation","imageb64"]
    )

async def generate_emails(
        number_of_emails:int,
        state_key: str,
        images: list,
        theme: str,
        audience_dataframe: pd.DataFrame
    ):
        async_list = await asyncio.gather(
        *(email_generate(person[1], theme=str(theme), images=images
        ) for person in audience_dataframe.head(number_of_emails).iterrows()))
        st.session_state[state_key] = pd.concat(async_list, axis=1).T
        st.success("All the emails have been generated")


if CAMPAIGNS_KEY in st.session_state:
    campaigns_names = list(generate_names_uuid_dict().keys())
    expander_title = "**Choose a Campaign to get the audience**"
    expanded = True
    if UUID_KEY in st.session_state:
        expander_title = ("Change campaign")
        expanded = False

    with st.expander(expander_title, expanded):
        selected_campaign = st.selectbox(
            "List of Campaigns",
            campaigns_names)
        def choose_campaign():
            selected_uuid = generate_names_uuid_dict()[selected_campaign]
            if (UUID_KEY in st.session_state and 
                st.session_state[UUID_KEY] != selected_uuid):
                reset_page_state(PAGE_KEY_PREFIX)
            st.session_state[UUID_KEY] = selected_uuid
            
        st.button("Retrieve audiences from campaign", on_click=choose_campaign)
        
else:
    st.info("Please generate a campaign first by going to the Campaingns page "
            "and then create an audience in the Audiences page "
            "before using this page.")
if UUID_KEY in st.session_state:
    selected_uuid = st.session_state[UUID_KEY]
    campaign_name = st.session_state[CAMPAIGNS_KEY][selected_uuid].name
    st.subheader(f"Email Copy for campaign '{campaign_name}'")
    if isinstance(st.session_state[CAMPAIGNS_KEY][selected_uuid].audiences,
                  pd.DataFrame):
        audience_dataframe = st.session_state[CAMPAIGNS_KEY][
                            selected_uuid].audiences.copy()
        rows = len(audience_dataframe)
        if rows == 0:
            st.info("Audience is empty.")
        else:
            if "first_name" not in audience_dataframe:
                audience_dataframe = generate_information(audience_dataframe)
                st.session_state[CAMPAIGNS_KEY][
                    selected_uuid].audiences = audience_dataframe.copy()

            st.session_state[AUDIENCE_DATAFRAME_KEY] = audience_dataframe
    else:                  
        st.info("To use this page, please generate "
                f"the audience for campaign '{campaign_name}' "
                "using the Audience page. ")

if AUDIENCE_DATAFRAME_KEY in st.session_state:
    selected_uuid = st.session_state[UUID_KEY]
    campaign_image_dict = st.session_state[
        CAMPAIGNS_KEY][selected_uuid].campaign_uploaded_images
    audience_dataframe = st.session_state[AUDIENCE_DATAFRAME_KEY]
    rows = len(audience_dataframe)
    sample_size = st.slider("Select a sample size", 1,
                            min(10, rows), min(3, rows))
    st.dataframe(audience_dataframe.head(sample_size))

    expander_title = "Choose an option for the images"
    expanded = True
    if IMAGE_OPTION_KEY in st.session_state:
        expander_title = "Change image option"
        expanded = False

    with st.expander(expander_title, expanded):
        image_option_radio = st.radio(
            label="Choose image option", label_visibility="collapsed",
            key=f"{PAGE_KEY_PREFIX}_image_option_radio",
            options=["uploaded", "generated"],
            format_func=lambda x: f"{x.capitalize()} Images")
        def image_option_button():
            st.session_state[IMAGE_OPTION_KEY
                ] = st.session_state[f"{PAGE_KEY_PREFIX}_image_option_radio"]
        st.button("Select", on_click=image_option_button)


    if st.session_state.get(IMAGE_OPTION_KEY, "") == "uploaded":
        render_image_edit_prompt(
            image_to_edit_key=IMAGE_TO_EDIT_KEY,
            edit_image_prompt_key=EDIT_IMAGE_PROMPT_KEY,
            edited_images_key=EDITED_IMAGES_KEY,
            mask_image=True,
            mask_image_key=MASK_IMAGE_KEY,
            select_button=True,
            selected_image_key=SELECTED_IMAGE_KEY,
            file_uploader_key=FILE_UPLOADER_KEY,
            campaign_image_dict=campaign_image_dict,
            local_image_list=page_cfg["local_email_image"]
        )
    if (st.session_state.get(IMAGE_OPTION_KEY, "") == "generated" or 
          SELECTED_IMAGE_KEY in st.session_state):
        theme = st.session_state[CAMPAIGNS_KEY][selected_uuid].theme
        theme_expander_title = "Choose the theme for the email"
        theme_expanded = True
        if THEME_KEY in st.session_state:
            theme_expander_title = "Change the theme"
            theme_expanded = False
        with st.expander(theme_expander_title, theme_expanded):
            campaign_option = st.radio(
                "**Choose the theme for the email**",
                [f"Campaign: '{theme}'", "Custom"],
                label_visibility="collapsed")
            if campaign_option == "Custom":
                other_option = st.text_input("Enter your custom theme...")
            else:
                other_option = ""
                            
            generate_button = st.button("Generate email samples")
        
        if generate_button:
            if campaign_option != "Custom":
                st.session_state[THEME_KEY] = theme
            else:
                if other_option == "":
                    st.info("Please write the custom theme")
                    st.stop()
                st.session_state[THEME_KEY] = other_option
            images = []
            if EDITED_IMAGES_KEY in st.session_state:
                if SELECTED_IMAGE_KEY in st.session_state:
                    images.append(st.session_state[SELECTED_IMAGE_KEY])
                else:
                    images = st.session_state[EDITED_IMAGES_KEY]

            # Convert list of BytesIO images to base64 strings
            if images:
                images = [
                    "data:image/png;base64," +
                    base64.b64encode(image.getvalue()).decode('utf-8')
                    for image in images]
            st.session_state[IMAGES_KEY] = images

            asyncio.run(
                generate_emails(number_of_emails=sample_size,
                                state_key=SAMPLE_EMAILS_KEY,
                                images=st.session_state[IMAGES_KEY],
                                theme=str(st.session_state[THEME_KEY]),
                                audience_dataframe=audience_dataframe))


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
                                    state_key=GENERATED_EMAILS_KEY,
                                    images=st.session_state[IMAGES_KEY],
                                    theme=st.session_state[THEME_KEY],
                                    audience_dataframe=st.session_state[
                                        AUDIENCE_DATAFRAME_KEY]))

if (GENERATED_EMAILS_KEY in st.session_state and UUID_KEY in st.session_state): 
    selected_uuid = st.session_state[UUID_KEY]
    with st.form(PAGE_KEY_PREFIX+"_Link_To_Campaign"):
        link_to_campaign_button = st.form_submit_button("Save to Campaign")

    if link_to_campaign_button:
        emails_copy = st.session_state[GENERATED_EMAILS_KEY].copy()
        st.session_state[CAMPAIGNS_KEY][selected_uuid].emails = emails_copy
        st.success(f"Emails saved to campaign")

