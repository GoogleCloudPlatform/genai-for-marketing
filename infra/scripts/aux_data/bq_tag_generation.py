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

from google.cloud import datacatalog_v1
from google.cloud import bigquery
from typing import List

datacatalog_client = datacatalog_v1.DataCatalogClient()


def define_query(PROJECT_ID: str, DATASET_ID: str):
    # Perform a query to retrieve metadata
    return f'''
    SELECT
    meta.*,
    cols.data_type as data_type
    FROM
    `{PROJECT_ID}.{DATASET_ID}.metadata` meta
    JOIN
    `{PROJECT_ID}.{DATASET_ID}.INFORMATION_SCHEMA.COLUMNS` cols
    ON
    cols.table_schema = meta.dataset_id
    AND cols.table_name = meta.table_id
    AND cols.column_name = meta.column_id
    '''


def create_tag_template(
    TAG_TEMPLATE_ID: str,
    PROJECT_ID: str,
    LOCATION: str
):
    tag_template = datacatalog_v1.TagTemplate()
    tag_template.name = TAG_TEMPLATE_ID
    tag_template.display_name = "Talk to data catalog template"

    field_desc = datacatalog_v1.TagTemplateField()
    field_desc.type_.primitive_type = datacatalog_v1.FieldType.PrimitiveType.STRING
    field_desc.display_name = "Description"
    field_desc.is_required = True
    tag_template.fields["description"] = field_desc

    field_pk = datacatalog_v1.TagTemplateField()
    field_pk.type_.primitive_type = datacatalog_v1.FieldType.PrimitiveType.BOOL
    field_pk.display_name = "is_primary_key"
    field_pk.is_required = True
    tag_template.fields["is_primary_key"] = field_pk

    field_fk = datacatalog_v1.TagTemplateField()
    field_fk.type_.primitive_type = datacatalog_v1.FieldType.PrimitiveType.BOOL
    field_fk.display_name = "is_foreign_key"
    field_fk.is_required = True
    tag_template.fields["is_foreign_key"] = field_fk

    field_type = datacatalog_v1.TagTemplateField()
    field_type.type_.primitive_type = datacatalog_v1.FieldType.PrimitiveType.STRING
    field_type.display_name = "Data Type"
    field_type.is_required = False
    tag_template.fields["data_type"] = field_type

    try:
        tag_full_path = datacatalog_client.create_tag_template(
            parent=f'projects/{PROJECT_ID}/locations/{LOCATION}',
            tag_template_id=TAG_TEMPLATE_ID, 
            tag_template=tag_template)
        print('Tag created')
    except Exception as e:
        print(e)

    return tag_full_path.name


def tag_bq_columns(
        PROJECT_ID: str,
        TAG_TEMPLATE_PATH: str,
        TAG_TEMPLATE_ID: str,
        DATASET_ID: str, 
        table_id: str, 
        column_id: str, 
        values: List):
    # Lookup Data Catalog's Entry referring to the table.
    resource_name = (
        f"//bigquery.googleapis.com/projects/{PROJECT_ID}/datasets/{DATASET_ID}/tables/{table_id}"
    )

    table_entry = datacatalog_client.lookup_entry(
        request={"linked_resource": resource_name}
    )
    # Attach a Tag to the table.
    tag = datacatalog_v1.types.Tag()

    tag.template = TAG_TEMPLATE_PATH
    tag.name = "talktodata tag"
    tag.fields["description"] = datacatalog_v1.types.TagField()
    tag.fields["description"].string_value = values[0]

    tag.fields["is_primary_key"] = datacatalog_v1.types.TagField()
    tag.fields["is_primary_key"].bool_value = values[1]

    tag.fields["is_foreign_key"] = datacatalog_v1.types.TagField()
    tag.fields["is_foreign_key"].bool_value = values[2]

    tag.fields["data_type"] = datacatalog_v1.types.TagField()
    tag.fields["data_type"].string_value = values[3]

    tag.column = column_id
    try:
        tag = datacatalog_client.create_tag(parent=table_entry.name, tag=tag)
        print('tag created/updated for {}'.format(column_id))
    except Exception as e:
        print(e)
        print(
            'Failed to create template {} for {}.{}.{}.{}'.format(
                TAG_TEMPLATE_ID, 
                DATASET_ID, 
                DATASET_ID, 
                table_id,
                column_id)
        )

def tag_metadata_from_bq(
        PROJECT_ID,
        DATASET_ID,
        TAG_TEMPLATE_PATH,
        TAG_TEMPLATE_ID
):
    bq_client = bigquery.Client(project=PROJECT_ID)
    query_job = bq_client.query(define_query(PROJECT_ID, DATASET_ID))
    rows = query_job.result()
    for row in rows:
        tag_bq_columns(
            PROJECT_ID,
            TAG_TEMPLATE_PATH,
            TAG_TEMPLATE_ID,
            row.dataset_id, 
            row.table_id, 
            row.column_id, 
            [row.description, row.is_primary_key, row.is_foreign_key, row.data_type])
        

def create_template_and_tag_bq(
        PROJECT_ID: str,
        DATASET_ID: str,
        TAG_TEMPLATE_ID: str,
        LOCATION: str
):

    TAG_TEMPLATE_PATH = create_tag_template(
        TAG_TEMPLATE_ID, 
        PROJECT_ID, 
        LOCATION)
    
    tag_metadata_from_bq(
        PROJECT_ID,
        DATASET_ID,
        TAG_TEMPLATE_PATH,
        TAG_TEMPLATE_ID
    )