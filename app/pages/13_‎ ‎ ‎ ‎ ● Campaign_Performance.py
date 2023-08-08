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
import base64
import utils_config

st.set_page_config(
    page_title="Campaign Performance", 
    page_icon='/app/images/favicon.png',
    layout='wide'
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

DASHBOARDS = {
    # Sample Dashboard link
    'Campaign Performance': 'https://googledemo.looker.com/embed/dashboards/2127?allow_login_screen=true',
    'Campaign Comparison':'https://googledemo.looker.com/embed/dashboards/2128?allow_login_screen=true',
    'Product Performance':'https://googledemo.looker.com/embed/dashboards/2135?allow_login_screen=true',
    'Propensity to Purchase Predictions':'https://googledemo.looker.com/embed/dashboards/2136?allow_login_screen=true',
    'Customer Lifetime Value':'https://googledemo.looker.com/embed/dashboards/2129?allow_login_screen=true',
    'Demand Forecasting':'https://googledemo.looker.com/embed/dashboards/2130?allow_login_screen=true',
    'Sentiment Analysis':'https://googledemo.looker.com/embed/dashboards/2139?allow_login_screen=true'
}


# State variables
PAGE_KEY_PREFIX = "CampaignPerformance"
DASHBOARD_KEY = f"{PAGE_KEY_PREFIX}_Dashboard"

cols = st.columns([15,70,15])
with cols[1]:
    cols = st.columns([10, 90])
    with cols[0]:
        st.image('/app/images/opt_icon.png')
    with cols[1]:
        st.title('Campaign Performance')

    st.write(
        """
        This page presents visualizations of marketing data in the form of Looker Dashboards.
        """
    )

    if utils_config.DASHBOARDS:
        with st.form(key='generate_marketing_dashboard'):
            option = st.selectbox(
                'Select a dashboard to be displayed',
                tuple(DASHBOARDS.keys()))

            submit_button = st.form_submit_button(label='Generate Dashboard')

        if submit_button:
            st.session_state[DASHBOARD_KEY] = option
    else:
        st.info('Dashboards not available.')

if DASHBOARD_KEY in st.session_state:
    st.components.v1.html(f"""
<iframe src="{DASHBOARDS.get(st.session_state[DASHBOARD_KEY])}" frameborder="0" width="100%" height="800px"></iframe>
{utils_config.INFOBOT}
""", height=800)
else:
    st.components.v1.html(f"""
<iframe src="https://googledemo.looker.com/embed/dashboards/2127?allow_login_screen=true" frameborder="0" width="100%" height="800px"></iframe>
{utils_config.INFOBOT}
""", height=800)
