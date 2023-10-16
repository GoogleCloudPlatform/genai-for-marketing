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
Content Search: 
- Improve the search experience for enterprise users with Gen App Builder.
"""


import streamlit as st
import base64

import utils_config
from utils_streamlit import reset_page_state
from utils_enterprise_search import search, complete_query
from google.cloud import discoveryengine

# Set project parameters
PROJECT_ID = utils_config.get_env_project_id()
LOCATION = utils_config.SEARCH_LOCATION
DATASTORES = utils_config.DATASTORES

search_client = discoveryengine.SearchServiceClient()
complete_client = discoveryengine.CompletionServiceClient()

# State variables for enterprise search results
PAGE_KEY_PREFIX = "EnterpriseSearch"
QUERY_KEY = f"{PAGE_KEY_PREFIX}_Query"
RESULTS_KEY = f"{PAGE_KEY_PREFIX}_Results"
AUTOCOMPLETE_KEY = f"{PAGE_KEY_PREFIX}_Autocomplete"


st.set_page_config(
    page_title="Consumer Insights", 
    page_icon='/app/images/favicon.png')

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path='/app/images/menu_icon_2.png'
)


cols = st.columns([15, 85])
with cols[0]:
    st.image('/app/images/consumer_icon.png')
with cols[1]:
    st.title('Consumer Insights')

st.write(
    """
    This page demonstrates how to use Vertex AI Search to find marketing assets. 
    """
)

st.write('Search for assets using Vertex AI Search')

if DATASTORES:
    with st.form(key=f"{PAGE_KEY_PREFIX}_form"):
        datastore = list(DATASTORES.keys())[0]

        text = st.text_input("**Query**", key=f"{PAGE_KEY_PREFIX}_text_input")
        search_button = st.form_submit_button("Search")

    if search_button and text != st.session_state.get(QUERY_KEY):
        st.session_state[QUERY_KEY] = text
        if RESULTS_KEY in st.session_state:
            del st.session_state[RESULTS_KEY]
else:
    st.info('Datastore not available.')

if QUERY_KEY in st.session_state and RESULTS_KEY not in st.session_state:
    with st.spinner(f"Searching for '{st.session_state[QUERY_KEY]}'"):
        results = []
        try:
            search_results = search(
                search_query=st.session_state[QUERY_KEY],
                project_id=PROJECT_ID,
                location=LOCATION,
                search_engine_id=datastore,
                serving_config_id=DATASTORES[datastore],
                search_client=search_client
                )
        except Exception as e:
            st.error(e)
        else:
            if search_results:
                st.success('Query executed successfully. Retrieving results.')
            else:
                st.success('Empty results.')

            for search_result in search_results:
                struct_data = search_result.document.derived_struct_data
                title = struct_data["title"]
                link = struct_data["link"]
                snippet = struct_data["snippets"][0]["snippet"]
                html_snippet = struct_data["snippets"][0]["htmlSnippet"]
                result = {
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                    "html_snippet": html_snippet
                }
                results.append(result)
        
            if results:
                st.session_state[RESULTS_KEY] = results

if RESULTS_KEY in st.session_state:
    for i, result in enumerate(st.session_state[RESULTS_KEY]):
        st.subheader(f"{i+1}. {result['title']}")
        st.write(result["link"])
        st.write(result["html_snippet"], unsafe_allow_html=True)
        st.divider()

