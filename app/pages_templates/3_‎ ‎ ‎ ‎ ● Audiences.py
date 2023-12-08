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
Audience and Insight finder: 
- Create a conversational interface with data 
  by translating from natural language to SQL queries.
"""

import streamlit as st
import utils_codey
import vertexai

from google.cloud import bigquery
from vertexai.preview.language_models import TextGenerationModel
from utils_config import GLOBAL_CFG, MODEL_CFG, PAGES_CFG


page_cfg = PAGES_CFG["3_audiences"]

# Set project parameters
PROJECT_ID = GLOBAL_CFG["project_id"]
LOCATION = GLOBAL_CFG["location"]
TEXT_MODEL_NAME = MODEL_CFG["text"]["text_model_name"]

DATASET_ID = page_cfg["dataset_id"]
TAG_NAME = page_cfg["tag_name"]

TAG_TEMPLATE_NAME = f'projects/{PROJECT_ID}/locations/{LOCATION}/tagTemplates/{TAG_NAME}'
QUERY = (
    f'SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.INFORMATION_SCHEMA.TABLES`'
    ' WHERE table_name NOT LIKE "%metadata%"')

bqclient = bigquery.Client(project=PROJECT_ID)
vertexai.init(project=PROJECT_ID, location=LOCATION)
llm = TextGenerationModel.from_pretrained(TEXT_MODEL_NAME)

# State variables for code generation and data preview
PAGE_KEY_PREFIX = "TalkToData"
PREVIEW_TABLES_KEY = f"{PAGE_KEY_PREFIX}_Preview_Tables"
RESULT_PREVIEW_QUERY_KEY = f"{PAGE_KEY_PREFIX}_Result_Preview_Query"
RESULT_FINAL_QUERY_KEY = f"{PAGE_KEY_PREFIX}_Result_Final_Query"
GENCODE_KEY = f"{PAGE_KEY_PREFIX}_Gen_Code"
PROMPT_TEMPLATE_KEY = f"{PAGE_KEY_PREFIX}_Prompt_Template"
DATASET_METADATA_KEY = f"{PAGE_KEY_PREFIX}_Dataset_Metadata"


st.set_page_config(page_title=page_cfg["page_title"], 
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
    "This page provides instructions on how to extract data from BigQuery"  
    "using natural language and the PaLM API. "
    "PaLM is a large language model from Google AI that can understand "
    "and respond to natural language queries. " 
    "By using PaLM, you can ask questions about your data in plain English, "
    "and PaLM will generate the SQL queries necessary to retrieve the data."
)

# =========================== Data preview =====================================

st.subheader('Data preview')
st.write('Click to preview the CDP dataset tables')
preview_button = st.button('Preview tables')

if preview_button:
    if PREVIEW_TABLES_KEY in st.session_state:
        del st.session_state[PREVIEW_TABLES_KEY]
    else:
        dataset_path = f"{PROJECT_ID}.{DATASET_ID}"
        query_template = f"SELECT * FROM `{dataset_path}.""{table}` LIMIT 3"
        table_names = ["customers", "events", "transactions"] 
        st.session_state[PREVIEW_TABLES_KEY] = [{
            'query': query_template.format(table=table_name),
            'name': table_name
        } for table_name in table_names]

if PREVIEW_TABLES_KEY in st.session_state:
    if RESULT_PREVIEW_QUERY_KEY not in st.session_state:
        result_query = []
        with st.spinner('Querying BigQuery...'):
            for table in st.session_state[PREVIEW_TABLES_KEY]:
                result_query.append({
                    "name": table['name'],
                    "dataframe": bqclient.query(table['query']).to_dataframe()
                })
        st.session_state[RESULT_PREVIEW_QUERY_KEY] = result_query
    
    for result in st.session_state[RESULT_PREVIEW_QUERY_KEY]:
        st.write(f'Preview for table: {result["name"]}')
        st.dataframe(result['dataframe'])

st.subheader('Audience Insights Finder')

utils_codey.generate_sql_and_query(
    state_key=f"{PAGE_KEY_PREFIX}_insight",
    title="Ask your data",
    query=QUERY,
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    tag_template_name=TAG_TEMPLATE_NAME,
    bqclient=bqclient,
    default_query=page_cfg.get("audience_query_0", "")
)
