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
import functools
import streamlit as st
import tomllib

from vertexai.preview.language_models import TextGenerationModel
from utils_campaign import add_new_campaign


# Load configuration file
with open("./app_config.toml", "rb") as f:
    data = tomllib.load(f)

st.set_page_config(
    page_title=data["pages"]["campaigns"]["page_title"],
    page_icon=data["pages"]["campaigns"]["page_icon"]
)

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path=data["pages"]["campaigns"]["sidebar_image_path"]
)

# Campaigns unique key
CAMPAIGNS_KEY = data["pages"]["campaigns"]["campaigns_key"]

# Set project parameters 
PROJECT_ID = data["global"]["project_id"]
LOCATION = data["global"]["location"]

# Model configuration
TEXT_MODEL_NAME = data["models"]["text"]["text_model_name"]
IMAGE_MODEL_NAME = data["models"]["image"]["image_model_name"]

# State variables for image and text generation
PAGE_KEY_PREFIX = "CreativeBrief"
BRAND_STATEMENT_KEY = f'{PAGE_KEY_PREFIX}_brand_statement'
PRIMARY_MSG_KEY = f'{PAGE_KEY_PREFIX}_primary_msg'
COMMS_CHANNEL_KEY = f'{PAGE_KEY_PREFIX}_comms_channels'
THEMES_FOR_PROMPTS_KEY = f'{PAGE_KEY_PREFIX}_theme'

# Prompt templates
CYMBAL_OVERVIEW = data["pages"]["campaigns"]["prompt_cymbal_brand_overview"]
BRAND_STATEMENT_PROMPT_TEMPLATE = data["pages"]["campaigns"]["prompt_brand_statement_template"]
PRIMARY_MSG_PROMPT_TEMPLATE = data["pages"]["campaigns"]["prompt_primary_msg_template"]
COMMS_CHANNEL_PROMPT_TEMPLATE = data["pages"]["campaigns"]["prompt_comms_channel_template"]
BUSINESS_NAME = data["pages"]["campaigns"]["prompt_business_name"]
GENDER_FOR_PROMPTS = data["pages"]["campaigns"]["prompt_genders"]
AGEGROUP_FOR_PROMPTS = data["pages"]["campaigns"]["prompt_age_groups"]
OBJECTIVES_FOR_PROMPTS = data["pages"]["campaigns"]["prompt_objectives"]
COMPETITORS_FOR_PROMPTS = data["pages"]["campaigns"]["prompt_competitors"]


cols = st.columns([13, 87])
with cols[0]:
    st.image(data["pages"]["campaigns"]["page_title_icon"])
with cols[1]:
    st.title(data["pages"]["campaigns"]["page_title"])

st.write('''Campaign and creative brief generation.''')

with st.form(CAMPAIGNS_KEY+"_Creation_Form"):
    st.write("**Create a new campaign**")
    campaign_name = st.text_input("Campaign name")

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


campaign_uuid = None
if create_campaign_button:
    llm = TextGenerationModel.from_pretrained(TEXT_MODEL_NAME)
    is_allowed_to_create_campaign = False

    if (CAMPAIGNS_KEY in st.session_state and 
        st.session_state[CAMPAIGNS_KEY].keys()):

        campaigns = st.session_state[CAMPAIGNS_KEY].values()
        campaign_names = {
            campaign.name : str(campaign.unique_uuid) for campaign in campaigns
        }

        if campaign_name in campaign_names:
            st.info(f"Campaign with name '{campaign_name}' already created. "
                     "Provide a unique name.")
        else:
            is_allowed_to_create_campaign = True
    else:
        is_allowed_to_create_campaign = True

    if is_allowed_to_create_campaign:
        async def async_predict(prompt: str, name: str)-> str:
            loop = asyncio.get_running_loop()
            with st.spinner(f"Generating {name}"):
                generated_response = await loop.run_in_executor(
                    None,
                    functools.partial(
                        llm.predict,
                            prompt=prompt, 
                            temperature=0.2, 
                            max_output_tokens=1024, 
                            top_k=40, top_p=0.8))
            if generated_response and generated_response.text:
                return generated_response.text
            return ""
        async def generate_campaign() -> tuple:
            return await asyncio.gather(
                async_predict(
                    BRAND_STATEMENT_PROMPT_TEMPLATE.format(
                        gender_theme=gender_select_theme, 
                        age_theme=age_select_theme,
                        objective_theme=objective_select_theme,
                        competitor_theme=competitor_select_theme,
                        cymbal_overview=CYMBAL_OVERVIEW),
                    "Brand Statement"),
                async_predict(
                    PRIMARY_MSG_PROMPT_TEMPLATE.format(
                        gender_theme=gender_select_theme, 
                        age_theme=age_select_theme,
                        objective_theme=objective_select_theme,
                        competitor_theme=competitor_select_theme,
                        cymbal_overview=CYMBAL_OVERVIEW),
                    "Brand Strategy"),
                async_predict(
                    COMMS_CHANNEL_PROMPT_TEMPLATE.format(
                        gender_theme=gender_select_theme, 
                        age_theme=age_select_theme,
                        objective_theme=objective_select_theme,
                        competitor_theme=competitor_select_theme),
                    "Communication channels")) 
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
            st.success(f"Campaign '{campaign_name}' generated "
                       f"with the uuid '{campaign_uuid}'")
            # Store generated assets
            st.session_state[CAMPAIGNS_KEY][campaign_uuid].brief = {
                'business_name': BUSINESS_NAME,
                'campaign_name': campaign_name,
                'brief_scenario': st.session_state[THEMES_FOR_PROMPTS_KEY],
                'brand_statement': st.session_state[BRAND_STATEMENT_KEY],
                'primary_message': st.session_state[PRIMARY_MSG_KEY],
                'comm_channels': st.session_state[COMMS_CHANNEL_KEY]
            }


if CAMPAIGNS_KEY not in st.session_state:
    st.info('No campaigns created yet, start by creating one.')
elif (CAMPAIGNS_KEY in st.session_state and 
      st.session_state[CAMPAIGNS_KEY].keys()):
    campaigns = st.session_state[CAMPAIGNS_KEY].values()
    campaign_names = {
        campaign.name : str(campaign.unique_uuid) for campaign in campaigns}

    if not create_campaign_button:
        campaigns_list_menu = list(campaign_names.keys())
    else:
        campaigns_list_menu = list(campaign_names.keys())
        idx = campaigns_list_menu.index(campaign_name)
        campaigns_list_menu.insert(0, campaigns_list_menu[idx])
        campaigns_list_menu.pop(idx+1)
    
    with st.form('list_brief_campaigns'):
        st.write("**Active Campaigns**")
        campaign_list_name = st.selectbox(
            'Select a campaign to display its brief', campaigns_list_menu)
        retrieve_brief_button = st.form_submit_button('Retrieve Brief')

    if retrieve_brief_button:
        campaign_uuid = campaign_names[campaign_list_name]

if campaign_uuid:
    brief = st.session_state[CAMPAIGNS_KEY][campaign_uuid].brief
    st.subheader(
        f'Creative Brief for campaign: {brief["campaign_name"]}')
    def bi_column(title:str, content:str):
        col1, col2 = st.columns([28,72])
        with col1:
            st.write(f'**{title}:**')
        with col2:
            st.write(content)
    bi_column("Business name", brief["business_name"])
    bi_column("Scenario", brief["brief_scenario"])
    bi_column("Brand Statement", brief["brand_statement"])
    bi_column("Brand Strategy", brief["primary_message"])
    bi_column("Communication Channels", brief["comm_channels"])

