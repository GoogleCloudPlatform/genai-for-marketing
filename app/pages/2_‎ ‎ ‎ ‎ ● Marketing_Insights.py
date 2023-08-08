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


import streamlit as st
import utils_config

st.set_page_config(
    page_title="Marketing Insights", 
    page_icon='/app/images/favicon.png',
    layout='wide'
)

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path='/app/images/menu_icon_2.png'
)

# Set project parameters 
PROJECT_ID = utils_config.get_env_project_id()
LOCATION = utils_config.LOCATION
TEXT_MODEL_NAME = utils_config.TEXT_MODEL_NAME

# State variables for image and text generation
PAGE_KEY_PREFIX = "MarketingPlatforms"
GENERATED_TEXT_KEY = f"{PAGE_KEY_PREFIX}_Generated_Text"
GENERATED_IMAGES_KEY = f"{PAGE_KEY_PREFIX}_Generated_Images"
IMAGE_TO_EDIT_GENERATION_KEY = f"{PAGE_KEY_PREFIX}_Image_to_Edit_Generation"
MASK_IMAGE_GENERATION_KEY = f"{PAGE_KEY_PREFIX}_Mask_Image_Generation"
EDITED_IMAGES_GENERATION_KEY = f"{PAGE_KEY_PREFIX}_Edited_Images_Generation"
IMAGE_GENERATION_TEXT_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Text_Prompt_Images_Generation"
EDIT_GENERATED_IMAGE_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Edit_Text_Prompt_Images_Generation"

# State variables for image editing 
IMAGE_TO_EDIT_KEY = f"{PAGE_KEY_PREFIX}_Image_to_Edit"
EDITED_IMAGES_KEY = f"{PAGE_KEY_PREFIX}_Edited_Images"
MASK_IMAGE_KEY = f"{PAGE_KEY_PREFIX}_Mask_Image"
DASHBOARD_KEY = f"{PAGE_KEY_PREFIX}_Dashboard"
FILE_UPLOADER_KEY = f"{PAGE_KEY_PREFIX}_File_Uploader"
IMAGE_TO_EDIT_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Edit_Prompt_key"
PRE_POPULATED_PROMPTS = [
    'A photo of a handbag on a kitchen counter, natural lighting, 4k',
    'A photo of a handbag on the beach, natural lighting, 4k',
    'Studio photo of a purple handbag, natural lighting, 4k'
]


cols = st.columns([15,70,15])

with cols[1]:
    cols = st.columns([15, 85])
    with cols[0]:
        st.image('/app/images/marketing_analytics_icon.png')
    with cols[1]:
        st.title('Marketing Insights')

    st.write(
        """
        This page presents visualizations of marketing data in the form of Looker Dashboards.
        """
    )

    if utils_config.DASHBOARDS:
        with st.form(key='generate_marketing_dashboard'):
            option = st.selectbox(
                'Select a dashboard to be displayed',
                tuple(utils_config.DASHBOARDS.keys()))

            submit_button = st.form_submit_button(label='Generate Dashboard')

        if submit_button:
            st.session_state[DASHBOARD_KEY] = option
    else:
        st.info('Dashboards not available.')

if DASHBOARD_KEY in st.session_state:
    st.components.v1.iframe(
        src=utils_config.DASHBOARDS.get(st.session_state[DASHBOARD_KEY]), 
        height=800, 
        scrolling=False
    )
else:
    st.components.v1.iframe(
        src=utils_config.DASHBOARDS['Overview'],
        height=800, 
        scrolling=False
    )
