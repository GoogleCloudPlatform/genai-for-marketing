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
Utility module for Codey releated demo.
"""

import pandas as pd
import streamlit as st

from google.cloud import bigquery
from google.cloud import datacatalog_v1
from pandas import DataFrame
from typing import Optional
from utils_campaign import generate_names_uuid_dict
from utils_config import GLOBAL_CFG, MODEL_CFG, PAGES_CFG
from utils_streamlit import reset_page_state
from vertexai.preview.language_models import TextGenerationModel


TEXT_MODEL_NAME = MODEL_CFG["text"]["text_model_name"]

PROMPT = PAGES_CFG["3_audiences"]["prompt_nl_sql"]
PROMPT_PROJECT_ID = [GLOBAL_CFG['project_id']]*130
CAMPAIGNS_KEY = PAGES_CFG["campaigns"]["campaigns_key"]


def get_tags_from_table(
        dataset_id: str, 
        table_id: str, 
        project_id: str, 
        tag_template_name: str
):
    """Gets the tags from a BigQuery table.

    Args:
        dataset_id:
             The ID of the BigQuery dataset that contains the table.
        table_id: 
            The ID of the BigQuery table.
        project_id: 
            The ID of the Google Cloud project.
        tag_template_name: 
            The name of the tag template.

    Returns:
        A string containing the tags for the table.
    """
    # Lookup Data Catalog's Entry referring to the table.
    datacatalog_client = datacatalog_v1.DataCatalogClient()
    resource_name = (
        f"//bigquery.googleapis.com/projects/{project_id}"
        f"/datasets/{dataset_id}/tables/{table_id}"
    )
    table_entry = datacatalog_client.lookup_entry(
        request={"linked_resource": resource_name}
    )

    # Make the request
    page_result = datacatalog_client.list_tags(parent=table_entry.name)
    tags_str = ''
    # Handle the response
    for response in page_result:
        if response.template == tag_template_name:
            desc = response.fields["description"].string_value
            data_type = response.fields["data_type"].string_value
            pk = response.fields["is_primary_key"].bool_value
            fk = response.fields["is_foreign_key"].bool_value            
            tags_str += ("Full table name: {} "
                         "- Column: {} " 
                         "- Data Type: {} " 
                         "- Primary Key: {} " 
                         "- Foreign Key: {} " 
                         "- Description: {}\n".format(
                f'`{project_id}.{dataset_id}.{table_id}`', 
                response.column, 
                data_type, 
                pk, 
                fk, 
                desc))

    return tags_str


def get_metadata_from_dataset(
        query: str,
        project_id: str,
        dataset_id: str, 
        tag_template_name: str,
        state_key: str
):
    """Gets the metadata for all tables in a BigQuery dataset.

    Args:
        query: 
            The BigQuery query to run to get the list of tables.
        project_id: 
            The ID of the BigQuery project.
        dataset_id: 
            The ID of the BigQuery dataset.
        tag_template_name: 
            The name of the BigQuery tag template to use to get the table 
            descriptions.
        state_key: 
            The key to use to store the metadata in the Streamlit 
            session state.
    """
    
    if len(st.session_state.get(state_key, [])) == 0:
        # print("Gets the metadata once")
        bqclient = bigquery.Client(project=project_id)
        query_job = bqclient.query(query)  # API request
        rows = query_job.result()
        metadata = []
    
        for row in rows:
            full_table_path = f'`{project_id}.{dataset_id}.{row.table_name}`'
            table_metadata = f'[SCHEMA details for table {full_table_path}]\n'

            table_metadata += get_tags_from_table(
                dataset_id, row.table_name, project_id, tag_template_name)
            metadata.append(table_metadata)

        st.session_state[state_key] = metadata


def get_full_context_from_list(metadata: list):
    """Gets the full context from a list of metadata.

    Args:
        metadata: A list of metadata objects.

    Returns:
        A string containing the full context.
    """
    context = ''
    for i in metadata:
        context += i
    return context


def generate_prompt(
        question: str,
        metadata: list,
        state_key: str,
):
    """Generates a prompt for a GoogleSQL query compatible with BigQuery.

    Args:
        question: 
            The question to answer.
        metadata: 
            A list of dictionaries, where each dictionary describes a BigQuery 
            table. 
            The dictionaries should have the following keys:
            - name: The name of the table.
            - schema: The schema of the table.
            - description: A description of the table.
        state_key: 
            The key to use to store the prompt in the session state.

    Returns:
        The prompt.
    """
    context = ''
    for i in metadata:
        context += i

    st.session_state[state_key] = f"""{PROMPT.format(*PROMPT_PROJECT_ID)}
{context}
[Q]: {question}
[SQL]: 
"""


def generate_sql_and_query(
        state_key: str,
        title: str,
        query: str,
        project_id: str,
        dataset_id: str,
        tag_template_name: str,
        bqclient: bigquery.Client,
        default_query: str="") -> Optional[DataFrame]:
    """Generates a GoogleSQL query and executes it against a BigQuery dataset.

    Args:
        state_key: 
            A unique identifier for the current session.
        title: 
            The title of the UI page.
        query: 
            The initial query text.
        project_id: 
            The ID of the BigQuery project.
        dataset_id: 
            The ID of the BigQuery dataset.
        tag_template_name: 
            The name of the tag template to use for the query.
        bqclient: 
            A BigQuery client object.

    Returns:
        A DataFrame containing the results of the query.

    Raises:
        NotFoundError: If the dataset or table is not found.
        BadRequestError: If the query is invalid.
    """
    with st.form(f"{state_key}_form"):
        st.write(f"**{title}**")
        placeholder_for_selectbox = st.empty()
        placeholder_for_custom_question = st.empty()
        submit_button = st.form_submit_button("Submit")
    
    with placeholder_for_selectbox:

        question_option = st.selectbox(
            label=("Select one of the options to ask BigQuery tables "
                   "and find your audience"),
            options=PAGES_CFG["3_audiences"][
                "prompt_examples"] + ["Another question..."],
            key=f"{state_key}_question_prompt_text_area")

    with placeholder_for_custom_question:
        if question_option == "Another question...":
            otherQuestion = st.text_input("Enter your custom question")
        else:
            otherQuestion = ""

    if submit_button:
        question = ""
        reset_page_state(state_key)
        if question_option == "Another question":
            if otherQuestion == "":
                st.info("Please write your custom question...")
                return None
            else:
                question = otherQuestion
        elif question_option:
            question = question_option
        with st.spinner('Retrieving metadata from BigQuery'):
            get_metadata_from_dataset(
                query=query, 
                project_id=project_id, 
                dataset_id=dataset_id,
                tag_template_name=tag_template_name,
                state_key=f"{state_key}_Dataset_Metadata")

        with st.spinner('Creating a prompt'):
            generate_prompt(
                question, 
                st.session_state[f"{state_key}_Dataset_Metadata"],
                f"{state_key}_Prompt_Template")

        with st.expander('Prompt'):
            st.text(st.session_state[f"{state_key}_Prompt_Template"])
        
        with st.spinner('Generating the GoogleSQL statement with PaLM'):
            client_code_model = TextGenerationModel.from_pretrained(
                TEXT_MODEL_NAME)
            try:
                gen_code = client_code_model.predict(
                    prompt = st.session_state[f"{state_key}_Prompt_Template"],
                    max_output_tokens = 1024,
                    temperature=0.2
                ).text
            except Exception as e:
                print("Error")
                print(str(e))
                gen_code = ""

            gen_code = gen_code.replace("```sql","").replace("```","")
            if gen_code:
                st.session_state[f"{state_key}_Gen_Code"] = gen_code
            elif default_query:
                st.session_state[
                    f"{state_key}_Gen_Code"] = default_query.format(
                    *PROMPT_PROJECT_ID)

        try:
            with st.spinner('Querying BigQuery...'):
                result_query = bqclient.query(
                    st.session_state[f"{state_key}_Gen_Code"])
                result_query.result()
        except:
            if default_query:
                st.session_state[f"{state_key}_Gen_Code"] = default_query.format(
                *PROMPT_PROJECT_ID)
            with st.spinner('Querying BigQuery...'):
                try:
                    result_query = bqclient.query(
                        st.session_state[f"{state_key}_Gen_Code"])
                    result_query.result()
                except Exception as e:
                    print(str(e))
                    st.session_state[
                        f"{state_key}_Result_Final_Query"
                    ] = pd.DataFrame({'Empty' : []})

                else:
                    st.session_state[
                        f"{state_key}_Result_Final_Query"
                    ] = result_query.to_dataframe()
    
            st.write('Resulting query generated by PaLM 2')
            st.write(f"""```sql
                    {st.session_state[f"{state_key}_Gen_Code"]}```""")
            st.success('Query executed successfully. Retrieving dataset.')
            st.write('')
            st.write('Resulting table (limited by 50 rows)')
            st.dataframe(
                st.session_state[f"{state_key}_Result_Final_Query"].iloc[:50])
        else:
            st.write('Resulting query generated by PaLM 2')
            st.write(f"""```sql
                    {st.session_state[f"{state_key}_Gen_Code"]}```""")
            st.success('Query executed successfully. Retrieving dataset.')
            st.session_state[
                f"{state_key}_Result_Final_Query"
            ] = result_query.to_dataframe()
            st.write('')
            st.write('Resulting table (limited by 50 rows)')
            st.dataframe(
                st.session_state[f"{state_key}_Result_Final_Query"].iloc[:50])

    else:
        if f"{state_key}_Prompt_Template" in st.session_state:
            with st.expander('Prompt'):
                st.text(st.session_state[f"{state_key}_Prompt_Template"])

        if f"{state_key}_Gen_Code" in st.session_state:
            st.write('Resulting query generated by PaLM 2')
            st.write(st.session_state[f"{state_key}_Gen_Code"])

        if f"{state_key}_Result_Final_Query" in st.session_state:
            st.write('Resulting table (limited by 50 rows)')
            st.dataframe(
                st.session_state[f"{state_key}_Result_Final_Query"].iloc[:50])

    if (f"{state_key}_Result_Final_Query" in st.session_state and
        CAMPAIGNS_KEY in st.session_state):
        df = st.session_state[f"{state_key}_Result_Final_Query"]
        if "email" not in df.columns:
            st.info("No email column found in the results")
        else:
            campaigns_names = generate_names_uuid_dict().keys()
            with st.form(state_key+"_Link_To_Campaign_Upload"):
                st.write("**Choose a Campaign to save the audience**")
                selected_name = st.selectbox("List of Campaigns",
                                             campaigns_names)
                link_to_campaign_button = st.form_submit_button(
                    label="Save to Campaign")

            if link_to_campaign_button:
                selected_uuid = generate_names_uuid_dict()[selected_name]
                st.session_state[CAMPAIGNS_KEY][
                    selected_uuid].audiences = st.session_state[
                        f"{state_key}_Result_Final_Query"]
                st.success(f"Saved to campaign {selected_name}")
