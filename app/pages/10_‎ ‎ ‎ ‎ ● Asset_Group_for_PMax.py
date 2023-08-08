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
import utils_image
import utils_config
from vertexai.preview.language_models import TextGenerationModel
import pandas as pd
import base64

import random
import utils_default_image_text

from utils_campaign import CAMPAIGNS_KEY, generate_names_uuid_dict

st.set_page_config(
    page_title="Asset Group for PMax", 
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
PAGE_KEY_PREFIX = "AssetGroupPmax"
HEADLINE_KEY = f'{PAGE_KEY_PREFIX}_headlines'
LONG_HEADLINE_KEY = f'{PAGE_KEY_PREFIX}_long_headlines'
DESCRIPTION_KEY = f'{PAGE_KEY_PREFIX}_description'
CALL_TO_ACTION_KEY = f'{PAGE_KEY_PREFIX}_call_to_action'
THEMES_FOR_PROMPTS_KEY = f'{PAGE_KEY_PREFIX}_theme'

IMAGE_UPLOAD_CHECKBOX = f"{PAGE_KEY_PREFIX}_Image_Upload_Checkbox"
FILE_UPLOADER_KEY = f"{PAGE_KEY_PREFIX}_File_Uploader"
IMAGE_TO_EDIT_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Edit_Prompt_key"

IMAGE_TO_EDIT_KEY = f"{PAGE_KEY_PREFIX}_Image_To_Edit"
MASK_IMAGE_KEY = f"{PAGE_KEY_PREFIX}_Mask_Image"
EDITED_IMAGES_KEY = f"{PAGE_KEY_PREFIX}_Edited_Images"
IMAGE_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Image_Prompt"

GENERATED_IMAGES_KEY = f'{PAGE_KEY_PREFIX}_generated_images'
# EDIT_GENERATED_IMAGE_PROMPT_KEY = f'{PAGE_KEY_PREFIX}_edit_generated_image_prompt'
# SELECTED_IMAGE_KEY = f'{PAGE_KEY_PREFIX}_selected_image'
# IMAGE_TO_EDIT_KEY = f'{PAGE_KEY_PREFIX}_image_to_edit'
# MASK_IMAGE_KEY = f'{PAGE_KEY_PREFIX}_mask_image'
# EDITED_IMAGES_KEY = f'{PAGE_KEY_PREFIX}_edited_images'

IMAGE_GENERATION_PROMPT = "Generate an image for {theme}"


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
HEADLINE_PROMPT_TEMPLATE = """Using the Cymbal brand information below as your context, create 5 headlines for a campaign with {theme} as objective, under 30 characters each headline.
{cymbal_overview}

Headlines: """

LONG_HEADLINE_PROMPT_TEMPLATE = """Using the Cymbal brand information below as your context, create 5 long headlines (90 characters each) for a campaign with {theme} as objective. Be creative and use all the 90 characters for the long headline.
{cymbal_overview}
Long headlines: """

DESCRIPTION_PROMPT_TEMPLATE = """Using the Cymbal brand information below as your context, create a product description (90 characters) for {theme}. Be creative and use all the 90 characters for the long headline.
{cymbal_overview}
Product description: """

BUSINESS_NAME = 'Cymbal'

CALL_TO_ACTION = [
"Book Now",
"Contact Us",
"Download",
"Learn More",
"Visit Site",
"Shop Now",
"Sign Up",
"Subscribe",
"See More"]

THEMES_FOR_PROMPTS = [
    "sales of new women's handbags at Cymbal",
    "introducing a new line of men's leather shoes",
    "new opening of Cymbal concept shoe store in NYC",
    "Cymbal shoes retail brand in NYC"
]

cols = st.columns([15, 85])
with cols[0]:
    st.image('/app/images/asset_icon.png')
with cols[1]:
    st.title('Asset Group for PMax')

st.write("""Generate an asset group for PMax using Vertex AI PaLM 2 API.""")

is_new_asset = False
with st.form(key='form_theme'):
    select_theme = st.selectbox(
        'Select the scenario to generate an asset group for PMax.',
        options=THEMES_FOR_PROMPTS)
    upload_image = st.checkbox('Upload Image')

    is_button = st.form_submit_button('Generate Asset Group')

if is_button:
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

    is_new_asset = True
    st.session_state[IMAGE_UPLOAD_CHECKBOX] = upload_image

    llm = TextGenerationModel.from_pretrained(TEXT_MODEL_NAME)

    with st.spinner('Generating headlines, long headlines, description and call to action...'):
        try:
            st.session_state[HEADLINE_KEY] = llm.predict(
                HEADLINE_PROMPT_TEMPLATE.format(
                    theme=select_theme,
                    cymbal_overview=CYMBAL_OVERVIEW)
            ).text
        except:
            st.session_state[HEADLINE_KEY] = utils_default_image_text.ASSET_GROUP_HEADLINES
        else:
            if not st.session_state[HEADLINE_KEY]:
                st.session_state[HEADLINE_KEY] = utils_default_image_text.ASSET_GROUP_HEADLINES

        try:
            st.session_state[LONG_HEADLINE_KEY] = llm.predict(
                LONG_HEADLINE_PROMPT_TEMPLATE.format(
                    theme=select_theme,
                    cymbal_overview=CYMBAL_OVERVIEW),
                max_output_tokens=1024
            ).text
        except:
            st.session_state[HEADLINE_KEY] = utils_default_image_text.ASSET_GROUP_LONG_HEADLINES
        else:
            if not st.session_state[HEADLINE_KEY]:
                st.session_state[HEADLINE_KEY] = utils_default_image_text.ASSET_GROUP_LONG_HEADLINES

        try:
            st.session_state[DESCRIPTION_KEY] = llm.predict(
                DESCRIPTION_PROMPT_TEMPLATE.format(
                    theme=select_theme,
                    cymbal_overview=CYMBAL_OVERVIEW),
                max_output_tokens=1024
            ).text
        except:
            st.session_state[HEADLINE_KEY] = utils_default_image_text.ASSET_GROUP_DESCRIPTION
        else:
            if not st.session_state[HEADLINE_KEY]:
                st.session_state[HEADLINE_KEY] = utils_default_image_text.ASSET_GROUP_DESCRIPTION

        st.session_state[CALL_TO_ACTION_KEY] = random.choice(CALL_TO_ACTION)
        st.session_state[THEMES_FOR_PROMPTS_KEY] = select_theme

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

    # ------------------------------------ First generate images
    try:
        if upload_image:
            utils_image.render_image_edit_prompt(
                edited_images_key=GENERATED_IMAGES_KEY,
                edit_image_prompt_key=IMAGE_TO_EDIT_PROMPT_KEY,
                upload_file=True,
                image_to_edit_key=IMAGE_TO_EDIT_KEY,
                mask_image=True,
                mask_image_key=MASK_IMAGE_KEY,
                download_button=False,
                file_uploader_key=FILE_UPLOADER_KEY,
                select_button=False)
        else:
            with st.spinner('Generating images...'):
                utils_image.image_generation(
                    IMAGE_GENERATION_PROMPT.format(theme=st.session_state[THEMES_FOR_PROMPTS_KEY]),
                    8,
                    256,
                    '1:1',
                    GENERATED_IMAGES_KEY)
    except:
        st.session_state[GENERATED_IMAGES_KEY] = []
        if select_theme == THEMES_FOR_PROMPTS[0]:
            with open("/app/images/asset_group_0_0.png", "rb") as fp:
                st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
            with open("/app/images/asset_group_0_1.png", "rb") as fp:
                st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
            
        elif select_theme == THEMES_FOR_PROMPTS[1]:
            with open("/app/images/asset_group_1_0.png", "rb") as fp:
                st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
            with open("/app/images/asset_group_1_1.png", "rb") as fp:
                st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
            
        elif select_theme == THEMES_FOR_PROMPTS[2]:
            with open("/app/images/asset_group_2_0.png", "rb") as fp:
                st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
            with open("/app/images/asset_group_2_1.png", "rb") as fp:
                st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
            
        elif select_theme == THEMES_FOR_PROMPTS[3]:
            with open("/app/images/asset_group_3_0.png", "rb") as fp:
                st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
            with open("/app/images/asset_group_3_1.png", "rb") as fp:
                st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
    else:
        if GENERATED_IMAGES_KEY in st.session_state:
            if not st.session_state[GENERATED_IMAGES_KEY]:
                st.session_state[GENERATED_IMAGES_KEY] = []
                if select_theme == THEMES_FOR_PROMPTS[0]:
                    with open("/app/images/asset_group_0_0.png", "rb") as fp:
                        st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
                    with open("/app/images/asset_group_0_1.png", "rb") as fp:
                        st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
                    
                elif select_theme == THEMES_FOR_PROMPTS[1]:
                    with open("/app/images/asset_group_1_0.png", "rb") as fp:
                        st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
                    with open("/app/images/asset_group_1_1.png", "rb") as fp:
                        st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
                    
                elif select_theme == THEMES_FOR_PROMPTS[2]:
                    with open("/app/images/asset_group_2_0.png", "rb") as fp:
                        st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
                    with open("/app/images/asset_group_2_1.png", "rb") as fp:
                        st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
                    
                elif select_theme == THEMES_FOR_PROMPTS[3]:
                    with open("/app/images/asset_group_3_0.png", "rb") as fp:
                        st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
                    with open("/app/images/asset_group_3_1.png", "rb") as fp:
                        st.session_state[GENERATED_IMAGES_KEY].append({"bytesBase64Encoded":base64.b64encode(fp.read()).decode('utf-8')})
    
    if GENERATED_IMAGES_KEY in st.session_state:
        st.write('**Generated images**')
        utils_image.generate_image_columns(
                GENERATED_IMAGES_KEY, download_button=False)


if THEMES_FOR_PROMPTS_KEY in st.session_state and not is_new_asset:
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

    if st.session_state[IMAGE_UPLOAD_CHECKBOX]:
        try:
            utils_image.render_image_edit_prompt(
                edited_images_key=GENERATED_IMAGES_KEY,
                edit_image_prompt_key=IMAGE_TO_EDIT_PROMPT_KEY,
                upload_file=True,
                image_to_edit_key=IMAGE_TO_EDIT_KEY,
                mask_image=True,
                mask_image_key=MASK_IMAGE_KEY,
                download_button=False,
                file_uploader_key=FILE_UPLOADER_KEY,
                select_button=False)
        except:
            st.info("Could not generate image due to policy restrictions. Please provide a different prompt.")
        else:
            if GENERATED_IMAGES_KEY in st.session_state:
                if not st.session_state[GENERATED_IMAGES_KEY]:
                    st.info("Could not generate image due to policy restrictions. Please provide a different prompt.")
        
        if GENERATED_IMAGES_KEY in st.session_state:
            st.write('**Generated images**')
            utils_image.generate_image_columns(GENERATED_IMAGES_KEY, download_button=False)
    else:
        if GENERATED_IMAGES_KEY in st.session_state:
            st.write('**Generated images**')
            utils_image.generate_image_columns(
                    GENERATED_IMAGES_KEY, download_button=False)


if (HEADLINE_KEY in st.session_state and 
    CAMPAIGNS_KEY in st.session_state and 
    GENERATED_IMAGES_KEY in st.session_state):
    campaigns_names = generate_names_uuid_dict().keys()
    with st.form(PAGE_KEY_PREFIX+"_Link_To_Campaign"):
        st.write("**Choose a Campaign to link the results**")
        selected_name = st.selectbox("List of Campaigns", campaigns_names)
        link_to_campaign_button = st.form_submit_button()

    if link_to_campaign_button:
        selected_uuid = generate_names_uuid_dict()[selected_name]

        assets_group_dict = {}
        assets_group_dict.update({'business_name': BUSINESS_NAME})
        assets_group_dict.update({'scenario':st.session_state[THEMES_FOR_PROMPTS_KEY]})
        assets_group_dict.update({'headline':st.session_state[HEADLINE_KEY]})
        assets_group_dict.update({'long_headline':st.session_state[LONG_HEADLINE_KEY]})
        assets_group_dict.update({'description':st.session_state[DESCRIPTION_KEY]})
        assets_group_dict.update({'call_to_action':st.session_state[CALL_TO_ACTION_KEY]})

        assets_text_pd = pd.DataFrame().from_dict(
            assets_group_dict,
            orient='index',
            columns=['text_assets']
        )

        st.session_state[CAMPAIGNS_KEY][selected_uuid].asset_classes_text = assets_text_pd

        assets_images_pd = pd.DataFrame()
        for i, value in enumerate(st.session_state[GENERATED_IMAGES_KEY]):
            assets_images_pd.insert(
                i,
                column=f'image_{i}',
                value=["data:image/png;base64,"+value["bytesBase64Encoded"]])

        st.session_state[CAMPAIGNS_KEY][selected_uuid].asset_classes_images = assets_images_pd
        st.success(f"Asset group linked to campaign {selected_name}")

if (HEADLINE_KEY in st.session_state and 
    CAMPAIGNS_KEY in st.session_state and 
    FILE_UPLOADER_KEY in st.session_state and
    IMAGE_TO_EDIT_KEY in st.session_state and
    GENERATED_IMAGES_KEY not in st.session_state):
    campaigns_names = generate_names_uuid_dict().keys()
    with st.form(PAGE_KEY_PREFIX+"_Link_To_Campaign"):
        st.write("**Choose a Campaign to link the results**")
        selected_name = st.selectbox("List of Campaigns", campaigns_names)
        link_to_campaign_button = st.form_submit_button()

    if link_to_campaign_button:
        selected_uuid = generate_names_uuid_dict()[selected_name]

        assets_group_dict = {}
        assets_group_dict.update({'business_name': BUSINESS_NAME})
        assets_group_dict.update({'scenario':st.session_state[THEMES_FOR_PROMPTS_KEY]})
        assets_group_dict.update({'headline':st.session_state[HEADLINE_KEY]})
        assets_group_dict.update({'long_headline':st.session_state[LONG_HEADLINE_KEY]})
        assets_group_dict.update({'description':st.session_state[DESCRIPTION_KEY]})
        assets_group_dict.update({'call_to_action':st.session_state[CALL_TO_ACTION_KEY]})

        assets_text_pd = pd.DataFrame().from_dict(
            assets_group_dict,
            orient='index',
            columns=['text_assets']
        )

        st.session_state[CAMPAIGNS_KEY][selected_uuid].asset_classes_text = assets_text_pd

        assets_images_pd = pd.DataFrame()
        assets_images_pd.insert(
            0, 
            column='image_0', 
            value=["data:image/png;base64,"+base64.b64encode(st.session_state[IMAGE_TO_EDIT_KEY]).decode('utf-8')])

        st.session_state[CAMPAIGNS_KEY][selected_uuid].asset_classes_images = assets_images_pd
        st.success(f"Asset group linked to campaign {selected_name}")
