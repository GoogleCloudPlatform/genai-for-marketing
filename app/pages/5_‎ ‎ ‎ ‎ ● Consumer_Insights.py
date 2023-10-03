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
- Improve the search experience for enterprise users with Vertex AI Search.
"""

import streamlit as st

from google.cloud import discoveryengine
from proto import Message
from utils_config import GLOBAL_CFG, PAGES_CFG
from utils_vertex_ai_search import search

page_cfg = PAGES_CFG["5_consumer_insights"]

# Set project parameters
PROJECT_ID = GLOBAL_CFG["project_id"]
LOCATION = page_cfg["search_location"]
DATASTORES = page_cfg["datastores"]

search_client = discoveryengine.SearchServiceClient()
complete_client = discoveryengine.CompletionServiceClient()

# State variables for Vertex AI Search results
PAGE_KEY_PREFIX = "VertexAISearch"
QUERY_KEY = f"{PAGE_KEY_PREFIX}_Query"
RESULTS_KEY = f"{PAGE_KEY_PREFIX}_Results"
AUTOCOMPLETE_KEY = f"{PAGE_KEY_PREFIX}_Autocomplete"


st.set_page_config(
    page_title=page_cfg["page_title"], 
    page_icon=page_cfg["page_icon"])

import utils_styles
utils_styles.sidebar_apply_style(
    style=utils_styles.style_sidebar,
    image_path=page_cfg["sidebar_image_path"]
)


cols = st.columns([15, 85])
with cols[0]:
    st.image(page_cfg["page_title_image"])
with cols[1]:
    st.title(page_cfg["page_title"])

st.write(
    "This page demonstrates how to use Vertex AI Search "
    "to find marketing assets."
)

datastore = None
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

if (datastore and 
    QUERY_KEY in st.session_state and 
    RESULTS_KEY not in st.session_state):
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
                search_result_dict = Message.to_dict(search_result)
                document = search_result_dict.get("document", {})
                struct_data = document.get("derived_struct_data",{})
                title = struct_data.get("title", "")
                link = struct_data.get("link", "")
                snippets = struct_data.get("snippets", [])
                if len(snippets) > 0:
                    snippet = snippets[0].get("snippet", "")
                    html_snippet = snippets[0].get("htmlSnippet", "")
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
