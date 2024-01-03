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
Marketing Insights demonstration: 
- Render Looker Dashboards with marketing data
- Create personalized headlines and images for marketing campaigns
- Translate content
"""

import asyncio
import base64
from itertools import chain
import pandas as pd
import numpy as np
import random
import streamlit as st

import utils_image
from utils_streamlit import reset_page_state

from utils_campaign import generate_names_uuid_dict
from utils_config import GLOBAL_CFG, MODEL_CFG, PAGES_CFG
from utils_prompt import async_predict_text_llm


page_cfg = PAGES_CFG["10_asset_group"]

st.set_page_config(
    page_title=page_cfg["page_title"], 
    page_icon=page_cfg["page_icon"]
)

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path=page_cfg["sidebar_image_path"]
)

# Set project parameters 
PROJECT_ID = GLOBAL_CFG["project_id"]
LOCATION = GLOBAL_CFG["location"]
TEXT_MODEL_NAME = MODEL_CFG["text"]["text_model_name"]
IMAGE_MODEL_NAME = MODEL_CFG["image"]["image_model_name"]
CAMPAIGNS_KEY = PAGES_CFG["campaigns"]["campaigns_key"]

# State variables for image and text generation
PAGE_KEY_PREFIX = "AssetGroupPmax"
HEADLINE_KEY = f'{PAGE_KEY_PREFIX}_headlines'
LONG_HEADLINE_KEY = f'{PAGE_KEY_PREFIX}_long_headlines'
DESCRIPTION_KEY = f'{PAGE_KEY_PREFIX}_description'
CALL_TO_ACTION_KEY = f'{PAGE_KEY_PREFIX}_call_to_action'
THEMES_FOR_PROMPTS_KEY = f'{PAGE_KEY_PREFIX}_theme'

IMAGE_OPTION = f"{PAGE_KEY_PREFIX}_Image_Upload_Checkbox"
FILE_UPLOADER_KEY = f"{PAGE_KEY_PREFIX}_File_Uploader"
IMAGE_TO_EDIT_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Edit_Prompt_key"

IMAGE_TO_EDIT_KEY = f"{PAGE_KEY_PREFIX}_Image_To_Edit"
MASK_IMAGE_KEY = f"{PAGE_KEY_PREFIX}_Mask_Image"
EDITED_IMAGES_KEY = f"{PAGE_KEY_PREFIX}_Edited_Images"
IMAGE_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Image_Prompt"

GENERATED_IMAGES_KEY = f"{PAGE_KEY_PREFIX}_generated_images"
UUID_KEY = f"{PAGE_KEY_PREFIX}_UUID"
THEME_KEY = f"{PAGE_KEY_PREFIX}_Theme"

IMAGE_GENERATION_PROMPT = page_cfg["image_generation_prompt"]
BRAND_OVERVIEW = PAGES_CFG["campaigns"].get("prompt_brand_overview", "")

# Prompt templates
HEADLINE_PROMPT_TEMPLATE = page_cfg["headline_prompt_template"]
LONG_HEADLINE_PROMPT_TEMPLATE = page_cfg["load_headline_prompt_template"]
DESCRIPTION_PROMPT_TEMPLATE = page_cfg["description_prompt_template"]
BUSINESS_NAME = page_cfg["business_name"]
CALL_TO_ACTION = page_cfg["call_to_action"]
THEMES_FOR_PROMPTS = PAGES_CFG["campaigns"]["prompt_themes"]


cols = st.columns([15, 85])
with cols[0]:
    st.image(page_cfg["page_title_image"])
with cols[1]:
    st.title(page_cfg["page_title"])

st.write("""Generate an asset group for PMax using Vertex AI PaLM 2 API.""")

if CAMPAIGNS_KEY in st.session_state:
    campaigns_names = list(generate_names_uuid_dict().keys())
    expander_title = "**Choose a Campaign**"
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
            
        st.button("Choose campaign", on_click=choose_campaign)
        
else:
    st.info("Please generate a campaign first by going to the Campaingns page "
            "before using this page.")
if UUID_KEY in st.session_state:
    selected_uuid = st.session_state[UUID_KEY]
    campaign_name = st.session_state[CAMPAIGNS_KEY][selected_uuid].name
    campaign_theme = st.session_state[CAMPAIGNS_KEY][selected_uuid].theme
    st.subheader(f"Asset Group for PMax for campaign '{campaign_name}'")

    with st.form(key='form_theme'):
        placeholder_for_options_theme = st.empty()
        placeholder_for_custom_theme = st.empty()

        image_option = st.radio(label="Choose an option for the images:",
                 options=["uploaded", "generated"],
                 format_func=lambda x: f"{x.capitalize()} Images")
        
        generation_button = st.form_submit_button("Generate")
    # Create selectbox
    with placeholder_for_options_theme:
        theme_option = st.radio(
        "Choose the theme to generate an asset group for PMax.",
        [f"Campaign: '{campaign_theme}'", "Custom"])

    # Create text input for user entry
    with placeholder_for_custom_theme:
        if theme_option == "Custom":
            theme_other = st.text_input("Enter your custom theme...")
        else:
            theme_other = ""

    if generation_button:
        if theme_option != "Custom":
            theme = campaign_theme
        else:
            if theme_other == "":
                st.info("Please write the custom theme")
                st.stop()

            theme = theme_other
        # Initialize variables
        if GENERATED_IMAGES_KEY in st.session_state:
            del st.session_state[GENERATED_IMAGES_KEY]
        if EDITED_IMAGES_KEY in st.session_state:
            del st.session_state[EDITED_IMAGES_KEY]
        if IMAGE_TO_EDIT_KEY in st.session_state:
            del st.session_state[IMAGE_TO_EDIT_KEY]
        if IMAGE_TO_EDIT_PROMPT_KEY in st.session_state:
            del st.session_state[IMAGE_TO_EDIT_PROMPT_KEY]
        if FILE_UPLOADER_KEY in st.session_state:
            del st.session_state[FILE_UPLOADER_KEY]

        st.session_state[IMAGE_OPTION] = image_option

        async def generate_brief() -> tuple:
            return await asyncio.gather(
                async_predict_text_llm(
                    prompt=HEADLINE_PROMPT_TEMPLATE.format(
                        theme,
                        BRAND_OVERVIEW),
                    name="Headline",
                    pretrained_model=TEXT_MODEL_NAME,
                    max_output_tokens=256
                ),
                async_predict_text_llm(
                    prompt=LONG_HEADLINE_PROMPT_TEMPLATE.format(
                        theme,
                        BRAND_OVERVIEW),
                    name="Long Headline",
                    pretrained_model=TEXT_MODEL_NAME,
                ),
                async_predict_text_llm(
                    prompt=DESCRIPTION_PROMPT_TEMPLATE.format(
                        theme,
                        BRAND_OVERVIEW),
                    name="Description",
                    pretrained_model=TEXT_MODEL_NAME))

        try:
            generated_brief = asyncio.run(generate_brief())
            st.session_state[HEADLINE_KEY] = generated_brief[0]
            st.session_state[LONG_HEADLINE_KEY] = generated_brief[1]
            st.session_state[DESCRIPTION_KEY] = generated_brief[2]
        except Exception as e:
            print(e)

        if (not st.session_state[HEADLINE_KEY] and 
            "asset_group_headlines" in page_cfg):
            st.session_state[HEADLINE_KEY] = page_cfg[
                "asset_group_headlines"]

        if (not st.session_state[LONG_HEADLINE_KEY] and 
            "asset_group_long_headlines" in page_cfg):
            st.session_state[LONG_HEADLINE_KEY] = page_cfg[
                "asset_group_long_headlines"]

        if (not st.session_state[HEADLINE_KEY] and
            "asset_group_description" in page_cfg):
            st.session_state[HEADLINE_KEY] = page_cfg[
               "asset_group_description"]

        st.session_state[CALL_TO_ACTION_KEY] = random.choice(CALL_TO_ACTION)
        st.session_state[THEMES_FOR_PROMPTS_KEY] = theme

if (UUID_KEY in st.session_state and
    THEMES_FOR_PROMPTS_KEY in st.session_state and
    HEADLINE_KEY in st.session_state and
    LONG_HEADLINE_KEY in st.session_state and
    DESCRIPTION_KEY in st.session_state and
    CALL_TO_ACTION_KEY in st.session_state):
    selected_uuid = st.session_state[UUID_KEY]
    campaign_image_dict = st.session_state[
        CAMPAIGNS_KEY][selected_uuid].campaign_uploaded_images

    st.subheader('Asset Group for PMax')

    st.write(f'**Business name:** {BUSINESS_NAME}')
    st.write(f'**Scenario:** {st.session_state[THEMES_FOR_PROMPTS_KEY]}')

    col1, col2 = st.columns([20,80])
    with col1:
        st.write('**Headlines**')
    with col2:
        st.write(f'{st.session_state[HEADLINE_KEY]}')

    col1, col2 = st.columns([20,80])
    with col1:
        st.write('**Long Headlines**')
    with col2:
        st.write(f'{st.session_state[LONG_HEADLINE_KEY]}')

    col1, col2 = st.columns([20,80])
    with col1:
        st.write('**Description**')
    with col2:
        st.write(f'{st.session_state[DESCRIPTION_KEY]}')

    col1, col2 = st.columns([20,80])
    with col1:
        st.write('**Call to action**')
    with col2:
        st.write(f'{st.session_state[CALL_TO_ACTION_KEY]}')

    if st.session_state[IMAGE_OPTION] == "uploaded":
        utils_image.render_image_edit_prompt(
            edited_images_key=GENERATED_IMAGES_KEY,
            edit_image_prompt_key=IMAGE_TO_EDIT_PROMPT_KEY,
            upload_file=True,
            image_to_edit_key=IMAGE_TO_EDIT_KEY,
            mask_image=True,
            mask_image_key=MASK_IMAGE_KEY,
            download_button=False,
            file_uploader_key=FILE_UPLOADER_KEY,
            select_button=False,
            campaign_image_dict=campaign_image_dict,
            local_image_list=list(chain.from_iterable(
                page_cfg["local_image_asset"]))
        )
    else:

        if GENERATED_IMAGES_KEY not in st.session_state:
            with st.spinner('Generating images...'):
                utils_image.image_generation(
                    IMAGE_GENERATION_PROMPT.format(
                        st.session_state[THEMES_FOR_PROMPTS_KEY]),
                    8,
                    256,
                    '1:1',
                    GENERATED_IMAGES_KEY)

        theme = st.session_state[THEMES_FOR_PROMPTS_KEY]
        if st.session_state[GENERATED_IMAGES_KEY]:
            st.write('**Generated images**')
            utils_image.generate_image_columns(GENERATED_IMAGES_KEY,
                                               download_button=False)
        elif theme in THEMES_FOR_PROMPTS:
            index = THEMES_FOR_PROMPTS.index(theme)
            with open(page_cfg["local_image_asset"][index][0], "rb") as fp:
                st.session_state[GENERATED_IMAGES_KEY].append(
                    {"bytesBase64Encoded":base64.b64encode(
                        fp.read()).decode('utf-8')})
            with open(page_cfg["local_image_asset"][index][1], "rb") as fp:
                st.session_state[GENERATED_IMAGES_KEY].append(
                    {"bytesBase64Encoded":base64.b64encode(
                        fp.read()).decode('utf-8')})

if (UUID_KEY in st.session_state and
    HEADLINE_KEY in st.session_state and 
    CAMPAIGNS_KEY in st.session_state and 
    (GENERATED_IMAGES_KEY in st.session_state or 
     (IMAGE_TO_EDIT_KEY in st.session_state and 
      FILE_UPLOADER_KEY in st.session_state))):
    selected_uuid = st.session_state[UUID_KEY]
    campaign_name = st.session_state[CAMPAIGNS_KEY][selected_uuid].name

    with st.form(PAGE_KEY_PREFIX+"_Link_To_Campaign"):
        link_to_campaign_button = st.form_submit_button(label="Save to Campaign")

    if link_to_campaign_button:

        assets_group_dict = {}
        assets_group_dict.update({'business_name': BUSINESS_NAME})
        assets_group_dict.update(
            {'scenario':st.session_state[THEMES_FOR_PROMPTS_KEY]})
        assets_group_dict.update({'headline':st.session_state[HEADLINE_KEY]})
        assets_group_dict.update(
            {'long_headline':st.session_state[LONG_HEADLINE_KEY]})
        assets_group_dict.update(
            {'description':st.session_state[DESCRIPTION_KEY]})
        assets_group_dict.update(
            {'call_to_action':st.session_state[CALL_TO_ACTION_KEY]})

        assets_text_pd = pd.DataFrame().from_dict(
            assets_group_dict,
            orient='index',
            columns=['text_assets']
        )

        st.session_state[CAMPAIGNS_KEY][
                         selected_uuid].asset_classes_text = assets_text_pd

        assets_images_pd = pd.DataFrame()
        if GENERATED_IMAGES_KEY in st.session_state:
            for i, value in enumerate(st.session_state[GENERATED_IMAGES_KEY]):
                assets_images_pd.insert(
                    i,
                    column=f'image_{i}',
                    value=np.array(
                        ["data:image/png;base64,"+value["bytesBase64Encoded"]])
                )
        else:
            assets_images_pd.insert(
                0, 
                column='image_0', 
                value=np.array(["data:image/png;base64,"+base64.b64encode(
                    st.session_state[IMAGE_TO_EDIT_KEY]).decode('utf-8')]))


        st.session_state[CAMPAIGNS_KEY][
                         selected_uuid].asset_classes_images = assets_images_pd
        st.success(f"Asset group linked to campaign {campaign_name}")

