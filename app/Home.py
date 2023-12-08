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
import shutil, os
import base64
import streamlit as st
from utils_config import PAGES_CFG


def setup_pages():
    pages_path = os.path.join(os.path.dirname(__file__), "pages")
    templates_path = os.path.join(os.path.dirname(__file__), "pages_templates")

    files = [f for f in os.listdir(pages_path) if os.path.join(pages_path, f)]

    remove_files = set(files).difference(PAGES_CFG["menu"]['items'])
    copy_files = set(PAGES_CFG["menu"]['items']).difference(files)

    print("remove_files", remove_files)
    try:
        for f in remove_files:
            os.remove(os.path.join(pages_path, f))
    except Exception as e:
        print("-->",e)

    print("copy_files", copy_files)
    try:
        for f in copy_files:
            shutil.copy(os.path.join(templates_path, f), os.path.join(pages_path, f))
    except Exception as e:
        print("-->",e)

setup_pages()

page_cfg = PAGES_CFG["home"]

st.set_page_config(
    page_title=page_cfg["page_title"], 
    page_icon=page_cfg["page_icon"]
)

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path=page_cfg["sidebar_image_path"]
)

file_name_1 = page_cfg["file_name_1"]
file_name_2 = page_cfg["file_name_2"]

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

st.divider()

with st.expander("disclaimer: this is not an official Google product"):
    st.write("""
This is not an official Google product. This is a functional demo with a purpose to showcase capabilities of Google products.
""")
