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
import base64

st.set_page_config(
    page_title="Gen AI for Marketing", 
    page_icon='/app/images/favicon.png'
)

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path='/app/images/menu_icon_2.png'
)

file_name_1 = "/app/images/intro_home_1.png"
file_name_2 = "/app/images/intro_home_2.png"

with open(file_name_1, "rb") as fp:
    contents = fp.read()
    main_image_1 = base64.b64encode(contents).decode("utf-8")
    main_image_1 = 'data:image/png;base64,'+main_image_1

with open(file_name_2, "rb") as fp:
    contents = fp.read()
    main_image_2 = base64.b64encode(contents).decode("utf-8")
    main_image_2 = 'data:image/png;base64,'+main_image_2

st.image(image=main_image_1)
st.divider()
st.image(image=main_image_2)
