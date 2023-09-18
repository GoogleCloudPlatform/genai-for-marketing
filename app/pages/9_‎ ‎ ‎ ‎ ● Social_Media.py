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
Social Media Ads
"""

import base64
import streamlit as st
import tomllib
import vertexai
import utils_image

from vertexai.preview.language_models import TextGenerationModel
from utils_campaign import generate_names_uuid_dict
from utils_image import render_image_generation_and_edition_ui
from utils_streamlit import reset_page_state


# Load configuration file
with open("./app_config.toml", "rb") as f:
    data = tomllib.load(f)

PROJECT_ID = data["global"]["project_id"]
LOCATION = data["global"]["location"]
TEXT_MODEL_NAME = data["models"]["text"]["text_model_name"]
CAMPAIGNS_KEY = data["pages"]["campaigns"]["campaigns_key"]


PAGE_KEY_PREFIX = "Social_Media_Ads"
TWITTER_PREFIX = f"{PAGE_KEY_PREFIX}_Twitter"
INSTAGRAM_PREFIX = f"{PAGE_KEY_PREFIX}_Instagram"
THREADS_PREFIX = f"{PAGE_KEY_PREFIX}_Threads"

INSTAGRAM_GENDER_OPTIONS = data["pages"]["9_social_media"]["instagram_gender_options"]
INSTAGRAM_CHAR_LIMIT = data["pages"]["9_social_media"]["instagram_char_limit"]

THREADS_CHAR_LIMIT = data["pages"]["9_social_media"]["threads_char_limit"]

AD_PROMPT_TEMPLATE = data["pages"]["9_social_media"]["ad_prompt_template"]
IMAGE_PROMPT_TEMPLATE = data["pages"]["9_social_media"]["image_prompt_template"]
THEMES_FOR_PROMPTS = data["pages"]["9_social_media"]["themes_for_prompts"]

st.set_page_config(
    page_title=data["pages"]["9_social_media"]["page_title"],
    page_icon=data["pages"]["9_social_media"]["page_icon"]
)

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path=data["pages"]["9_social_media"]["sidebar_image_path"]
)

cols = st.columns([17, 83])
with cols[0]:
    st.image(data["pages"]["9_social_media"]["page_title_image"])
with cols[1]:
    st.title(data["pages"]["9_social_media"]["page_title"])

def generate_ad(
        theme, 
        platform, 
        age_range, 
        gender, 
        has_image, 
        limit, 
        key_prefix, 
        generate_image_option):

    st.session_state[key_prefix+'_Has_Image_Flag'] = has_image
    st.session_state[key_prefix+'_Image_Generate_Option'] = generate_image_option

    try:
        # Initialize variables
        with st.spinner(f'Generating {platform} text ...'):
            vertexai.init(project=PROJECT_ID, location=LOCATION)
            llm = TextGenerationModel.from_pretrained(TEXT_MODEL_NAME)
            response = llm.predict(
                    prompt=AD_PROMPT_TEMPLATE.format(
                        platform,
                        limit,
                        age_range, 
                        gender,
                        theme),
                    temperature=0.2,
                    max_output_tokens=limit//4, # 4 chars per token
                    top_k = 40,
                    top_p = 0.8
                ).text
    except:
        if platform == 'Threads':
            if theme == THEMES_FOR_PROMPTS[0]:
                st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_threads_0"]
            elif theme == THEMES_FOR_PROMPTS[1]:
                st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_threads_1"]
            elif theme == THEMES_FOR_PROMPTS[2]:
                st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_threads_2"]
            elif theme == THEMES_FOR_PROMPTS[3]:
                st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_threads_3"]
        elif platform == "Instagram":
            if theme == THEMES_FOR_PROMPTS[0]:
                st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_instagram_0"]
            elif theme == THEMES_FOR_PROMPTS[1]:
                st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_instagram_1"]
            elif theme == THEMES_FOR_PROMPTS[2]:
                st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_instagram_2"]
            elif theme == THEMES_FOR_PROMPTS[3]:
                st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_instagram_3"]
    else:
        st.session_state[key_prefix+"_Text"] = response
        if not response:
            if platform == 'Threads':
                if theme == THEMES_FOR_PROMPTS[0]:
                    st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_threads_0"]
                elif theme == THEMES_FOR_PROMPTS[1]:
                    st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_threads_1"]
                elif theme == THEMES_FOR_PROMPTS[2]:
                    st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_threads_2"]
                elif theme == THEMES_FOR_PROMPTS[3]:
                    st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_threads_3"]
            elif platform == "Instagram":
                if theme == THEMES_FOR_PROMPTS[0]:
                    st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_instagram_0"]
                elif theme == THEMES_FOR_PROMPTS[1]:
                    st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_instagram_1"]
                elif theme == THEMES_FOR_PROMPTS[2]:
                    st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_instagram_2"]
                elif theme == THEMES_FOR_PROMPTS[3]:
                    st.session_state[key_prefix+"_Text"] = data["pages"]["9_social_media"]["social_instagram_3"]
    
    if st.session_state[key_prefix+'_Has_Image_Flag'] and key_prefix+"_Text" in st.session_state:
        prompt_image = IMAGE_PROMPT_TEMPLATE.format(theme)
        st.session_state[key_prefix+"_Generated_Image_Prompt"] = prompt_image


def render_ad(
        key_prefix, 
        platform, 
        theme, 
        gender, 
        age_range):

    if key_prefix+"_Text" in st.session_state:
        st.write('**Generated Post**')
        st.write(st.session_state[key_prefix+"_Text"])

    if st.session_state[key_prefix+'_Has_Image_Flag'] and key_prefix+"_Generated_Image_Prompt" in st.session_state:
        try:
            if st.session_state[key_prefix+'_Image_Generate_Option'] == 'Generate Images':
                render_image_generation_and_edition_ui(
                    image_text_prompt_key=key_prefix+"_Image_Prompt",
                    generated_images_key=key_prefix+"_Generated_Images",
                    edit_image_prompt_key=key_prefix+"_Edit_Image_Prompt",
                    pre_populated_prompts=[st.session_state[key_prefix+"_Generated_Image_Prompt"]],
                    select_button=True,
                    selected_image_key=key_prefix+"_Selected_Image",
                    edit_button=True,
                    title=f"Generate {platform} ad image",
                    image_to_edit_key=key_prefix+"_Image_To_Edit",
                    edit_with_mask=True,
                    mask_image_key=key_prefix+"_Image_Mask",
                    edited_images_key=key_prefix+"_Edited_Images",
                    download_button=False,
                    auto_submit_first_pre_populated=True
                )
            else:
                utils_image.render_image_edit_prompt(
                    edited_images_key=key_prefix+"_Generated_Images",
                    edit_image_prompt_key=key_prefix+"_Image_Prompt",
                    upload_file=True,
                    image_to_edit_key=key_prefix+"_Image_To_Edit",
                    mask_image=True,
                    mask_image_key=key_prefix+"_Image_Mask",
                    download_button=False,
                    file_uploader_key=key_prefix+"_File_Uploader",
                    select_button=True,
                    selected_image_key=key_prefix+"_Selected_Image")
        except:
            if key_prefix+'_Image_Generate_Option' in st.session_state:
                st.info("Could not generate image due to policy restrictions. Please provide a different prompt.")
            else:
                if platform == "Instagram":
                    if theme == THEMES_FOR_PROMPTS[0]:
                        utils_image.get_default_image_bytesio(
                            data["pages"]["9_social_media"]["default_image_instagram_0"], key_prefix+"_Selected_Image")
                    elif theme == THEMES_FOR_PROMPTS[1]:
                        utils_image.get_default_image_bytesio(
                            data["pages"]["9_social_media"]["default_image_instagram_1"], key_prefix+"_Selected_Image")
                    elif theme == THEMES_FOR_PROMPTS[2]:
                        utils_image.get_default_image_bytesio(
                            data["pages"]["9_social_media"]["default_image_instagram_2"], key_prefix+"_Selected_Image")
                    elif theme == THEMES_FOR_PROMPTS[3]:
                        utils_image.get_default_image_bytesio(
                            data["pages"]["9_social_media"]["default_image_instagram_3"], key_prefix+"_Selected_Image")
                else:
                    if theme == THEMES_FOR_PROMPTS[0]:
                        utils_image.get_default_image_bytesio(
                            data["pages"]["9_social_media"]["default_image_threads_0"], key_prefix+"_Selected_Image")
                    elif theme == THEMES_FOR_PROMPTS[1]:
                        utils_image.get_default_image_bytesio(
                            data["pages"]["9_social_media"]["default_image_threads_1"], key_prefix+"_Selected_Image")
                    elif theme == THEMES_FOR_PROMPTS[2]:
                        utils_image.get_default_image_bytesio(
                            data["pages"]["9_social_media"]["default_image_threads_2"], key_prefix+"_Selected_Image")
                    elif theme == THEMES_FOR_PROMPTS[3]:
                        utils_image.get_default_image_bytesio(
                            data["pages"]["9_social_media"]["default_image_threads_3"], key_prefix+"_Selected_Image")
        else:
            if key_prefix+"_Generated_Images" in st.session_state:
                if not st.session_state[key_prefix+"_Generated_Images"]:
                    if key_prefix+'_Image_Generate_Option' in st.session_state:
                        st.info("Could not generate image due to policy restrictions. Please provide a different prompt.")
                    else:
                        if platform == "Instagram":
                            if theme == THEMES_FOR_PROMPTS[0]:
                                utils_image.get_default_image_bytesio(
                                    data["pages"]["9_social_media"]["default_image_instagram_0"], key_prefix+"_Selected_Image")
                            elif theme == THEMES_FOR_PROMPTS[1]:
                                utils_image.get_default_image_bytesio(
                                    data["pages"]["9_social_media"]["default_image_instagram_1"], key_prefix+"_Selected_Image")
                            elif theme == THEMES_FOR_PROMPTS[2]:
                                utils_image.get_default_image_bytesio(
                                    data["pages"]["9_social_media"]["default_image_instagram_2"], key_prefix+"_Selected_Image")
                            elif theme == THEMES_FOR_PROMPTS[3]:
                                utils_image.get_default_image_bytesio(
                                    data["pages"]["9_social_media"]["default_image_instagram_3"], key_prefix+"_Selected_Image")
                        else:
                            if theme == THEMES_FOR_PROMPTS[0]:
                                utils_image.get_default_image_bytesio(
                                    data["pages"]["9_social_media"]["default_image_threads_0"], key_prefix+"_Selected_Image")
                            elif theme == THEMES_FOR_PROMPTS[1]:
                                utils_image.get_default_image_bytesio(
                                    data["pages"]["9_social_media"]["default_image_threads_1"], key_prefix+"_Selected_Image")
                            elif theme == THEMES_FOR_PROMPTS[2]:
                                utils_image.get_default_image_bytesio(
                                    data["pages"]["9_social_media"]["default_image_threads_2"], key_prefix+"_Selected_Image")
                            elif theme == THEMES_FOR_PROMPTS[3]:
                                utils_image.get_default_image_bytesio(
                                    data["pages"]["9_social_media"]["default_image_threads_3"], key_prefix+"_Selected_Image")

    if key_prefix+"_Selected_Image" in st.session_state:
        st.image(st.session_state[key_prefix+"_Selected_Image"])

    # Attach to campaign when generate images
    if (key_prefix+"_Text" in st.session_state and 
        CAMPAIGNS_KEY in st.session_state and
        key_prefix+"_Selected_Image" in st.session_state):
        
        campaigns_names = generate_names_uuid_dict().keys() 
        with st.form(key_prefix+"_Link_To_Campaign"):
            st.write("**Choose a Campaign to link the results**")
            selected_name = st.selectbox("List of Campaigns", campaigns_names)
            link_to_campaign_button = st.form_submit_button()
        
        image = base64.b64encode(st.session_state[key_prefix+"_Selected_Image"].getvalue()).decode("utf-8")
        ad = {
            "theme": theme,
            "gender": gender,
            "age_range": age_range,
            "text": st.session_state[key_prefix+"_Text"],
            "image": "data:image/png;base64,"+image}
        
        if link_to_campaign_button:
            selected_uuid = generate_names_uuid_dict()[selected_name]
            if platform == "Threads":
                st.session_state[CAMPAIGNS_KEY][selected_uuid].ads_threads = ad
            elif platform == "Instagram":
                st.session_state[CAMPAIGNS_KEY][selected_uuid].ads_insta = ad
            st.success(f"Ad linked to campaign {selected_name}")

    # Attach to campaign when upload
    if (key_prefix+"_Text" in st.session_state and 
        key_prefix+"_Image_To_Edit" in st.session_state and 
        key_prefix+"_File_Uploader" in st.session_state and
        key_prefix+"_Selected_Image" not in st.session_state and
        CAMPAIGNS_KEY in st.session_state):
        
        campaigns_names = generate_names_uuid_dict().keys() 
        with st.form(key_prefix+"_Link_To_Campaign"):
            st.write("**Choose a Campaign to link the results**")
            selected_name = st.selectbox("List of Campaigns", campaigns_names)
            link_to_campaign_button = st.form_submit_button()
        
        image = base64.b64encode(st.session_state[key_prefix+"_Image_To_Edit"]).decode("utf-8")
        ad = {
            "theme": theme,
            "gender": gender,
            "age_range": age_range,
            "text": st.session_state[key_prefix+"_Text"],
            "image": "data:image/png;base64,"+image}
        
        if link_to_campaign_button:
            selected_uuid = generate_names_uuid_dict()[selected_name]
            if platform == "Threads":
                st.session_state[CAMPAIGNS_KEY][selected_uuid].ads_threads = ad
            elif platform == "Instagram":
                st.session_state[CAMPAIGNS_KEY][selected_uuid].ads_insta = ad
            st.success(f"Ad linked to campaign {selected_name}")


    # Link to campaign with NO images
    if (st.session_state[key_prefix+'_Has_Image_Flag'] == False and
        key_prefix+"_Text" in st.session_state and 
        CAMPAIGNS_KEY in st.session_state):
        
        campaigns_names = generate_names_uuid_dict().keys() 
        with st.form(key_prefix+"_Link_To_Campaign"):
            st.write("**Choose a Campaign to link the results**")
            selected_name = st.selectbox("List of Campaigns", campaigns_names)
            link_to_campaign_button = st.form_submit_button()
    
        ad = {
            "theme": theme,
            "gender": gender,
            "age_range": age_range,
            "text": st.session_state[key_prefix+"_Text"]}
        
        if link_to_campaign_button:
            selected_uuid = generate_names_uuid_dict()[selected_name]
            if platform == "Threads":
                st.session_state[CAMPAIGNS_KEY][selected_uuid].ads_threads = ad
            elif platform == "Instagram":
                st.session_state[CAMPAIGNS_KEY][selected_uuid].ads_insta = ad
            st.success(f"Ad linked to campaign {selected_name}")


threads_tab, instagram_tab = st.tabs(["Threads", "Instagram"])
is_new_generation = False
with threads_tab:
    with st.form("Generate Threads Ads"):
        i_col1, i_col2 =st.columns([1,1])
        with i_col1:
            threads_gender = st.selectbox('Gender', INSTAGRAM_GENDER_OPTIONS)
        with i_col2:
            threads_age = st.slider(
                'Age Segment', 21, 65, (21,30))
        
        col1, col2 = st.columns([1,1])
        with col1:
            threads_image = st.checkbox("Include Images", value=True)
        with col2:
            threads_65_plus = st.checkbox("Older than 65", value=False)
        generate_image_option = st.radio(
                    label='Select one of the options for image generation',
                    options=['Generate Images', 'Upload Image'])

        threads_theme = st.selectbox('Theme', THEMES_FOR_PROMPTS)
        threads_generation_button = st.form_submit_button()
    
    if threads_generation_button:
        reset_page_state(THREADS_PREFIX)
        is_new_generation = True

        age_range = f"{threads_age[0]}-{threads_age[1]}"
        if threads_age == 65 and threads_65_plus:
            age_range += "+"

        generate_ad(
            theme=threads_theme,
            platform="Threads",
            gender=threads_gender,
            age_range=age_range,
            has_image=threads_image,
            limit=THREADS_CHAR_LIMIT,
            key_prefix=THREADS_PREFIX,
            generate_image_option=generate_image_option)
    
    if THREADS_PREFIX+'_Has_Image_Flag' not in st.session_state:
        st.session_state[THREADS_PREFIX+'_Has_Image_Flag'] = False

    age_range = f"{threads_age[0]}-{threads_age[1]}"
    render_ad(
        THREADS_PREFIX, 
        platform="Threads",
        theme=threads_theme,
        gender=threads_gender,
        age_range=age_range)


with instagram_tab:
    with st.form("Generate Instagram Ads"):
        i_col1, i_col2 =st.columns([1,1])
        with i_col1:
            instagram_gender = st.selectbox('Gender', INSTAGRAM_GENDER_OPTIONS)
        with i_col2:
            instagram_age = st.slider(
                'Age Segment', 21, 65, (21,30))
        
        col1, col2 = st.columns([1,1])
        with col1:
            instagram_image = st.checkbox("Include Images", value=True)
        with col2:
            instagram_65_plus = st.checkbox("Older than 65", value=False)
        generate_image_option = st.radio(
                    label='Select one of the options for image generation',
                    options=['Generate Images', 'Upload Image'])

        instagram_theme = st.selectbox('Theme', THEMES_FOR_PROMPTS)
        instagram_generation_button = st.form_submit_button()
    
    if instagram_generation_button:
        reset_page_state(INSTAGRAM_PREFIX)

        age_range = f"{instagram_age[0]}-{instagram_age[1]}"
        if instagram_age == 65 and instagram_65_plus:
            age_range += "+"

        generate_ad(
            theme=instagram_theme,
            platform="Instagram",
            gender=instagram_gender,
            age_range=age_range,
            has_image=instagram_image,
            limit=INSTAGRAM_CHAR_LIMIT,
            key_prefix=INSTAGRAM_PREFIX,
            generate_image_option=generate_image_option)
    
    if INSTAGRAM_PREFIX+'_Has_Image_Flag' not in st.session_state:
        st.session_state[INSTAGRAM_PREFIX+'_Has_Image_Flag'] = False

    age_range = f"{instagram_age[0]}-{instagram_age[1]}"
    
    render_ad(
        INSTAGRAM_PREFIX, 
        platform="Instagram",
        theme=instagram_theme,
        gender=instagram_gender,
        age_range=age_range
    )
