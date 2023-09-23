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


import base64
import streamlit as st


style_sidebar = """
    <style>
        [data-testid="stSidebarNav"] {{
            background-image: url({logo});
            background-repeat: no-repeat;
            padding-top: 80px;
            background-position: top 70px left 25px;
            background-size: 200px;
            position: relative; /* To position the button with respect to this element */
        }}
        
        [data-testid="stDecoration"] {{
            background-image: linear-gradient(90deg, rgb(51 103 214), rgb(93 135 222));
        }}

        section[data-testid="stSidebar"] {{
            border-top-right-radius: 15px;    /* Rounded top right corner */
            border-bottom-right-radius: 15px; /* Rounded bottom right corner */
        }}

        .rounded-button {{
            font-family: "Source Sans Pro", sans-serif;
            display: inline-block; /* Allows for padding and other block properties on the <a> element */
            border: 1px solid #d6d6d9ff; 
            background-color: transparent; /* Transparent background */
            padding: 6px 13px; /* Spacing inside the button */
            border-radius: 7px; /* Rounded corners */
            font-size: 1rem;
            cursor: pointer; /* Hand cursor on hover */
            transition: background-color 0.3s; /* Smooth transition for hover effect */
            text-decoration: none; /* Removes the default underline from the hyperlink */
            color: #313340ff !important; /* Sets the text color to black */
        }}

        .rounded-button:hover {{
            text-decoration: none;
            color: #3367d6ff !important; /* Sets the text color to black */
            border-color: #3367d6ff !important;
        }}

        [data-testid="stToolbar"] {{
            display: none;
        }}

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
    </style>
"""


def sidebar_apply_style(
        style: str, 
        image_path: str):
    
    with open(image_path, "rb") as fp:
        contents = fp.read()
        menu_image = base64.b64encode(contents).decode("utf-8")
        menu_image = 'data:image/png;base64,'+menu_image

    st.markdown(
        style.format(
            logo=menu_image,
            icon_click=menu_image,
    ), unsafe_allow_html=True)