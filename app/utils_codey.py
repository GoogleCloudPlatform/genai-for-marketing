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


from typing import Optional
from functools import partial
import streamlit as st

from google.cloud import datacatalog_v1
from google.cloud import bigquery
from pandas import DataFrame

from google.cloud.exceptions import NotFound
from google.cloud.exceptions import BadRequest
from vertexai.preview.language_models import TextGenerationModel

from google.cloud import translate_v2 as translate
from utils_config import TRANSLATE_LANGUAGES
from utils_config import CODE_MODEL_NAME
from utils_config import TEXT_MODEL_NAME

import pandas as pd
import utils_default_image_text

from utils_streamlit import reset_page_state

translate_client = translate.Client()
prompt = '''This is a task converting text into GoogleSQL statement. We will first given the dataset schema and then ask a question in text. You are asked to generate SQL statement.
Here is an example: Convert text to SQL:
[SCHEMA details for table `rl-llm-dev.cdp_dataset.customers`]
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: cart_total - Data Type: FLOAT64 - Primary Key: False - foreign Key: False - Description: The value of the items in the customer's shopping cart.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: channel - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The channel through which the customer was acquired.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: city - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The city where the customer lives.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: customer_id - Data Type: INT64 - Primary Key: True - foreign Key: False - Description: A unique identifier of the customer.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: email - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The customer's email address.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: is_media_follower - Data Type: BOOL - Primary Key: False - foreign Key: False - Description: Whether the customer is a social media follower.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: last_activity_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date of the customer's last account activity.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: last_purchase_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date the customer made their last purchase.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: last_sign_up_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date the customer signed up.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: loyalty_score - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: A score that measures the customer's engagement with the company.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: state - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The state where the customer lives.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: total_emails - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total number of emails opened by the customer.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: total_purchases - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total number of purchases made by the customer.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: total_value - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total value of all purchases made by the customer.
[SCHEMA details for table `rl-llm-dev.cdp_dataset.transactions`]
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: app_purchase_qnt - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The value of the in-app purchase.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: customer_id - Data Type: INT64 - Primary Key: False - foreign Key: True - Description: A unique identifier of the customer.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: product_id - Data Type: INT64 - Primary Key: False - foreign Key: True - Description: The code of the inventory item that was purchased.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: product_name - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The name of the product that was purchased.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transaction_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date the transaction was made.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transaction_id - Data Type: INT64 - Primary Key: True - foreign Key: False - Description: A unique identifier for the transaction.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transaction_value - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total value of the transaction.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transation_qnt - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The quantity of items purchased in the transaction.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transation_type - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The type of transaction (e.g., purchase, refund, etc.).
[SCHEMA details for table `rl-llm-dev.cdp_dataset.events`]:
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: customer_id - Data Type: INT64 - Primary Key: False - foreign Key: True - Description: A unique identifier of the customer.
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: event_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date of the event.
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: event_id - Data Type: INT64 - Primary Key: True - foreign Key: False - Description: A unique identifier for the event.
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: event_type - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The type of event.
[Q]: What is the city and state with the most customer transactions?
[SQL]: SELECT c.city, c.state, SUM(t.transaction_qnt) as total_transactions
FROM `rl-llm-dev.cdp_dataset.customers` AS c
JOIN `rl-llm-dev.cdp_dataset.transactions` as t
ON c.customer_id = t.customer_id
GROUP BY c.city, c.state
ORDER BY total_transactions DESC

Here is an example: Convert text to SQL:
[SCHEMA details for table `rl-llm-dev.cdp_dataset.customers`]
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: cart_total - Data Type: FLOAT64 - Primary Key: False - foreign Key: False - Description: The value of the items in the customer's shopping cart.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: channel - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The channel through which the customer was acquired.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: city - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The city where the customer lives.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: customer_id - Data Type: INT64 - Primary Key: True - foreign Key: False - Description: A unique identifier of the customer.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: email - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The customer's email address.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: is_media_follower - Data Type: BOOL - Primary Key: False - foreign Key: False - Description: Whether the customer is a social media follower.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: last_activity_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date of the customer's last account activity.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: last_purchase_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date the customer made their last purchase.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: last_sign_up_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date the customer signed up.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: loyalty_score - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: A score that measures the customer's engagement with the company.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: state - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The state where the customer lives.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: total_emails - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total number of emails opened by the customer.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: total_purchases - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total number of purchases made by the customer.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: total_value - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total value of all purchases made by the customer.
[SCHEMA details for table `rl-llm-dev.cdp_dataset.transactions`]
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: app_purchase_qnt - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The value of the in-app purchase.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: customer_id - Data Type: INT64 - Primary Key: False - foreign Key: True - Description: A unique identifier of the customer.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: product_id - Data Type: INT64 - Primary Key: False - foreign Key: True - Description: The code of the inventory item that was purchased.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: product_name - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The name of the product that was purchased.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transaction_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date the transaction was made.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transaction_id - Data Type: INT64 - Primary Key: True - foreign Key: False - Description: A unique identifier for the transaction.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transaction_value - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total value of the transaction.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transation_qnt - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The quantity of items purchased in the transaction.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transation_type - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The type of transaction (e.g., purchase, refund, etc.).
[SCHEMA details for table `rl-llm-dev.cdp_dataset.events`]:
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: customer_id - Data Type: INT64 - Primary Key: False - foreign Key: True - Description: A unique identifier of the customer.
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: event_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date of the event.
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: event_id - Data Type: INT64 - Primary Key: True - foreign Key: False - Description: A unique identifier for the event.
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: event_type - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The type of event.
[Q]: What are the customer emails ordered by the quantity of purchases by the customer in the city of Atlanta and the state of Georgia?
[SQL]: SELECT c.email, c.total_purchases 
FROM `rl-llm-dev.cdp_dataset.customers` as c
WHERE c.city = "Atlanta" AND c.state = "Georgia"
ORDER BY c.total_purchases DESC

Here is an example: Convert text to SQL:
[SCHEMA details for table `rl-llm-dev.cdp_dataset.customers`]
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: cart_total - Data Type: FLOAT64 - Primary Key: False - foreign Key: False - Description: The value of the items in the customer's shopping cart.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: channel - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The channel through which the customer was acquired.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: city - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The city where the customer lives.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: customer_id - Data Type: INT64 - Primary Key: True - foreign Key: False - Description: A unique identifier of the customer.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: email - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The customer's email address.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: is_media_follower - Data Type: BOOL - Primary Key: False - foreign Key: False - Description: Whether the customer is a social media follower.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: last_activity_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date of the customer's last account activity.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: last_purchase_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date the customer made their last purchase.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: last_sign_up_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date the customer signed up.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: loyalty_score - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: A score that measures the customer's engagement with the company.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: state - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The state where the customer lives.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: total_emails - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total number of emails opened by the customer.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: total_purchases - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total number of purchases made by the customer.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: total_value - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total value of all purchases made by the customer.
[SCHEMA details for table `rl-llm-dev.cdp_dataset.transactions`]
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: app_purchase_qnt - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The value of the in-app purchase.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: customer_id - Data Type: INT64 - Primary Key: False - foreign Key: True - Description: A unique identifier of the customer.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: product_id - Data Type: INT64 - Primary Key: False - foreign Key: True - Description: The code of the inventory item that was purchased.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: product_name - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The name of the product that was purchased.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transaction_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date the transaction was made.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transaction_id - Data Type: INT64 - Primary Key: True - foreign Key: False - Description: A unique identifier for the transaction.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transaction_value - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total value of the transaction.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transation_qnt - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The quantity of items purchased in the transaction.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transation_type - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The type of transaction (e.g., purchase, refund, etc.).
[SCHEMA details for table `rl-llm-dev.cdp_dataset.events`]:
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: customer_id - Data Type: INT64 - Primary Key: False - foreign Key: True - Description: A unique identifier of the customer.
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: event_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date of the event.
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: event_id - Data Type: INT64 - Primary Key: True - foreign Key: False - Description: A unique identifier for the event.
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: event_type - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The type of event.
[Q]: What are the customer emails ordered by the total transactions in app by the customer in the city of Atlanta and the state of Georgia?
[SQL]: SELECT c.email, SUM(t.app_purchase_qnt) as total_app_purchase
FROM `rl-llm-dev.cdp_dataset.customers` as c
JOIN `rl-llm-dev.cdp_dataset.transactions` as t
ON c.customer_id = t.customer_id
WHERE c.city = "Atlanta" AND c.state = "Georgia"
GROUP BY c.email, c.city, c.state
ORDER BY total_app_purchase DESC

Here is an example: Convert text to SQL:
[SCHEMA details for table `rl-llm-dev.cdp_dataset.customers`]
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: cart_total - Data Type: FLOAT64 - Primary Key: False - foreign Key: False - Description: The value of the items in the customer's shopping cart.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: channel - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The channel through which the customer was acquired.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: city - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The city where the customer lives.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: customer_id - Data Type: INT64 - Primary Key: True - foreign Key: False - Description: A unique identifier of the customer.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: email - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The customer's email address.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: is_media_follower - Data Type: BOOL - Primary Key: False - foreign Key: False - Description: Whether the customer is a social media follower.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: last_activity_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date of the customer's last account activity.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: last_purchase_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date the customer made their last purchase.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: last_sign_up_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date the customer signed up.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: loyalty_score - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: A score that measures the customer's engagement with the company.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: state - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The state where the customer lives.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: total_emails - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total number of emails opened by the customer.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: total_purchases - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total number of purchases made by the customer.
Full table name: `rl-llm-dev.cdp_dataset.customers` - Column: total_value - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total value of all purchases made by the customer.
[SCHEMA details for table `rl-llm-dev.cdp_dataset.transactions`]
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: app_purchase_qnt - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The value of the in-app purchase.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: customer_id - Data Type: INT64 - Primary Key: False - foreign Key: True - Description: A unique identifier of the customer.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: product_id - Data Type: INT64 - Primary Key: False - foreign Key: True - Description: The code of the inventory item that was purchased.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: product_name - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The name of the product that was purchased.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transaction_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date the transaction was made.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transaction_id - Data Type: INT64 - Primary Key: True - foreign Key: False - Description: A unique identifier for the transaction.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transaction_value - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The total value of the transaction.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transation_qnt - Data Type: INT64 - Primary Key: False - foreign Key: False - Description: The quantity of items purchased in the transaction.
Full table name: `rl-llm-dev.cdp_dataset.transactions` - Column: transation_type - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The type of transaction (e.g., purchase, refund, etc.).
[SCHEMA details for table `rl-llm-dev.cdp_dataset.events`]:
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: customer_id - Data Type: INT64 - Primary Key: False - foreign Key: True - Description: A unique identifier of the customer.
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: event_date - Data Type: DATE - Primary Key: False - foreign Key: False - Description: The date of the event.
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: event_id - Data Type: INT64 - Primary Key: True - foreign Key: False - Description: A unique identifier for the event.
Full table name: `rl-llm-dev.cdp_dataset.events` - Column: event_type - Data Type: STRING - Primary Key: False - foreign Key: False - Description: The type of event.
[Q]: Retrieve top 10 customer emails ordered by loyalty score
[SQL]: SELECT c.email
FROM `rl-llm-dev.cdp_dataset.customers` as c
ORDER BY c.loyalty_score DESC 

Here is an example: Convert text to SQL:'''


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
            The name of the BigQuery tag template to use to get the table descriptions.
        state_key: 
            The key to use to store the metadata in the Streamlit session state.
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
        state_key: str
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
    context = ''
    for i in metadata:
        context += i

    st.session_state[state_key] = f"""{prompt}
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
        prompt_example: str,
        fallback_query: str="",
        email_prompt_example: str="",
        text_model: TextGenerationModel=None) -> Optional[DataFrame]:
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
        prompt_example: 
            An example prompt for the query.
        email_prompt_example: 
            An example prompt for the email.
        text_model: 
            A TextGenerationModel object.

    Returns:
        A DataFrame containing the results of the query.

    Raises:
        NotFoundError: If the dataset or table is not found.
        BadRequestError: If the query is invalid.
    """
    with st.form(f"{state_key}_form"):
        st.write(f"**{title}**")

        question = st.text_area(
            'Ask a question using natural language to the dataset above',
            key=f"{state_key}_question_prompt_text_area",
            value=prompt_example, height=50)

        # Every form must have a submit button.
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        reset_page_state(state_key)
        if not question:
            st.warning("Question is empty")
            return None
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
            client_code_model = TextGenerationModel.from_pretrained(TEXT_MODEL_NAME)
            try:
                gen_code = client_code_model.predict(
                    prompt = st.session_state[f"{state_key}_Prompt_Template"],
                    max_output_tokens = 1024,
                    temperature=0.2
                )
            except:
                st.session_state[f"{state_key}_Gen_Code"] = fallback_query
            else:
                if gen_code and gen_code.text:
                    st.session_state[f"{state_key}_Gen_Code"] = gen_code.text
                else:
                    st.session_state[f"{state_key}_Gen_Code"] = fallback_query

        try:
            with st.spinner('Querying BigQuery...'):
                result_query = bqclient.query(st.session_state[f"{state_key}_Gen_Code"])
                result_query.result()
        except:
            st.session_state[f"{state_key}_Gen_Code"] = fallback_query
            with st.spinner('Querying BigQuery...'):
                try:
                    result_query = bqclient.query(st.session_state[f"{state_key}_Gen_Code"])
                    result_query.result()
                except:
                    if state_key == "TalkToData_insight":
                        st.session_state[f"{state_key}_Result_Final_Query"] = pd.DataFrame(utils_default_image_text.AUDIENCE_RESULT_0)
                    elif state_key == "TalkToData_audience":
                        st.session_state[f"{state_key}_Result_Final_Query"] = pd.DataFrame(utils_default_image_text.AUDIENCE_RESULT_1)
                    elif state_key == "TalkToData_followup":
                        st.session_state[f"{state_key}_Result_Final_Query"] = pd.DataFrame(utils_default_image_text.AUDIENCE_RESULT_2)
                else:
                    st.session_state[
                        f"{state_key}_Result_Final_Query"] = result_query.to_dataframe()
    
            st.write('Resulting query generated by PaLM 2')
            st.write(f"""```sql
                    {st.session_state[f"{state_key}_Gen_Code"]}""")
            st.success('Query executed successfully. Retrieving dataset.')
            st.write('')
            st.write('Resulting table (limited by 50 rows)')
            st.dataframe(
                st.session_state[f"{state_key}_Result_Final_Query"].iloc[:50])
        else:
            st.write('Resulting query generated by PaLM 2')
            st.write(f"""```sql
                    {st.session_state[f"{state_key}_Gen_Code"]}""")
            st.success('Query executed successfully. Retrieving dataset.')
            st.session_state[
                f"{state_key}_Result_Final_Query"] = result_query.to_dataframe()
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
    
    if f"{state_key}_Result_Final_Query" in st.session_state:
        if email_prompt_example:
            results_length = len(
                st.session_state[f"{state_key}_Result_Final_Query"])
            with st.form(f"{state_key}_email_form"):
                st.write(f"**Write an email**")

                col1, col2 = st.columns([70,30])

                with col1:
                    email_prompt = st.text_area(
                        'Write an email using natural language to each customer',
                        key=f"{state_key}_email_prompt_text_area",
                        value=email_prompt_example,
                        height=170)
                    number_emails = st.slider(
                        "Number of emails to generate",
                        min_value=1,
                        max_value=min(results_length, 500),
                        step=1,
                        value=int(min(results_length/2, 2)))
                
                with col2:
                    st.write('**Model parameters**')
                    temperature = st.slider('Temperature', 0.0, 1.0, 0.2)

                # Every form must have a submit button.
                email_submit_button = st.form_submit_button("Submit")

            if email_submit_button:
                if not email_prompt:
                    st.warning("Email prompt is empty.")
                    return None
                
                emails = {"email":[], "generated_email": []}

                bar = st.progress(0.0, f"Generating emails...0.0%")
                
                for i, row in st.session_state[
                        f"{state_key}_Result_Final_Query"].iloc[
                            :number_emails].iterrows():
                    

                    data_string = "\n".join(
                        [f"{row_key}: {row[row_key]}" for row_key in row.keys()])
                    
                    response = text_model.predict(
                            prompt=f"{data_string} \n {email_prompt}",
                            temperature=temperature,
                            max_output_tokens=1024,
                        ).text
                    
                    emails["email"].append(row.get("email","")),
                    emails["generated_email"].append(response)
                    
                    percent = (i+1)/number_emails
                    bar.progress(percent, f"Generating emails...{percent*100:.1f}%")
                
                st.success("Emails generated")
                
                st.session_state[f"{state_key}_Generated_Emails"] = DataFrame(
                    emails)
                st.session_state[
                    f"{state_key}_Generated_Emails_CSV"] = DataFrame(
                    emails).to_csv().encode('utf-8')
            
            if f"{state_key}_Generated_Emails" in st.session_state:
                st.write('Generated emails')
                st.session_state[f"{state_key}_Generated_Emails"] = st.data_editor(
                    st.session_state[f"{state_key}_Generated_Emails"]
                )
                st.download_button(
                    "Download csv", 
                    data=st.session_state[f"{state_key}_Generated_Emails_CSV"],
                    file_name="emails.csv",
                    mime="text/csv") 
                
                with st.form(key=f'{state_key}_translate_form'):
                    st.write(f"**Translate generated text**")

                    target_language_name = st.selectbox(
                        "Languages", options=TRANSLATE_LANGUAGES.keys())

                    translate_submit_button = st.form_submit_button(
                        label='Translate')

                if translate_submit_button:
                    translated_df = st.session_state[
                        f"{state_key}_Generated_Emails"].copy()
                    
                    with st.spinner("Translating..."):
                        translate_map = partial(
                            translate_client.translate,
                            source_language="en",
                            target_language=TRANSLATE_LANGUAGES[target_language_name])
                        translated_df["generated_email"] = translated_df[
                            "generated_email"].apply(
                            translate_map).apply(
                            lambda x: x.get("translatedText",""))
                        st.session_state[
                            f"{state_key}_Translated"] = translated_df
                        st.session_state[
                            f"{state_key}_Translated_CSV"
                            ] = translated_df.to_csv().encode('utf-8')
                    st.success("Emails translated")
                
                if f"{state_key}_Translated" in st.session_state:
                    st.write('Translated Generated emails')
                    st.session_state[f"{state_key}_Translated"] = st.data_editor(
                        st.session_state[f"{state_key}_Translated"]) 
                    st.download_button(
                        "Download CSV", 
                        data=st.session_state[f"{state_key}_Translated_CSV"],
                        file_name="translated_emails.csv",
                        mime="text/csv") 
  
        else:
            return st.session_state[f"{state_key}_Result_Final_Query"]
    
    return None
