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
import tomllib
import utils_image
import vertexai

from vertexai.preview.language_models import TextGenerationModel
from utils_campaign import generate_names_uuid_dict


# Load configuration file
with open("./app_config.toml", "rb") as f:
    data = tomllib.load(f)

page_cfg = data["pages"]["8_website_post"]
st.set_page_config(page_title=page_cfg["page_title"],
                   page_icon=page_cfg["page_icon"])

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path=page_cfg["sidebar_image_path"]
)

# Set project parameters
PROJECT_ID = data["global"]["project_id"]
LOCATION = data["global"]["location"]
TEXT_MODEL_NAME = data["models"]["text"]["text_model_name"]
CAMPAIGNS_KEY = data["pages"]["campaigns"]["campaigns_key"]

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
IMAGE_TO_EDIT_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Edit_Prompt_key"

SELECTED_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Selected_Prompt"

# State variables for image generation
IMAGE_GENERATION_TEXT_PROMPT_KEY = (
        f"{PAGE_KEY_PREFIX}_Text_Prompt_Images_Generation")
EDIT_GENERATED_IMAGE_PROMPT_KEY = (
        f"{PAGE_KEY_PREFIX}_Edit_Text_Prompt_Images_Generation")
DEFAULT_IMAGE_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Image_Prompt"

# Templates
WEBSITE_PROMPT_TEMPLATE = page_cfg["prompt_website_template"]
IMAGE_PROMPT_TAMPLATE = page_cfg["prompt_image_template"]
THEMES_FOR_PROMPTS = page_cfg["prompt_themes"]


cols = st.columns([15, 85])
with cols[0]:
    st.image(page_cfg["page_title_image"])
with cols[1]:
    st.title(page_cfg["page_title"])

st.write(
    "This page provides a step-by-step guide to generating a website post.")

st.subheader('Post Generation')

flag_new = False

with st.form(key='form_post_generation'):
    selected_prompt = st.selectbox(
        label='Select a scenario to generate the website post',
        options=THEMES_FOR_PROMPTS)
    image_option = st.radio(label="Choose an option for the post image:",
             options=["uploaded", "generated"],
             format_func=lambda x: f"{x.capitalize()} Image")

    st.session_state[SELECTED_PROMPT_KEY] = selected_prompt

    submit_button = st.form_submit_button(label='Generate')

if submit_button:
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
    
    st.session_state[IMAGE_OPTION] = image_option 
    flag_new = True

    with st.spinner('Generating website post ...'):
        try:
            vertexai.init(project=PROJECT_ID, location=LOCATION)
            llm = TextGenerationModel.from_pretrained(TEXT_MODEL_NAME)
            response = llm.predict(
                    prompt=WEBSITE_PROMPT_TEMPLATE.format(selected_prompt),
                    max_output_tokens=1024,
                ).text
        except:
            response = ""
        if not response:
            if selected_prompt in THEMES_FOR_PROMPTS:
                index = THEMES_FOR_PROMPTS.index(selected_prompt)
                response = page_cfg["prompt_default_responses"][index]
        st.session_state[GENERATED_TEXT_KEY] = response

    st.write('**Generated text**')
    st.write(st.session_state[GENERATED_TEXT_KEY])
    error = False

    try:
        if image_option == "uploaded":
            utils_image.render_image_edit_prompt(
                edited_images_key=EDITED_IMAGES_KEY,
                edit_image_prompt_key=IMAGE_TO_EDIT_PROMPT_KEY,
                upload_file=True,
                image_to_edit_key=IMAGE_TO_EDIT_KEY,
                mask_image=True,
                mask_image_key=MASK_IMAGE_KEY,
                download_button=False,
                file_uploader_key=FILE_UPLOADER_KEY,
                select_button=True,
                selected_image_key=SELECTED_IMAGE_KEY)
        else:
            utils_image.render_image_generation_and_edition_ui(
                image_text_prompt_key=IMAGE_GENERATION_TEXT_PROMPT_KEY,
                generated_images_key=GENERATED_IMAGES_KEY,
                edit_image_prompt_key=EDIT_GENERATED_IMAGE_PROMPT_KEY,
                pre_populated_prompts=[
                    IMAGE_PROMPT_TAMPLATE.format(selected_prompt)],
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
    except:
        error = True

    if (error or 
        (image_option == "generated" and 
         not st.session_state[GENERATED_IMAGES_KEY])):
            if selected_prompt == THEMES_FOR_PROMPTS[0]:
                utils_image.get_default_image_bytesio(
                    page_cfg["default_image_0"], SELECTED_IMAGE_KEY, True)
            elif selected_prompt == THEMES_FOR_PROMPTS[1]:
                utils_image.get_default_image_bytesio(
                    page_cfg["default_image_1"], SELECTED_IMAGE_KEY, True)
            elif selected_prompt == THEMES_FOR_PROMPTS[2]:
                utils_image.get_default_image_bytesio(
                    page_cfg["default_image_2"], SELECTED_IMAGE_KEY, True)
            elif selected_prompt == THEMES_FOR_PROMPTS[3]:
                utils_image.get_default_image_bytesio(
                    page_cfg["default_image_3"], SELECTED_IMAGE_KEY, True)


if GENERATED_TEXT_KEY in st.session_state and not flag_new:
    st.write('**Generated text**')
    st.write(st.session_state[GENERATED_TEXT_KEY])

    try:
        if st.session_state[IMAGE_OPTION] == "uploaded":
            utils_image.render_image_edit_prompt(
                edited_images_key=EDITED_IMAGES_KEY,
                edit_image_prompt_key=IMAGE_TO_EDIT_PROMPT_KEY,
                upload_file=True,
                image_to_edit_key=IMAGE_TO_EDIT_KEY,
                mask_image=True,
                mask_image_key=MASK_IMAGE_KEY,
                download_button=False,
                file_uploader_key=FILE_UPLOADER_KEY,
                select_button=True,
                selected_image_key=SELECTED_IMAGE_KEY)
        else:
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
                auto_submit_first_pre_populated=False)
    except:
        st.info('Could not generate image due to policy restrictions. '
                'Please provide a different prompt.')
    else:
        if EDITED_IMAGES_KEY in st.session_state:
            if not st.session_state[EDITED_IMAGES_KEY]:
                st.info('Could not generate image due to policy restrictions. '
                        'Please provide a different prompt.')

    if SELECTED_IMAGE_KEY in st.session_state:
        with st.container():
            st.write("**Currently selected image**")
            st.image(st.session_state[SELECTED_IMAGE_KEY])


if (GENERATED_TEXT_KEY in st.session_state and 
    SELECTED_IMAGE_KEY in st.session_state and 
    CAMPAIGNS_KEY in st.session_state):
    campaigns_names = generate_names_uuid_dict().keys()
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
