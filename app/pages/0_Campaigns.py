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

import streamlit as st
from utils_campaign import CAMPAIGNS_KEY, add_new_campaign

import utils_config
from vertexai.preview.language_models import TextGenerationModel
from utils_campaign import CAMPAIGNS_KEY


st.set_page_config(
    page_title="Campaigns",
    page_icon='/app/images/favicon.png'
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
IMAGE_MODEL_NAME = utils_config.IMAGE_MODEL_NAME

# State variables for image and text generation
PAGE_KEY_PREFIX = "CreativeBrief"
BRAND_STATEMENT_KEY = f'{PAGE_KEY_PREFIX}_brand_statement'
PRIMARY_MSG_KEY = f'{PAGE_KEY_PREFIX}_primary_msg'
COMMS_CHANNEL_KEY = f'{PAGE_KEY_PREFIX}_comms_channels'
THEMES_FOR_PROMPTS_KEY = f'{PAGE_KEY_PREFIX}_theme'

CYMBAL_OVERVIEW = """Cymbal brand information:
1. Brand Name:Cymbal
2. Vision: Elevate every step and statement with our curated ensemble of footwear and handbags.
3. Mission: To seamlessly blend comfort and style, Cymbal aims to provide a harmonious collection of shoes and handbags, resonating with modern elegance and timeless charm.
4. Products: 
Shoes: From the bustling city streets to quiet evening outings, our shoes are tailored to fit every scenario with unmatched style and comfort.
Handbags: Crafted for the modern individual, our range spans from spacious totes for daily grind to chic clutches for those nights to remember.
5. Unique Selling Proposition (USP): A symphony of style. At Cymbal, we believe in orchestrating the perfect balance between trendsetting designs and unparalleled quality.
6. Target Audience: Style-savvy individuals aged 20-50 who have an ear for quality and an eye for timeless elegance, seeking the perfect accessories to accompany their ever-evolving lifestyles.
7. Brand Personality: Harmonious, chic, and captivating. Cymbal echoes the rhythm of contemporary fashion with a hint of classic allure.
8. Core Values: Quality First: Every product at Cymbal resonates with a promise of durability and excellence.
Listening to the Beat: We constantly tune into our customer's needs and desires, shaping our collections to mirror the world's evolving fashion pulse.
Echoing Sustainability: Cymbal strikes a chord with the environment, ensuring eco-friendly practices and sustainable choices are at the forefront.
9. Brand Tagline: "Echo Your Elegance."
10. Competitive Landscape: The fashion industry reverberates with many brands, but Cymbal stands distinct with its commitment to harmonizing quality, trend, and sustainability.
11. Future Outlook: Cymbal aspires to expand its resonance in the global market, infusing more sustainable materials into its products, and initiating special editions through designer partnerships, creating exclusive, melodious collections.
Cymbal is not just a brand; it's an experience. Recognizing the rhythm of life and the melodies of fashion, we ensure every piece adds a note of sophistication to our customer's ensemble. Every choice at Cymbal is a step toward a more stylish tomorrow.
"""


# Prompt templates
BRAND_STATEMENT_PROMPT_TEMPLATE = """Using the Cymbal brand information below as your context, create a brand statement for a campaign targeting {gender_theme} at age range {age_theme} with {objective_theme} as objective.
{cymbal_overview}

Brand statement: """

PRIMARY_MSG_PROMPT_TEMPLATE = """You are working to create a creative brief for Cymbal brand, a document that outlines the creative approach and deliverables for a new project, such as a marketing or advertising campaign. 
It's a short document that summarizes the project's mission, goals, challenges, demographics, messaging, and other key details. 
Generate a creative brief for Cymbal's brand for a campaign targeting {gender_theme} at age range {age_theme} with {objective_theme} as objective and {competitor_theme} as main competitor.
The creative brief must include the primary message, mission, goals, challenges, demographics and any other relevant details for a clear and concise creative brief. Use the context below to extract any information that you need. 
{cymbal_overview}

Creative brief: """

COMMS_CHANNEL_PROMPT_TEMPLATE = """I want you to act as a marketing specialist who knows how to create awesome marketing assets. Suggest the best marketing channels for an ads campaign for a new women clothing line."""

BUSINESS_NAME = 'Cymbal'

GENDER_FOR_PROMPTS =[
    'Women',
    'Men'
]

AGEGROUP_FOR_PROMPTS =[
    '20-30',
    '30-40',
    '40-50'
]

OBJECTIVES_FOR_PROMPTS = [
    'Drive Awareness',
    'Increasing Traffic',
    'Increasing Engagement',
    'Increasing Sales'
]

COMPETITORS_FOR_PROMPTS = [
    'Fashion Forward',
    'Style Setter',
    'Wardrobe Wonder'
]

cols = st.columns([13, 87])
with cols[0]:
    st.image('/app/images/logo.png')
with cols[1]:
    st.title('Generative AI for Marketing')

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

if create_campaign_button:
    llm = TextGenerationModel.from_pretrained(TEXT_MODEL_NAME)
    generated_uuid = None
    is_allowed_to_create_campaign = False

    if CAMPAIGNS_KEY in st.session_state and st.session_state[CAMPAIGNS_KEY].keys():
        campaigns = st.session_state[CAMPAIGNS_KEY].values()
        campaign_names = {campaign.name : str(campaign.unique_uuid) for campaign in campaigns}

        if campaign_name in campaign_names:
            st.info(f"Campaign with name '{campaign_name}' already created. Provide a unique name.")
        else:
            is_allowed_to_create_campaign = True
    else:
        is_allowed_to_create_campaign = True

    if is_allowed_to_create_campaign:
        with st.spinner('Generating creative brief ...'):
            try:
                st.session_state[BRAND_STATEMENT_KEY] = llm.predict(
                    BRAND_STATEMENT_PROMPT_TEMPLATE.format(
                        gender_theme=gender_select_theme, 
                        age_theme=age_select_theme,
                        objective_theme=objective_select_theme,
                        competitor_theme=competitor_select_theme,
                        cymbal_overview=CYMBAL_OVERVIEW),
                        max_output_tokens=1024
                ).text

                st.session_state[PRIMARY_MSG_KEY] = llm.predict(
                    PRIMARY_MSG_PROMPT_TEMPLATE.format(
                        gender_theme=gender_select_theme, 
                        age_theme=age_select_theme,
                        objective_theme=objective_select_theme,
                        competitor_theme=competitor_select_theme,
                        cymbal_overview=CYMBAL_OVERVIEW),
                        max_output_tokens=1024
                ).text

                st.session_state[COMMS_CHANNEL_KEY] = llm.predict(
                    COMMS_CHANNEL_PROMPT_TEMPLATE.format(
                        gender_theme=gender_select_theme, 
                        age_theme=age_select_theme,
                        objective_theme=objective_select_theme,
                        competitor_theme=competitor_select_theme),
                        max_output_tokens=1024
                ).text

                st.session_state[THEMES_FOR_PROMPTS_KEY] = f'Targeting gender: {gender_select_theme}, Age group: {age_select_theme}, Campaign objective: {objective_select_theme}, Competitor: {competitor_select_theme}'
            except:
                st.info('Something went wrong with your prompt. Try again.')
            else:
                generated_uuid = add_new_campaign(campaign_name)
                # Store generated assets
                st.session_state[CAMPAIGNS_KEY][generated_uuid].brief = {'business_name': BUSINESS_NAME}
                st.session_state[CAMPAIGNS_KEY][generated_uuid].brief.update({'campaign_name': campaign_name})
                st.session_state[CAMPAIGNS_KEY][generated_uuid].brief.update({'brief_scenario': st.session_state[THEMES_FOR_PROMPTS_KEY]})
                st.session_state[CAMPAIGNS_KEY][generated_uuid].brief.update({'brand_statement': st.session_state[BRAND_STATEMENT_KEY]})
                st.session_state[CAMPAIGNS_KEY][generated_uuid].brief.update({'primary_message': st.session_state[PRIMARY_MSG_KEY]})
                st.session_state[CAMPAIGNS_KEY][generated_uuid].brief.update({'comm_channels': st.session_state[COMMS_CHANNEL_KEY]})


if CAMPAIGNS_KEY not in st.session_state: # and st.session_state[CAMPAIGNS_KEY].keys():
    st.info('No campaigns created yet, start by creating one.')

elif CAMPAIGNS_KEY in st.session_state and st.session_state[CAMPAIGNS_KEY].keys():
    campaigns = st.session_state[CAMPAIGNS_KEY].values()
    campaign_names = {campaign.name : str(campaign.unique_uuid) for campaign in campaigns}

    if not create_campaign_button:
        campaigns_list_menu = list(campaign_names.keys())
    else:
        campaigns_list_menu = list(campaign_names.keys())
        idx = campaigns_list_menu.index(campaign_name)
        campaigns_list_menu.insert(0, campaigns_list_menu[idx])
        campaigns_list_menu.pop(idx+1)
    
    with st.form('list_brief_campaigns'):
        st.write("**Active Campaigns**")
        campaign_list_name = st.selectbox('Select a campaign to display its brief', campaigns_list_menu)
        retrieve_brief_button = st.form_submit_button('Retrieve Brief')

    if retrieve_brief_button:
        campaign_uuid = campaign_names[campaign_list_name]
        st.subheader(f'Creative Brief for campaign: {st.session_state[CAMPAIGNS_KEY][campaign_uuid].brief["campaign_name"]}')
        col1, col2 = st.columns([28,72])
        with col1:
            st.write('**Business name:**')
        with col2:
            st.write(st.session_state[CAMPAIGNS_KEY][campaign_uuid].brief['business_name'])
        col3, col4 = st.columns([28,72])
        with col3:
            st.write('**Scenario:**')
        with col4:
            st.write(st.session_state[CAMPAIGNS_KEY][campaign_uuid].brief['brief_scenario'])

        col5, col6 = st.columns([28,72])
        with col5:
            st.write('**Brand Statement:**')
        with col6:
            st.write(st.session_state[CAMPAIGNS_KEY][campaign_uuid].brief['brand_statement'])
        
        col7, col8 = st.columns([28,72])
        with col7:
            st.write('**Brand Strategy:**')
        with col8:
            st.write(st.session_state[CAMPAIGNS_KEY][campaign_uuid].brief['primary_message'])
        
        col9, col10 = st.columns([28,72])
        with col9:
            st.write('**Communication Channels:**')
        with col10:
            st.write(st.session_state[CAMPAIGNS_KEY][campaign_uuid].brief['comm_channels'])

if create_campaign_button:
    if generated_uuid:
        st.success(f"Campaign '{campaign_name}' generated with the uuid '{generated_uuid}'")
        # Render the generated brief
        st.subheader(f'Creative Brief for campaign: {campaign_name}')
        col1, col2 = st.columns([28,72])
        with col1:
            st.write('**Business name:**')
        with col2:
            st.write(BUSINESS_NAME)
        col3, col4 = st.columns([28,72])
        with col3:
            st.write('**Scenario:**')
        with col4:
            st.write(st.session_state[THEMES_FOR_PROMPTS_KEY])

        col5, col6 = st.columns([28,72])
        with col5:
            st.write('**Brand Statement:**')
        with col6:
            st.write(f'{st.session_state[BRAND_STATEMENT_KEY]}')
        
        col7, col8 = st.columns([28,72])
        with col7:
            st.write('**Brand Strategy:**')
        with col8:
            st.write(f'{st.session_state[PRIMARY_MSG_KEY]}')
        
        col9, col10 = st.columns([28,72])
        with col9:
            st.write('**Communication Channels:**')
        with col10:
            st.write(f'{st.session_state[COMMS_CHANNEL_KEY]}')
