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
Text Generation: 
- Create a variety of text content, such as blog posts, articles, and product descriptions.
"""


import streamlit as st
import utils_prompt
from utils_config import GLOBAL_CFG, MODEL_CFG, PAGES_CFG

page_cfg = PAGES_CFG["15_text_generation"]

# Set project parameters
PROJECT_ID = GLOBAL_CFG["project_id"]
LOCATION = GLOBAL_CFG["location"]
TEXT_MODEL_NAME = MODEL_CFG["text"]["text_model_name"]

# State variables for text generation
PAGE_KEY_PREFIX = "TextGeneration"
GENERATED_TEXT_KEY = f"{PAGE_KEY_PREFIX}_Generated_Text"

st.set_page_config(
    page_title=page_cfg["page_title"],
    page_icon=page_cfg["page_icon"])

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path=page_cfg["sidebar_image_path"])

cols = st.columns([13, 87])
with cols[0]:
    st.image(page_cfg["page_title_icon"])
with cols[1]:
    st.title(page_cfg["page_title"])

st.write(
    """
    Create prompts to generate text using Vertex AI PaLM API.
    """)

# Prompt engineering for text generation
utils_prompt.render_marketing_prompt_design(
    project_id=PROJECT_ID,
    location=LOCATION,
    state_key=GENERATED_TEXT_KEY,
    translate=True
)
