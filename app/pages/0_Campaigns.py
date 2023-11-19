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
Initial page with an overview architecture and a description of each demo page.
"""

import asyncio
from itertools import cycle
import streamlit as st
import streamlit.components.v1 as components
import time
import utils_workspace

from PIL import Image, ImageOps
from vertexai.preview.language_models import TextGenerationModel
from utils_campaign import Campaign, add_new_campaign
from utils_prompt import async_predict_text_llm
from utils_config import GLOBAL_CFG, MODEL_CFG, PAGES_CFG


# Load configuration file

page_cfg = PAGES_CFG["campaigns"]
st.set_page_config(
    page_title=page_cfg["page_title"],
    page_icon=page_cfg["page_icon"]
)

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path=page_cfg["sidebar_image_path"]
)

DOMAIN = page_cfg["domain"]

# Campaigns unique key
CAMPAIGNS_KEY = page_cfg["campaigns_key"]

# Set project parameters 
PROJECT_ID = GLOBAL_CFG["project_id"]
LOCATION = GLOBAL_CFG["location"]

# Model configuration
TEXT_MODEL_NAME = MODEL_CFG["text"]["text_model_name"]
IMAGE_MODEL_NAME = MODEL_CFG["image"]["image_model_name"]

# State variables for image and text generation
PAGE_KEY_PREFIX = "CreativeBrief"
BRAND_STATEMENT_KEY = f'{PAGE_KEY_PREFIX}_brand_statement'
PRIMARY_MSG_KEY = f'{PAGE_KEY_PREFIX}_primary_msg'
COMMS_CHANNEL_KEY = f'{PAGE_KEY_PREFIX}_comms_channels'
THEMES_FOR_PROMPTS_KEY = f'{PAGE_KEY_PREFIX}_theme'

FILE_UPLOADER_KEY = f"{PAGE_KEY_PREFIX}_File_Uploader"

# Prompt templates
BRAND_OVERVIEW = page_cfg.get("prompt_brand_overview", "")
BRAND_STATEMENT_PROMPT_TEMPLATE = page_cfg["prompt_brand_statement_template"]
PRIMARY_MSG_PROMPT_TEMPLATE = page_cfg["prompt_primary_msg_template"]
COMMS_CHANNEL_PROMPT_TEMPLATE = page_cfg["prompt_comms_channel_template"]
BUSINESS_NAME = page_cfg["prompt_business_name"]
GENDER_FOR_PROMPTS = page_cfg["prompt_genders"]
AGEGROUP_FOR_PROMPTS = page_cfg["prompt_age_groups"]
OBJECTIVES_FOR_PROMPTS = page_cfg["prompt_objectives"]
COMPETITORS_FOR_PROMPTS = page_cfg["prompt_competitors"]
PROMPT_THEMES = page_cfg["prompt_themes"]

# Variables for Workspace integration
DOC_TEMPLATE_ID = PAGES_CFG["12_review_activate"]["doc_template_id"]
DRIVE_FOLDER_ID = PAGES_CFG["12_review_activate"]["drive_folder_id"]

DOC_ID_KEY = f"{CAMPAIGNS_KEY}_doc_id_key"
NEW_FOLDER_KEY = f"{CAMPAIGNS_KEY}_new_folder_id_key"


cols = st.columns([13, 87])
with cols[0]:
    st.image(page_cfg["page_title_icon"])
with cols[1]:
    st.title(page_cfg["page_title"])

tab1, tab2 = st.tabs(["Create Campaign", "Existing Campaigns"])

with tab1:
    with st.form(CAMPAIGNS_KEY+"_Creation_Form"):
        st.write("**Create a new campaign**")
        campaign_name = st.text_input("Campaign name")

        placeholder_for_selectbox_theme = st.empty()
        placeholder_for_custom_theme = st.empty()

        st.write("**Creative brief inputs**")
        cols = st.columns([1, 1])

        with cols[0]:
            gender_select_theme = st.selectbox(
            'Select the targeted gender:',
            options=GENDER_FOR_PROMPTS)
        with cols[1]:
            age_select_theme = st.selectbox(
            'Select the targeted age group:',
            options=AGEGROUP_FOR_PROMPTS)
        
        col1, col2 = st.columns([1,1])
        with col1:
            objective_select_theme = st.selectbox(
                'Select the objective:',
                options=OBJECTIVES_FOR_PROMPTS)

        with col2:
            competitor_select_theme = st.selectbox(
                'Select the chief competitor:',
                options=COMPETITORS_FOR_PROMPTS)

        create_campaign_button = st.form_submit_button()
    # Create selectbox
    with placeholder_for_selectbox_theme:
        options = PROMPT_THEMES + ["Another theme..."]
        selection = st.selectbox("Select a theme", options=options)

    # Create text input for user entry
    with placeholder_for_custom_theme:
        if selection == "Another theme...":
            other_option = st.text_input("Enter your custom theme...")
        else:
            other_option = ""

    campaign_uuid = None
    if create_campaign_button:
        theme = ""
        if selection != "Another theme...":
            theme = selection
        else:
            if other_option == "":
                st.info("Please write the custom theme")

            theme = other_option
        llm = TextGenerationModel.from_pretrained(TEXT_MODEL_NAME)
        is_allowed_to_create_campaign = False

        if (CAMPAIGNS_KEY in st.session_state and 
            st.session_state[CAMPAIGNS_KEY].keys()):

            campaigns = st.session_state[CAMPAIGNS_KEY].values()
            campaign_names = {
                campaign.name : str(
                    campaign.unique_uuid) for campaign in campaigns
            }

            if campaign_name in campaign_names:
                st.info(f"Campaign with name '{campaign_name}' "
                        "already created. "
                        "Provide a unique name.")
            else:
                is_allowed_to_create_campaign = True
        else:
            is_allowed_to_create_campaign = True

        if is_allowed_to_create_campaign and theme != "":
            async def generate_campaign() -> tuple:
                return await asyncio.gather(
                    async_predict_text_llm(
                        BRAND_STATEMENT_PROMPT_TEMPLATE.format(
                            gender_select_theme, 
                            age_select_theme,
                            objective_select_theme,
                            competitor_select_theme,
                            BRAND_OVERVIEW),
                        "Brand Statement",
                        TEXT_MODEL_NAME),
                    async_predict_text_llm(
                        PRIMARY_MSG_PROMPT_TEMPLATE.format(
                            gender_select_theme, 
                            age_select_theme,
                            objective_select_theme,
                            competitor_select_theme,
                            BRAND_OVERVIEW),
                        "Brand Strategy",
                        TEXT_MODEL_NAME),
                    async_predict_text_llm(
                        COMMS_CHANNEL_PROMPT_TEMPLATE.format(
                            gender_select_theme, 
                            age_select_theme,
                            objective_select_theme,
                            competitor_select_theme),
                        "Communication channels",
                        TEXT_MODEL_NAME)) 
            try:
                generated_tuple = asyncio.run(generate_campaign())
                st.session_state[BRAND_STATEMENT_KEY] = generated_tuple[0] 
                st.session_state[PRIMARY_MSG_KEY] = generated_tuple[1]
                st.session_state[COMMS_CHANNEL_KEY] = generated_tuple[2]
                st.session_state[THEMES_FOR_PROMPTS_KEY] = (
                    f'Targeting gender: {gender_select_theme}, '
                    f'Age group: {age_select_theme}, '
                    f'Campaign objective: {objective_select_theme}, '
                    f'Competitor: {competitor_select_theme}')
            except:
                st.info('Something went wrong with your prompt. Try again.')
            else:
                campaign_uuid = add_new_campaign(campaign_name)
                # Store generated assets
                st.session_state[CAMPAIGNS_KEY][campaign_uuid].brief = {
                    'business_name': BUSINESS_NAME,
                    'campaign_name': campaign_name,
                    'brief_scenario': st.session_state[THEMES_FOR_PROMPTS_KEY],
                    'brand_statement': st.session_state[BRAND_STATEMENT_KEY],
                    'primary_message': st.session_state[PRIMARY_MSG_KEY],
                    'comm_channels': st.session_state[COMMS_CHANNEL_KEY]
                }
                st.session_state[CAMPAIGNS_KEY][
                    campaign_uuid].theme = theme
                # local reference
                brief = st.session_state[CAMPAIGNS_KEY][campaign_uuid].brief 

            try:
                with st.spinner("Creating Google Drive folder..."):
                    new_folder_id = utils_workspace.create_folder_in_folder(
                        folder_name=f"Marketing_Assets_{int(time.time())}",
                        parent_folder_id=DRIVE_FOLDER_ID)
                    st.session_state[NEW_FOLDER_KEY] = new_folder_id
                    utils_workspace.set_permission(
                        file_id=new_folder_id,
                        domain=DOMAIN)
                with st.spinner("Uploading Creative Brief to Google Docs..."):
                    doc_id = utils_workspace.copy_drive_file(
                        drive_file_id=DOC_TEMPLATE_ID,
                        parentFolderId=new_folder_id,
                        copy_title=f"GenAI Marketing Brief")
                    st.session_state[DOC_ID_KEY] = doc_id
                    clean = lambda x: x.replace("*", "").strip()
                    utils_workspace.update_doc(
                        document_id=doc_id,
                        campaign_name= campaign_name,
                        business_name=clean(brief["business_name"]), 
                        scenario=clean(brief["brief_scenario"]), 
                        brand_statement=clean(brief["brand_statement"]),
                        primary_msg=clean(brief["primary_message"]), 
                        comms_channel=clean(brief["comm_channels"]))
            except:
                del st.session_state[CAMPAIGNS_KEY][campaign_uuid]
                st.info("Campaign could not be created. Please try again.")
            else:
                st.success(f"Campaign '{campaign_name}' generated "
                           f"with the uuid '{campaign_uuid}'")
                st.success("Brief document uploaded to Google Docs.")
                st.session_state[CAMPAIGNS_KEY][
                    campaign_uuid].workspace_assets = {}
                st.session_state[CAMPAIGNS_KEY][
                    campaign_uuid].workspace_assets["brief_docs_id"]=doc_id
                st.session_state[CAMPAIGNS_KEY][
                    campaign_uuid].workspace_assets["folder_id"]=new_folder_id

                if st.session_state[CAMPAIGNS_KEY][
                    campaign_uuid].workspace_assets["brief_docs_id"]:
                    components.iframe(
                        src=f'https://docs.google.com/file/d/{doc_id}/preview',
                        height=1000
                    )


def display_campaigns_upload(
        campaign: Campaign
):
    if campaign.workspace_assets == None:
        return
    docs_link = f'https://docs.google.com/document/d/{campaign.workspace_assets["brief_docs_id"]}/edit'
    docs_link_preview = f'https://docs.google.com/file/d/{campaign.workspace_assets["brief_docs_id"]}/preview'
    folder_link = f'http://drive.google.com/corp/drive/folders/{campaign.workspace_assets["folder_id"]}'

    with st.form(
        key=f"{PAGE_KEY_PREFIX}_{str(campaign.unique_uuid)}_form", 
        clear_on_submit=True):
        st.write(f"**Campaign name**: {campaign.name}")
        st.write(f"**Campaign theme**: {campaign.theme}")
        st.write(f"**Workspace**: [Edit brief in Google Docs ↗]({docs_link}) | "
            f"[Explore files in Google Drive ↗]({folder_link})")


        if campaign.campaign_uploaded_images:
            st.write("**Campaign images**:")
            images = campaign.campaign_uploaded_images.values() 
            cols = cycle(st.columns(4)) 
            for im in images:
                next(cols).image(im["thumbnail"], width=150, caption=im["name"])

        uploaded_files = st.file_uploader(
            "Upload images to your campaign. It MUST be in PNG or JPEG format.",
            type=['png', 'jpg'],
            key=FILE_UPLOADER_KEY+str(campaign.unique_uuid),
            accept_multiple_files=True)
        
        cols = st.columns([0.4,0.8])

        with cols[0]:
            submit_button = st.form_submit_button("Save images to Campaign")
        
        with cols[1]:
            placeholder_for_toggle = st.empty()

        placeholder_for_iframe = st.empty()

    with placeholder_for_toggle:
        preview_docs_toggle = st.toggle(
            label="Preview brief",
            key=str(campaign.unique_uuid)+"_toggle"
        )

    with placeholder_for_iframe.container():
        if preview_docs_toggle:
            components.iframe(
                src=docs_link_preview,
                height=1000
            )

    if submit_button:
        with st.spinner("Uploading files to Google Drive..."):
            if uploaded_files:
                if not campaign.campaign_uploaded_images:
                    campaign.campaign_uploaded_images = {}
                for file in uploaded_files:
                    try:
                        file_id = utils_workspace.upload_to_folder(
                            f=file,
                            folder_id=campaign.workspace_assets["folder_id"],
                            upload_name=file.name,
                            mime_type=file.type
                        )
                    except:
                        st.error("Could not upload one or more images. "
                                 "Please try again.")
                    else:
                        im = Image.open(file).convert("RGB")
                        im = ImageOps.fit(im, (150, 150))
                        campaign.campaign_uploaded_images[file_id] = {
                                "name":file.name,
                                "mime_type":file.type,
                                "size":file.size,
                                "thumbnail":im
                            }
                        st.success(f"File {file.name} uploaded to campaign.")
                st.rerun()
            else:
                st.info("Please select image(s) before saving to Drive.")

with tab2:
    if CAMPAIGNS_KEY not in st.session_state:
        st.info('No campaigns created yet, start by creating one.')
    elif (CAMPAIGNS_KEY in st.session_state and 
        st.session_state[CAMPAIGNS_KEY].keys()):
        st.subheader("List of existing campaigns")
        st.write("\n")
        for c in st.session_state[CAMPAIGNS_KEY].values():
            display_campaigns_upload(c)
