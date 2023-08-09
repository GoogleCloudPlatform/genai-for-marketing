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
import utils_image
import utils_config
from utils_streamlit import reset_page_state


st.set_page_config(
    page_title='Image Generation', 
    page_icon='/app/images/favicon.png')

# Set project parameters
PROJECT_ID = utils_config.get_env_project_id()
LOCATION = utils_config.LOCATION
MODEL_NAME = 'imagegeneration'
IMAGEN_API_ENDPOINT = f'{LOCATION}-aiplatform.googleapis.com'
IMAGEN_ENDPOINT = f'projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL_NAME}'

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
PRE_POPULATED_PROMPTS = [
    'A photo of a handbag on a kitchen counter, natural lighting, 4k',
    'A photo of a handbag on the beach, natural lighting, 4k',
    'Studio photo of a purple handbag, natural lighting, 4k'
]

cols = st.columns([13, 87])
with cols[0]:
    st.image('/app/images/favicon.png')
with cols[1]:
    st.title('Image Generation')

st.write(
    """
    Create prompts to generate image using Vertex AI PaLM 2 API.
    """
)

# Generate image
st.subheader('Image Generation')
st.write('Create a prompt to generate images.')
utils_image.render_image_generation_and_edition_ui(
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
st.write('Create a prompt to edit an image.')

# Edit image
utils_image.render_image_edit_prompt(
    edited_images_key=EDITED_IMAGES_KEY,
    edit_image_prompt_key=IMAGE_TO_EDIT_PROMPT_KEY,
    upload_file=True,
    image_to_edit_key=IMAGE_TO_EDIT_KEY,
    mask_image=True,
    mask_image_key=MASK_IMAGE_KEY,
    download_button=True,
    file_uploader_key=FILE_UPLOADER_KEY)
