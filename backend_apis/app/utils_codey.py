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

from google.cloud import bigquery


def get_tags_from_table(
        datacatalog_client,
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
        bqclient,
        datacatalog_client,
        query: str,
        project_id: str,
        dataset_id: str, 
        tag_template_name: str
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
            The name of the BigQuery tag template to use to get the table descriptions.
        state_key: 
            The key to use to store the metadata in the Streamlit session state.
    """
    # print("Gets the metadata once")
    query_job = bqclient.query(query)  # API request
    rows = query_job.result()
    metadata = []

    for row in rows:
        full_table_path = f'`{project_id}.{dataset_id}.{row.table_name}`'
        table_metadata = f'[SCHEMA details for table {full_table_path}]\n'

        table_metadata += get_tags_from_table(
            datacatalog_client,
            dataset_id, 
            row.table_name, 
            project_id, 
            tag_template_name)
        metadata.append(table_metadata)

    return metadata


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
        prompt: str,
        project_id: str
):
    """Generates a prompt for a GoogleSQL query compatible with BigQuery.

    Args:
        question: 
            The question to answer.
        metadata: 
            A list of dictionaries, where each dictionary describes a BigQuery table. 
            The dictionaries should have the following keys:
            - name: The name of the table.
            - schema: The schema of the table.
            - description: A description of the table.
        state_key: 
            The key to use to store the prompt in the session state.

    Returns:
        The prompt.
    """
    PROMPT_PROJECT_ID = [project_id]*7
    context = ''
    for i in metadata:
        context += i

    return (f"{prompt.format(context,*PROMPT_PROJECT_ID)} \n"
             f"[Q]: {question} \n"
             "[SQL]:")


def generate_sql_and_query(
        llm,
        datacatalog_client,
        prompt_template: str,
        query_metadata: str,
        question: str,
        project_id: str,
        dataset_id: str,
        tag_template_name: str,
        bqclient: bigquery.Client):
    """Generates a GoogleSQL query and executes it against a BigQuery dataset.

    Args:
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

    metadata = get_metadata_from_dataset(
        bqclient=bqclient,
        datacatalog_client=datacatalog_client,
        query=query_metadata, 
        project_id=project_id, 
        dataset_id=dataset_id,
        tag_template_name=tag_template_name)

    prompt = generate_prompt(
        question, 
        metadata,
        prompt_template,
        project_id)

    gen_code = llm.predict(
        prompt = prompt,
        max_output_tokens = 1024,
        temperature=0.3
    ).text.replace("```","")
    gen_code = gen_code[gen_code.find("SELECT"):]
    result = []
    result_job = bqclient.query(gen_code)
    for row in result_job:
        result.append(dict(row.items()))
    return result, gen_code, prompt
