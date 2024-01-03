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
Website post generation: 
- Automatically create website posts on a wide range of topics 
  and in a variety of styles. 
- These articles include text and visuals
"""

import base64
import streamlit as st
import utils_image
import vertexai

from vertexai.preview.language_models import TextGenerationModel
from utils_config import GLOBAL_CFG, MODEL_CFG, PAGES_CFG
from utils_campaign import generate_names_uuid_dict
from utils_streamlit import reset_page_state


page_cfg = PAGES_CFG["8_website_post"]
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
TEXT_MODEL_NAME = MODEL_CFG["text"]["text_model_name"]
CAMPAIGNS_KEY = PAGES_CFG["campaigns"]["campaigns_key"]

# State variables for Website post generation (text and image)
PAGE_KEY_PREFIX = "WebsitePost"
GENERATED_TEXT_KEY = f"{PAGE_KEY_PREFIX}_Generated_Text"
GENERATED_IMAGES_KEY = f"{PAGE_KEY_PREFIX}_Generated_Image"
SELECTED_IMAGE_KEY = f"{PAGE_KEY_PREFIX}_Selected_Image"
IMAGE_TO_EDIT_KEY = f"{PAGE_KEY_PREFIX}_Image_To_Edit"
MASK_IMAGE_KEY = f"{PAGE_KEY_PREFIX}_Mask_Image"
EDITED_IMAGES_KEY = f"{PAGE_KEY_PREFIX}_Edited_Images"
IMAGE_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Image_Prompt"

IMAGE_OPTION = f"{PAGE_KEY_PREFIX}_Image_Upload_Checkbox"
FILE_UPLOADER_KEY = f"{PAGE_KEY_PREFIX}_File_Uploader"
EDIT_IMAGE_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Edit_Prompt_key"
IMAGE_OPTION_KEY = f"{PAGE_KEY_PREFIX}_Image_Option"

SELECTED_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Selected_Prompt"

UUID_KEY = f"{PAGE_KEY_PREFIX}_UUID"
# State variables for image generation
IMAGE_GENERATION_TEXT_PROMPT_KEY = (
        f"{PAGE_KEY_PREFIX}_Text_Prompt_Images_Generation")
EDIT_GENERATED_IMAGE_PROMPT_KEY = (
        f"{PAGE_KEY_PREFIX}_Edit_Text_Prompt_Images_Generation")
DEFAULT_IMAGE_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Image_Prompt"

# Templates
WEBSITE_PROMPT_TEMPLATE = page_cfg["prompt_website_template"]
IMAGE_PROMPT_TAMPLATE = page_cfg["prompt_image_template"]
THEMES_FOR_PROMPTS = PAGES_CFG["campaigns"]["prompt_themes"]


cols = st.columns([15, 85])
with cols[0]:
    st.image(page_cfg["page_title_image"])
with cols[1]:
    st.title(page_cfg["page_title"])

st.write(
    "This page provides a step-by-step guide to generating a website post.")

st.subheader('Post Generation')

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

    st.subheader(f"Website Post for campaign '{campaign_name}'")
    theme = st.session_state[CAMPAIGNS_KEY][selected_uuid].theme
    theme_expander_title = "Choose the theme for the email"
    theme_expanded = True
    if SELECTED_PROMPT_KEY in st.session_state:
        theme_expander_title = "Change the theme"
        theme_expanded = False
    with st.expander(theme_expander_title, theme_expanded):
        campaign_option = st.radio(
            "**Choose the theme to generate the website post**",
            [f"Campaign: '{theme}'", "Custom"],
            label_visibility="collapsed")
        if campaign_option == "Custom":
            other_option = st.text_input("Enter your custom theme...")
        else:
            other_option = ""
                        
        generate_button = st.button("Generate")
    
    if generate_button:
        if campaign_option != "Custom":
            st.session_state[SELECTED_PROMPT_KEY] = theme
        else:
            if other_option == "":
                st.info("Please write the custom theme")
                st.stop()
            st.session_state[SELECTED_PROMPT_KEY] = other_option

        selected_prompt = st.session_state[SELECTED_PROMPT_KEY]
        # Initialize variables
        if GENERATED_TEXT_KEY in st.session_state:
            del st.session_state[GENERATED_TEXT_KEY]
        if SELECTED_IMAGE_KEY in st.session_state:
            del st.session_state[SELECTED_IMAGE_KEY]
        if GENERATED_IMAGES_KEY in st.session_state:
            del st.session_state[GENERATED_IMAGES_KEY]
        if EDITED_IMAGES_KEY in st.session_state:
            del st.session_state[EDITED_IMAGES_KEY]
        if IMAGE_TO_EDIT_KEY in st.session_state:
            del st.session_state[IMAGE_TO_EDIT_KEY]
        if FILE_UPLOADER_KEY in st.session_state:
            del st.session_state[FILE_UPLOADER_KEY]
        if IMAGE_OPTION_KEY in st.session_state:
            del st.session_state[IMAGE_OPTION_KEY]

        with st.spinner('Generating website post ...'):
            try:
                vertexai.init(project=PROJECT_ID, location=LOCATION)
                llm = TextGenerationModel.from_pretrained(TEXT_MODEL_NAME)
                response = llm.predict(
                        prompt=WEBSITE_PROMPT_TEMPLATE.format(selected_prompt),
                        max_output_tokens=1024,
                    ).text
            except:
                response = "No text was generated."
                if (selected_prompt in THEMES_FOR_PROMPTS and 
                    "prompt_default_responses" in page_cfg):
                    index = THEMES_FOR_PROMPTS.index(selected_prompt)
                    response = page_cfg["prompt_default_responses"][index]
            st.session_state[GENERATED_TEXT_KEY] = response
 

if GENERATED_TEXT_KEY in st.session_state and UUID_KEY in st.session_state:
    st.write('**Generated text**')
    st.write(st.session_state[GENERATED_TEXT_KEY])
    selected_uuid = st.session_state[UUID_KEY]
    campaign_image_dict = st.session_state[
        CAMPAIGNS_KEY][selected_uuid].campaign_uploaded_images

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
        utils_image.render_image_edit_prompt(
            image_to_edit_key=IMAGE_TO_EDIT_KEY,
            edit_image_prompt_key=EDIT_IMAGE_PROMPT_KEY,
            edited_images_key=EDITED_IMAGES_KEY,
            mask_image=True,
            mask_image_key=MASK_IMAGE_KEY,
            select_button=True,
            selected_image_key=SELECTED_IMAGE_KEY,
            file_uploader_key=FILE_UPLOADER_KEY,
            campaign_image_dict=campaign_image_dict,
            local_image_list=page_cfg["local_images"]
        )
    elif st.session_state.get(IMAGE_OPTION_KEY, "") == "generated":      
        utils_image.render_image_generation_and_edition_ui(
            image_text_prompt_key=IMAGE_GENERATION_TEXT_PROMPT_KEY,
            generated_images_key=GENERATED_IMAGES_KEY,
            edit_image_prompt_key=EDIT_GENERATED_IMAGE_PROMPT_KEY,
            pre_populated_prompts=[
                IMAGE_PROMPT_TAMPLATE.format(
                    st.session_state[SELECTED_PROMPT_KEY])],
            select_button=True,
            selected_image_key=SELECTED_IMAGE_KEY,
            edit_button=True,
            image_to_edit_key=IMAGE_TO_EDIT_KEY,
            edit_with_mask=True,
            mask_image_key=MASK_IMAGE_KEY,
            edited_images_key=EDITED_IMAGES_KEY,
            download_button=False,
            auto_submit_first_pre_populated=True
        )


if (GENERATED_TEXT_KEY in st.session_state and 
    SELECTED_IMAGE_KEY in st.session_state and 
    CAMPAIGNS_KEY in st.session_state):
    campaigns_names = generate_names_uuid_dict().keys()

    image = None
    if SELECTED_IMAGE_KEY in st.session_state:
        st.write("**Selected image**")
        st.image(st.session_state[SELECTED_IMAGE_KEY])
        
    with st.form(PAGE_KEY_PREFIX+"_Link_To_Campaign"):
        st.write("**Choose a Campaign to save the results**")
        selected_name = st.selectbox("List of Campaigns", campaigns_names)
        link_to_campaign_button = st.form_submit_button("Save to Campaign")

    if link_to_campaign_button:
        image = "data:image/png;base64,"+base64.b64encode(
            st.session_state[SELECTED_IMAGE_KEY].getvalue()).decode("utf-8")
        selected_uuid = generate_names_uuid_dict()[selected_name]
        st.session_state[CAMPAIGNS_KEY][selected_uuid].website_post = {
            'website_text': st.session_state[GENERATED_TEXT_KEY]}
        st.session_state[CAMPAIGNS_KEY][selected_uuid].website_post.update(
            {'website_image': image})
        st.success(f"Post saved to campaign {selected_name}")


if (GENERATED_TEXT_KEY in st.session_state and
    IMAGE_TO_EDIT_KEY in st.session_state and
    FILE_UPLOADER_KEY in st.session_state and
    SELECTED_IMAGE_KEY not in st.session_state and
    CAMPAIGNS_KEY in st.session_state):
    campaigns_names = generate_names_uuid_dict().keys()
    with st.form(PAGE_KEY_PREFIX+"_Link_To_Campaign_Upload"):
        st.write("**Choose a Campaign to save the results**")
        selected_name = st.selectbox("List of Campaigns", campaigns_names)
        link_to_campaign_button = st.form_submit_button("Save to Campaign")

    if link_to_campaign_button:
        image = "data:image/png;base64,"+base64.b64encode(
            st.session_state[IMAGE_TO_EDIT_KEY]).decode("utf-8")
        selected_uuid = generate_names_uuid_dict()[selected_name]
        st.session_state[CAMPAIGNS_KEY][selected_uuid].website_post = {
            'website_text': st.session_state[GENERATED_TEXT_KEY]}
        st.session_state[CAMPAIGNS_KEY][selected_uuid].website_post.update(
            {'website_image': image})
        st.success(f"Post saved to campaign {selected_name}")
