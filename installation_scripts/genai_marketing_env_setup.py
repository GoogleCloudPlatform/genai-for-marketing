#!/bin/python3

import sys


PROJECT_ID = sys.argv[1]  # Change to your project ID
LOCATION = sys.argv[2]
DATASET_ID = sys.argv[3]

# Tag template 
TAG_TEMPLATE_ID = 'llmcdptemplate'
TAG_TEMPLATE_PATH = f"projects/{PROJECT_ID}/locations/{LOCATION}/tagTemplates/{TAG_TEMPLATE_ID}"

# Set the project id
#! gcloud config set project {PROJECT_ID}


# Create BigQuery Dataset talktodata on your project
from google.cloud import bigquery
from google.cloud import datacatalog_v1

bq_client = bigquery.Client(project=PROJECT_ID)
datacatalog_client = datacatalog_v1.DataCatalogClient()

dataset_id = "{}.{}".format(bq_client.project, DATASET_ID)
dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"

# Create the dataset
try:
    dataset = bq_client.create_dataset(dataset, timeout=30,exists_ok=True)
    print(f'Dataset {DATASET_ID} create successfully.')
except Exception as e:
    print(e)

QUERY = f'SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.INFORMATION_SCHEMA.TABLES` WHERE table_name NOT LIKE "%metadata%"'
def get_tags_from_table(table_id):
    # Lookup Data Catalog's Entry referring to the table.
    resource_name = (
        f"//bigquery.googleapis.com/projects/{PROJECT_ID}/datasets/{DATASET_ID}/tables/{table_id}"
    )
    table_entry = datacatalog_client.lookup_entry(
        request={"linked_resource": resource_name}
    )

    # Make the request
    page_result = datacatalog_client.list_tags(parent=table_entry.name)
    # print(page_result)

    tags_str = ''

    # Handle the response
    for response in page_result:
        if response.template == TAG_TEMPLATE_PATH:
            desc = response.fields["description"].string_value
            data_type = response.fields["data_type"].string_value
            pk = response.fields["is_primary_key"].bool_value
            fk = response.fields["is_foreign_key"].bool_value            
            tags_str += ("Table: {} "
                         "- Column: {} " 
                         "- Data Type: {} " 
                         "- Primary Key: {} " 
                         "- Foreing Key: {} " 
                         "- Description: {}\n".format(
                table_id, response.column, data_type, pk, fk, desc))
    return tags_str

def get_metadata_from_dataset(
        query: str
):
    # print("Gets the metadata once")
    query_job = bq_client.query(query)  # API request
    rows = query_job.result()
    metadata = []

    for row in rows:
        table_metadata = {}
        table_metadata['ddl'] = row.ddl
        table_metadata['description'] = get_tags_from_table(row.table_name)
        metadata.append(table_metadata)
    
    return metadata

tags = get_metadata_from_dataset(QUERY)

if len(tags) == 0:
    from aux_data import data_gen

    data_gen.generate_and_populate_dataset(
        PROJECT_ID=PROJECT_ID,
        DATASET_ID=DATASET_ID
    )


    from aux_data import bq_tag_generation

    bq_tag_generation.create_template_and_tag_bq(
        PROJECT_ID,
        DATASET_ID,
        TAG_TEMPLATE_ID,
        LOCATION
    )
