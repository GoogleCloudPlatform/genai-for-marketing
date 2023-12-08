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
Image Generation: 
- Create realistic images from text descriptions.
"""


import streamlit as st
import utils_standalone_image_gen
from utils_config import PAGES_CFG


page_cfg = PAGES_CFG["16_image_generation"]

st.set_page_config(
    page_title=page_cfg["page_title"], 
    page_icon=page_cfg["page_icon"])

# State variables for image generation
PAGE_KEY_PREFIX = "ImageGeneration"
GENERATED_IMAGES_KEY = f"{PAGE_KEY_PREFIX}_Generated_Images"
IMAGE_TO_EDIT_GENERATION_KEY = f"{PAGE_KEY_PREFIX}_Image_To_Edit_Generation"
EDITED_IMAGES_GENERATION_KEY = f"{PAGE_KEY_PREFIX}_Edited_Images_Generation"
MASK_IMAGE_GENERATION_KEY = f"{PAGE_KEY_PREFIX}_Mask_Image_Generation"
IMAGE_GENERATION_TEXT_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Text_Prompt_Images_Generation"
EDIT_GENERATED_IMAGE_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Edit_Text_Prompt_Images_Generation"

# State variables for image editing
IMAGE_TO_EDIT_KEY = f"{PAGE_KEY_PREFIX}_Image_To_Edit"
EDITED_IMAGES_KEY = f"{PAGE_KEY_PREFIX}_Edited_Images"
MASK_IMAGE_KEY = f"{PAGE_KEY_PREFIX}_Mask_Image"
FILE_UPLOADER_KEY = f"{PAGE_KEY_PREFIX}_File_Uploader"
IMAGE_TO_EDIT_PROMPT_KEY = f"{PAGE_KEY_PREFIX}_Edit_Prompt_key"

# Pre populated prompts for image generation
PRE_POPULATED_PROMPTS = page_cfg["pre_populated_prompts"]

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path=page_cfg["sidebar_image_path"])

cols = st.columns([13, 87])
with cols[0]:
    st.image(page_cfg["page_title_icon"])
with cols[1]:
    st.title(page_cfg["page_title"])

# Generate image
st.subheader('Image Generation')
st.write('Create a prompt to generate images.')
utils_standalone_image_gen.render_image_generation_and_edition_ui(
    image_text_prompt_key=IMAGE_GENERATION_TEXT_PROMPT_KEY,
    generated_images_key=GENERATED_IMAGES_KEY,
    edit_image_prompt_key=EDIT_GENERATED_IMAGE_PROMPT_KEY,
    pre_populated_prompts=PRE_POPULATED_PROMPTS,
    select_button=False,
    edit_button=True,
    image_to_edit_key=IMAGE_TO_EDIT_GENERATION_KEY,
    edit_with_mask=True,
    mask_image_key=MASK_IMAGE_GENERATION_KEY,
    edited_images_key=EDITED_IMAGES_GENERATION_KEY,
    download_button=True)

st.subheader('Image Editing')
st.write('Upload and edit an image with a text prompt.')

# Edit image
utils_standalone_image_gen.render_image_edit_prompt(
    edited_images_key=EDITED_IMAGES_KEY,
    edit_image_prompt_key=IMAGE_TO_EDIT_PROMPT_KEY,
    upload_file=True,
    image_to_edit_key=IMAGE_TO_EDIT_KEY,
    mask_image=True,
    mask_image_key=MASK_IMAGE_KEY,
    download_button=True,
    file_uploader_key=FILE_UPLOADER_KEY)
